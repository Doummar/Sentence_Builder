"""
Storage Backend for Grammar Pro.

Provides the low-level storage interface for persisting data.
"""

import json
import os
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..config.settings import Settings


@dataclass
class StorageConfig:
    """Configuration for storage backend."""
    storage_type: str = "json"  # 'json', 'sqlite', or 'anki_db'
    data_directory: Path = None
    use_anki_database: bool = False


class StorageBackend(ABC):
    """
    Abstract base class for storage backends.
    
    All storage backends must implement this interface.
    """
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the storage backend.
        
        Returns:
            True if initialization was successful
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the storage backend."""
        pass
    
    @abstractmethod
    def save_data(self, key: str, data: Any) -> bool:
        """
        Save data with a given key.
        
        Args:
            key: Unique key for the data
            data: Data to save (must be JSON-serializable)
            
        Returns:
            True if save was successful
        """
        pass
    
    @abstractmethod
    def load_data(self, key: str, default: Any = None) -> Any:
        """
        Load data with a given key.
        
        Args:
            key: Unique key for the data
            default: Default value if key not found
            
        Returns:
            The loaded data, or default if not found
        """
        pass
    
    @abstractmethod
    def delete_data(self, key: str) -> bool:
        """
        Delete data with a given key.
        
        Args:
            key: Unique key for the data
            
        Returns:
            True if deletion was successful
        """
        pass
    
    @abstractmethod
    def list_keys(self, prefix: str = "") -> List[str]:
        """
        List all keys with a given prefix.
        
        Args:
            prefix: Optional prefix to filter keys
            
        Returns:
            List of keys
        """
        pass
    
    @abstractmethod
    def clear_all(self) -> None:
        """Clear all stored data."""
        pass


class JSONStorageBackend(StorageBackend):
    """
    JSON-based storage backend.
    
    Stores data as JSON files in a directory.
    """
    
    def __init__(self, config: StorageConfig = None, settings: 'Settings' = None):
        """
        Initialize the JSON storage backend.
        
        Args:
            config: Storage configuration
            settings: Settings instance
        """
        self.config = config or StorageConfig()
        self.settings = settings
        self._data_dir: Optional[Path] = None
        self._initialized = False
    
    def initialize(self) -> bool:
        """Initialize the JSON storage backend."""
        if self._initialized:
            return True
        
        # Determine data directory
        if self.config.data_directory:
            self._data_dir = self.config.data_directory
        elif self.settings:
            # Use Anki's addon directory
            from anki.utils import getAddonPath
            addon_dir = Path(getAddonPath(__name__.split('.')[0]))
            self._data_dir = addon_dir / "data"
        else:
            # Use a default directory
            self._data_dir = Path.home() / ".grammar_pro" / "data"
        
        # Create directory if it doesn't exist
        try:
            self._data_dir.mkdir(parents=True, exist_ok=True)
            self._initialized = True
            return True
        except Exception as e:
            print(f"Error initializing JSON storage: {e}")
            return False
    
    def shutdown(self) -> None:
        """Shutdown the JSON storage backend."""
        self._initialized = False
    
    def _get_file_path(self, key: str) -> Path:
        """Get the file path for a given key."""
        if not self._data_dir:
            self.initialize()
        
        # Sanitize the key to be a valid filename
        safe_key = key.replace("/", "_").replace("\\", "_").replace(":", "_")
        return self._data_dir / f"{safe_key}.json"
    
    def save_data(self, key: str, data: Any) -> bool:
        """Save data to a JSON file."""
        if not self._initialized:
            if not self.initialize():
                return False
        
        file_path = self._get_file_path(key)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")
            return False
    
    def load_data(self, key: str, default: Any = None) -> Any:
        """Load data from a JSON file."""
        if not self._initialized:
            if not self.initialize():
                return default
        
        file_path = self._get_file_path(key)
        
        if not file_path.exists():
            return default
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return default
    
    def delete_data(self, key: str) -> bool:
        """Delete a data file."""
        if not self._initialized:
            if not self.initialize():
                return False
        
        file_path = self._get_file_path(key)
        
        if file_path.exists():
            try:
                file_path.unlink()
                return True
            except Exception as e:
                print(f"Error deleting data file {file_path}: {e}")
                return False
        
        return False
    
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all data keys with a given prefix."""
        if not self._initialized:
            if not self.initialize():
                return []
        
        keys = []
        if self._data_dir and self._data_dir.exists():
            for file_path in self._data_dir.glob("*.json"):
                key = file_path.stem
                if key.startswith(prefix):
                    keys.append(key)
        
        return keys
    
    def clear_all(self) -> None:
        """Clear all stored data."""
        if not self._initialized:
            if not self.initialize():
                return
        
        if self._data_dir and self._data_dir.exists():
            for file_path in self._data_dir.glob("*.json"):
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


class SQLiteStorageBackend(StorageBackend):
    """
    SQLite-based storage backend.
    
    Stores data in an SQLite database.
    """
    
    def __init__(self, config: StorageConfig = None, settings: 'Settings' = None):
        """
        Initialize the SQLite storage backend.
        
        Args:
            config: Storage configuration
            settings: Settings instance
        """
        self.config = config or StorageConfig()
        self.settings = settings
        self._db_path: Optional[Path] = None
        self._connection: Optional[sqlite3.Connection] = None
        self._initialized = False
    
    def initialize(self) -> bool:
        """Initialize the SQLite storage backend."""
        if self._initialized:
            return True
        
        # Determine database path
        if self.config.data_directory:
            self._db_path = self.config.data_directory / "grammar_pro.db"
        elif self.settings:
            from anki.utils import getAddonPath
            addon_dir = Path(getAddonPath(__name__.split('.')[0]))
            self._db_path = addon_dir / "grammar_pro.db"
        else:
            self._db_path = Path.home() / ".grammar_pro" / "grammar_pro.db"
        
        # Create directory if it doesn't exist
        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Connect to database
            self._connection = sqlite3.connect(str(self._db_path))
            
            # Create table
            cursor = self._connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self._connection.commit()
            
            self._initialized = True
            return True
        except Exception as e:
            print(f"Error initializing SQLite storage: {e}")
            return False
    
    def shutdown(self) -> None:
        """Shutdown the SQLite storage backend."""
        if self._connection:
            try:
                self._connection.close()
            except Exception as e:
                print(f"Error closing SQLite connection: {e}")
        
        self._connection = None
        self._initialized = False
    
    def save_data(self, key: str, data: Any) -> bool:
        """Save data to the SQLite database."""
        if not self._initialized:
            if not self.initialize():
                return False
        
        try:
            value = json.dumps(data, ensure_ascii=False)
            cursor = self._connection.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO data (key, value) VALUES (?, ?)",
                (key, value)
            )
            self._connection.commit()
            return True
        except Exception as e:
            print(f"Error saving data to SQLite: {e}")
            return False
    
    def load_data(self, key: str, default: Any = None) -> Any:
        """Load data from the SQLite database."""
        if not self._initialized:
            if not self.initialize():
                return default
        
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT value FROM data WHERE key = ?", (key,))
            result = cursor.fetchone()
            
            if result:
                return json.loads(result[0])
            return default
        except Exception as e:
            print(f"Error loading data from SQLite: {e}")
            return default
    
    def delete_data(self, key: str) -> bool:
        """Delete data from the SQLite database."""
        if not self._initialized:
            if not self.initialize():
                return False
        
        try:
            cursor = self._connection.cursor()
            cursor.execute("DELETE FROM data WHERE key = ?", (key,))
            self._connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting data from SQLite: {e}")
            return False
    
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all data keys with a given prefix."""
        if not self._initialized:
            if not self.initialize():
                return []
        
        try:
            cursor = self._connection.cursor()
            if prefix:
                cursor.execute("SELECT key FROM data WHERE key LIKE ?", (f"{prefix}%",))
            else:
                cursor.execute("SELECT key FROM data")
            
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error listing keys from SQLite: {e}")
            return []
    
    def clear_all(self) -> None:
        """Clear all stored data."""
        if not self._initialized:
            if not self.initialize():
                return
        
        try:
            cursor = self._connection.cursor()
            cursor.execute("DELETE FROM data")
            self._connection.commit()
        except Exception as e:
            print(f"Error clearing SQLite data: {e}")
