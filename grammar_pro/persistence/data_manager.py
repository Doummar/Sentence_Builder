"""
Data Manager for Grammar Pro.

High-level data management interface that handles persistence of all addon data.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .storage_backend import StorageBackend, JSONStorageBackend, StorageConfig

if TYPE_CHECKING:
    from ..config.settings import Settings
    from ..exercises.base_exercise import BaseExercise, ExerciseResult
    from ..statistics.statistics_manager import StatisticsData


@dataclass
class DataKey:
    """Keys for storing different types of data."""
    # Exercise data
    EXERCISE_HISTORY = "exercise_history"
    EXERCISE_SESSIONS = "exercise_sessions"
    CUSTOM_EXERCISES = "custom_exercises"
    
    # Statistics data
    STATISTICS = "statistics"
    STATISTICS_SUMMARY = "statistics_summary"
    WEAK_AREAS = "weak_areas"
    STRONG_AREAS = "strong_areas"
    
    # User data
    USER_PREFERENCES = "user_preferences"
    LEARNING_PROGRESS = "learning_progress"
    
    # Settings
    SETTINGS = "settings"
    
    # Cache
    GRAMMAR_CACHE = "grammar_cache"
    EXERCISE_CACHE = "exercise_cache"


class DataManager:
    """
    High-level data manager for Grammar Pro.
    
    Provides a unified interface for:
    - Saving and loading exercises
    - Managing statistics
    - Storing custom exercises
    - Caching data
    """
    
    def __init__(self, settings: 'Settings' = None, storage_config: StorageConfig = None):
        """
        Initialize the Data Manager.
        
        Args:
            settings: Settings instance
            storage_config: Optional storage configuration
        """
        self.settings = settings
        self.storage_config = storage_config or StorageConfig()
        self._backend: Optional[StorageBackend] = None
        self._initialized = False
        
        self.initialize()
    
    def initialize(self) -> bool:
        """Initialize the data manager."""
        if self._initialized:
            return True
        
        # Create the appropriate storage backend
        if self.storage_config.storage_type == "sqlite":
            from .storage_backend import SQLiteStorageBackend
            self._backend = SQLiteStorageBackend(self.storage_config, self.settings)
        else:
            # Default to JSON
            self._backend = JSONStorageBackend(self.storage_config, self.settings)
        
        self._initialized = self._backend.initialize()
        return self._initialized
    
    def shutdown(self) -> None:
        """Shutdown the data manager."""
        if self._backend:
            self._backend.shutdown()
        self._initialized = False
    
    def save_exercise(self, exercise: 'BaseExercise') -> bool:
        """
        Save an exercise to storage.
        
        Args:
            exercise: Exercise to save
            
        Returns:
            True if save was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        # Convert exercise to dictionary
        data = exercise.to_dict()
        
        # Save with a unique key
        key = f"{DataKey.EXERCISE_HISTORY}:{exercise.exercise_id}"
        return self._backend.save_data(key, data)
    
    def load_exercise(self, exercise_id: str) -> Optional[Dict[str, Any]]:
        """
        Load an exercise from storage.
        
        Args:
            exercise_id: ID of the exercise to load
            
        Returns:
            Exercise data as dictionary, or None if not found
        """
        if not self._initialized:
            if not self.initialize():
                return None
        
        key = f"{DataKey.EXERCISE_HISTORY}:{exercise_id}"
        return self._backend.load_data(key)
    
    def save_exercise_result(self, result: 'ExerciseResult') -> bool:
        """
        Save an exercise result to storage.
        
        Args:
            result: Exercise result to save
            
        Returns:
            True if save was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        # Convert result to dictionary
        data = result.to_dict()
        
        # Save with a unique key
        key = f"{DataKey.EXERCISE_HISTORY}:result:{result.exercise_id}:{result.timestamp}"
        return self._backend.save_data(key, data)
    
    def save_exercise_session(self, exercises: List['BaseExercise']) -> bool:
        """
        Save a complete exercise session.
        
        Args:
            exercises: List of exercises in the session
            
        Returns:
            True if save was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        # Convert exercises to dictionaries
        data = [ex.to_dict() for ex in exercises]
        
        # Save with timestamp
        timestamp = datetime.now().isoformat()
        key = f"{DataKey.EXERCISE_SESSIONS}:{timestamp}"
        return self._backend.save_data(key, data)
    
    def load_exercise_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Load recent exercise sessions.
        
        Args:
            limit: Maximum number of sessions to load
            
        Returns:
            List of session data
        """
        if not self._initialized:
            if not self.initialize():
                return []
        
        # List all session keys
        keys = self._backend.list_keys(DataKey.EXERCISE_SESSIONS)
        
        # Sort by timestamp (newest first)
        keys.sort(reverse=True)
        
        # Load the most recent sessions
        sessions = []
        for key in keys[:limit]:
            data = self._backend.load_data(key)
            if data:
                sessions.append(data)
        
        return sessions
    
    def save_statistics(self, data: 'StatisticsData') -> bool:
        """
        Save statistics data.
        
        Args:
            data: Statistics data to save
            
        Returns:
            True if save was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        # Convert data to dictionary if needed
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        
        key = DataKey.STATISTICS
        return self._backend.save_data(key, data)
    
    def load_statistics(self) -> Optional[Dict[str, Any]]:
        """
        Load statistics data.
        
        Returns:
            Statistics data as dictionary, or None if not found
        """
        if not self._initialized:
            if not self.initialize():
                return None
        
        return self._backend.load_data(DataKey.STATISTICS)
    
    def save_custom_exercise(self, exercise_data: Dict[str, Any]) -> bool:
        """
        Save a custom exercise.
        
        Args:
            exercise_data: Custom exercise data to save
            
        Returns:
            True if save was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        # Generate a unique ID if not provided
        if 'id' not in exercise_data:
            import uuid
            exercise_data['id'] = str(uuid.uuid4())
        
        key = f"{DataKey.CUSTOM_EXERCISES}:{exercise_data['id']}"
        return self._backend.save_data(key, exercise_data)
    
    def load_custom_exercise(self, exercise_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a custom exercise.
        
        Args:
            exercise_id: ID of the custom exercise
            
        Returns:
            Custom exercise data, or None if not found
        """
        if not self._initialized:
            if not self.initialize():
                return None
        
        key = f"{DataKey.CUSTOM_EXERCISES}:{exercise_id}"
        return self._backend.load_data(key)
    
    def list_custom_exercises(self) -> List[Dict[str, Any]]:
        """
        List all custom exercises.
        
        Returns:
            List of custom exercise data
        """
        if not self._initialized:
            if not self.initialize():
                return []
        
        # List all custom exercise keys
        keys = self._backend.list_keys(DataKey.CUSTOM_EXERCISES)
        
        # Load all custom exercises
        exercises = []
        for key in keys:
            data = self._backend.load_data(key)
            if data:
                exercises.append(data)
        
        return exercises
    
    def delete_custom_exercise(self, exercise_id: str) -> bool:
        """
        Delete a custom exercise.
        
        Args:
            exercise_id: ID of the custom exercise to delete
            
        Returns:
            True if deletion was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        key = f"{DataKey.CUSTOM_EXERCISES}:{exercise_id}"
        return self._backend.delete_data(key)
    
    def save_user_preferences(self, preferences: Dict[str, Any]) -> bool:
        """
        Save user preferences.
        
        Args:
            preferences: User preferences to save
            
        Returns:
            True if save was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        key = DataKey.USER_PREFERENCES
        return self._backend.save_data(key, preferences)
    
    def load_user_preferences(self) -> Optional[Dict[str, Any]]:
        """
        Load user preferences.
        
        Returns:
            User preferences as dictionary, or None if not found
        """
        if not self._initialized:
            if not self.initialize():
                return None
        
        return self._backend.load_data(DataKey.USER_PREFERENCES)
    
    def save_learning_progress(self, progress: Dict[str, Any]) -> bool:
        """
        Save learning progress.
        
        Args:
            progress: Learning progress data to save
            
        Returns:
            True if save was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        key = DataKey.LEARNING_PROGRESS
        return self._backend.save_data(key, progress)
    
    def load_learning_progress(self) -> Optional[Dict[str, Any]]:
        """
        Load learning progress.
        
        Returns:
            Learning progress as dictionary, or None if not found
        """
        if not self._initialized:
            if not self.initialize():
                return None
        
        return self._backend.load_data(DataKey.LEARNING_PROGRESS)
    
    def clear_exercise_history(self) -> None:
        """Clear all exercise history."""
        if not self._initialized:
            if not self.initialize():
                return
        
        # Delete all exercise history keys
        keys = self._backend.list_keys(DataKey.EXERCISE_HISTORY)
        for key in keys:
            self._backend.delete_data(key)
    
    def clear_all_data(self) -> None:
        """Clear all stored data."""
        if self._backend:
            self._backend.clear_all()
    
    def export_data(self, export_format: str = "json") -> Optional[str]:
        """
        Export all data in a specified format.
        
        Args:
            export_format: Format to export ('json' or 'csv')
            
        Returns:
            Exported data as string, or None if export failed
        """
        if not self._initialized:
            if not self.initialize():
                return None
        
        # Collect all data
        all_data = {}
        
        # Add exercise history
        keys = self._backend.list_keys(DataKey.EXERCISE_HISTORY)
        all_data['exercise_history'] = {}
        for key in keys:
            data = self._backend.load_data(key)
            if data:
                all_data['exercise_history'][key] = data
        
        # Add statistics
        stats = self.load_statistics()
        if stats:
            all_data['statistics'] = stats
        
        # Add custom exercises
        custom_exercises = self.list_custom_exercises()
        if custom_exercises:
            all_data['custom_exercises'] = custom_exercises
        
        # Export based on format
        if export_format == "json":
            return json.dumps(all_data, indent=2, ensure_ascii=False)
        elif export_format == "csv":
            # For CSV, we'd need to flatten the data
            # This is a simplified version
            return "CSV export not yet implemented"
        
        return None
    
    def import_data(self, data: str, import_format: str = "json") -> bool:
        """
        Import data from a specified format.
        
        Args:
            data: Data to import as string
            import_format: Format of the data ('json' or 'csv')
            
        Returns:
            True if import was successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        if import_format == "json":
            try:
                all_data = json.loads(data)
                
                # Import exercise history
                if 'exercise_history' in all_data:
                    for key, value in all_data['exercise_history'].items():
                        self._backend.save_data(key, value)
                
                # Import statistics
                if 'statistics' in all_data:
                    self.save_statistics(all_data['statistics'])
                
                # Import custom exercises
                if 'custom_exercises' in all_data:
                    for exercise in all_data['custom_exercises']:
                        self.save_custom_exercise(exercise)
                
                return True
            except Exception as e:
                print(f"Error importing JSON data: {e}")
                return False
        
        return False
