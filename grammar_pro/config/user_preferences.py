"""
User preferences management for Grammar Pro.

Handles user-specific preferences that are separate from general settings.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class UserPreferences:
    """
    User-specific preferences for Grammar Pro.
    
    These are separate from general settings and include things like
    favorite exercises, recent activity, and personal learning data.
    """
    
    # User's preferred languages (in order of preference)
    preferred_languages: List[str] = field(default_factory=lambda: ["danish"])
    
    # Recently used exercise modes
    recent_modes: List[str] = field(default_factory=list)
    
    # Favorite exercise modes
    favorite_modes: Set[str] = field(default_factory=set)
    
    # Last used exercise mode
    last_mode: Optional[str] = None
    
    # Last used language
    last_language: Optional[str] = None
    
    # Last session timestamp
    last_session: Optional[str] = None
    
    # Total sessions completed
    total_sessions: int = 0
    
    # Total exercises completed
    total_exercises: int = 0
    
    # Last dashboard view timestamp
    last_dashboard_view: Optional[str] = None
    
    # Internal: preferences file path
    _prefs_path: Optional[Path] = None
    
    def __post_init__(self):
        """Initialize preferences after creation."""
        if isinstance(self.preferred_languages, dict):
            self.preferred_languages = list(self.preferred_languages.keys())
        if isinstance(self.recent_modes, dict):
            self.recent_modes = list(self.recent_modes.keys())
        if isinstance(self.favorite_modes, dict):
            self.favorite_modes = set(self.favorite_modes.keys())
    
    @property
    def prefs_path(self) -> Path:
        """Get the preferences file path."""
        if self._prefs_path is None:
            from anki.utils import getAddonPath
            addon_dir = Path(getAddonPath(__name__.split('.')[0]))
            self._prefs_path = addon_dir / "preferences.json"
        return self._prefs_path
    
    def load(self) -> None:
        """Load preferences from file."""
        if self._prefs_path and self._prefs_path.exists():
            try:
                with open(self._prefs_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._load_from_dict(data)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Warning: Could not load preferences: {e}")
    
    def _load_from_dict(self, data: Dict[str, Any]) -> None:
        """Load preferences from a dictionary."""
        if 'preferred_languages' in data:
            self.preferred_languages = list(data['preferred_languages'])
        if 'recent_modes' in data:
            self.recent_modes = list(data['recent_modes'])
        if 'favorite_modes' in data:
            self.favorite_modes = set(data['favorite_modes'])
        if 'last_mode' in data:
            self.last_mode = data['last_mode']
        if 'last_language' in data:
            self.last_language = data['last_language']
        if 'last_session' in data:
            self.last_session = data['last_session']
        if 'total_sessions' in data:
            self.total_sessions = data['total_sessions']
        if 'total_exercises' in data:
            self.total_exercises = data['total_exercises']
        if 'last_dashboard_view' in data:
            self.last_dashboard_view = data['last_dashboard_view']
    
    def save(self) -> None:
        """Save preferences to file."""
        data = self.to_dict()
        self.prefs_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.prefs_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert preferences to a dictionary for serialization."""
        return {
            'preferred_languages': self.preferred_languages,
            'recent_modes': self.recent_modes,
            'favorite_modes': list(self.favorite_modes),
            'last_mode': self.last_mode,
            'last_language': self.last_language,
            'last_session': self.last_session,
            'total_sessions': self.total_sessions,
            'total_exercises': self.total_exercises,
            'last_dashboard_view': self.last_dashboard_view,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """Create UserPreferences instance from a dictionary."""
        prefs = cls()
        prefs._load_from_dict(data)
        return prefs
    
    def add_recent_mode(self, mode: str) -> None:
        """Add a mode to recent modes list."""
        if mode in self.recent_modes:
            self.recent_modes.remove(mode)
        self.recent_modes.insert(0, mode)
        # Keep only last 10
        if len(self.recent_modes) > 10:
            self.recent_modes = self.recent_modes[:10]
    
    def add_favorite_mode(self, mode: str) -> None:
        """Add a mode to favorites."""
        self.favorite_modes.add(mode)
    
    def remove_favorite_mode(self, mode: str) -> None:
        """Remove a mode from favorites."""
        self.favorite_modes.discard(mode)
    
    def is_favorite_mode(self, mode: str) -> bool:
        """Check if a mode is a favorite."""
        return mode in self.favorite_modes
    
    def record_session(self) -> None:
        """Record that a session was completed."""
        self.total_sessions += 1
        self.last_session = datetime.now().isoformat()
    
    def record_exercise(self) -> None:
        """Record that an exercise was completed."""
        self.total_exercises += 1
    
    def set_last_mode(self, mode: str) -> None:
        """Set the last used exercise mode."""
        self.last_mode = mode
        self.add_recent_mode(mode)
    
    def set_last_language(self, language: str) -> None:
        """Set the last used language."""
        self.last_language = language
        if language not in self.preferred_languages:
            self.preferred_languages.insert(0, language)
    
    def set_dashboard_viewed(self) -> None:
        """Record that the dashboard was viewed."""
        self.last_dashboard_view = datetime.now().isoformat()
