"""
Settings management for Grammar Pro addon.

Handles all configuration options, defaults, and persistence.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from anki.utils import getText


@dataclass
class GrammarSettings:
    """Settings related to grammar engine behavior."""
    # Default language for exercises
    default_language: str = "danish"
    
    # Enable adaptive learning
    adaptive_learning: bool = True
    
    # Number of exercises to generate for weak areas
    weak_area_exercises: int = 30
    
    # Mastery threshold (0.0 to 1.0)
    mastery_threshold: float = 0.85
    
    # Enable progressive difficulty
    progressive_difficulty: bool = True
    
    # Current unlocked level (1-14)
    current_level: int = 1


@dataclass
class UISettings:
    """UI-related settings."""
    # Theme: 'light', 'dark', or 'system'
    theme: str = "system"
    
    # Font family
    font_family: str = ""
    
    # Font size
    font_size: int = 12
    
    # Enable keyboard shortcuts
    keyboard_shortcuts: bool = True
    
    # Enable drag and drop
    enable_drag_drop: bool = True
    
    # Enable keyboard navigation
    keyboard_navigation: bool = True
    
    # High DPI scaling
    high_dpi_scaling: bool = True
    
    # Window width
    window_width: int = 800
    
    # Window height
    window_height: int = 600


@dataclass
class ExerciseSettings:
    """Settings for exercise generation and presentation."""
    # Number of exercises per session
    exercises_per_session: int = 20
    
    # Enable hints
    enable_hints: bool = True
    
    # Hint levels: 1-5 (how many hints before showing answer)
    max_hint_level: int = 5
    
    # Show explanations after each exercise
    show_explanations: bool = True
    
    # Explanation detail level: 'brief', 'standard', 'detailed'
    explanation_detail: str = "standard"
    
    # Enable immediate feedback
    immediate_feedback: bool = True
    
    # Enable response time tracking
    track_response_time: bool = True
    
    # Enable confidence tracking
    track_confidence: bool = True
    
    # Auto-advance after correct answer (seconds)
    auto_advance_delay: float = 1.5


@dataclass
class StatisticsSettings:
    """Settings for statistics and analytics."""
    # Enable statistics collection
    enable_statistics: bool = True
    
    # Show dashboard on startup
    show_dashboard_startup: bool = False
    
    # Statistics retention days
    retention_days: int = 365
    
    # Export statistics format: 'csv', 'json', or 'both'
    export_format: str = "json"


@dataclass
class AccessibilitySettings:
    """Accessibility settings."""
    # Enable screen reader support
    screen_reader_support: bool = True
    
    # High contrast mode
    high_contrast: bool = False
    
    # Color scheme for colorblind users
    colorblind_mode: str = "none"  # 'none', 'deuteranopia', 'protanopia', 'tritanopia'
    
    # Minimum button size
    min_button_size: int = 40


@dataclass
class CustomExerciseSettings:
    """Settings for custom exercise creation."""
    # Enable custom exercise builder
    enable_custom_builder: bool = True
    
    # Default exercise type for custom exercises
    default_exercise_type: str = "sentence_builder"
    
    # Auto-save custom exercises
    auto_save_custom: bool = True


@dataclass
class Settings:
    """
    Main settings class for Grammar Pro.
    
    Manages all configuration options with defaults and persistence.
    """
    
    grammar: GrammarSettings = field(default_factory=GrammarSettings)
    ui: UISettings = field(default_factory=UISettings)
    exercise: ExerciseSettings = field(default_factory=ExerciseSettings)
    statistics: StatisticsSettings = field(default_factory=StatisticsSettings)
    accessibility: AccessibilitySettings = field(default_factory=AccessibilitySettings)
    custom: CustomExerciseSettings = field(default_factory=CustomExerciseSettings)
    
    # Internal: has been loaded from disk
    _loaded: bool = False
    
    # Internal: config file path
    _config_path: Optional[Path] = None
    
    def __post_init__(self):
        """Initialize settings after creation."""
        # Convert nested dicts to dataclasses if loaded from JSON
        if not self._loaded:
            self._ensure_dataclasses()
    
    def _ensure_dataclasses(self):
        """Ensure all nested settings are proper dataclass instances."""
        if not isinstance(self.grammar, GrammarSettings):
            self.grammar = GrammarSettings(**self.grammar) if isinstance(self.grammar, dict) else GrammarSettings()
        if not isinstance(self.ui, UISettings):
            self.ui = UISettings(**self.ui) if isinstance(self.ui, dict) else UISettings()
        if not isinstance(self.exercise, ExerciseSettings):
            self.exercise = ExerciseSettings(**self.exercise) if isinstance(self.exercise, dict) else ExerciseSettings()
        if not isinstance(self.statistics, StatisticsSettings):
            self.statistics = StatisticsSettings(**self.statistics) if isinstance(self.statistics, dict) else StatisticsSettings()
        if not isinstance(self.accessibility, AccessibilitySettings):
            self.accessibility = AccessibilitySettings(**self.accessibility) if isinstance(self.accessibility, dict) else AccessibilitySettings()
        if not isinstance(self.custom, CustomExerciseSettings):
            self.custom = CustomExerciseSettings(**self.custom) if isinstance(self.custom, dict) else CustomExerciseSettings()
    
    @property
    def config_path(self) -> Path:
        """Get the configuration file path."""
        if self._config_path is None:
            # Get Anki's addon directory
            from anki.utils import getAddonPath
            addon_dir = Path(getAddonPath(__name__.split('.')[0]))
            self._config_path = addon_dir / "config.json"
        return self._config_path
    
    def load(self) -> None:
        """Load settings from configuration file."""
        if self._config_path and self._config_path.exists():
            try:
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._load_from_dict(data)
                self._loaded = True
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # If loading fails, use defaults
                print(f"Warning: Could not load settings: {e}")
                self._loaded = False
        else:
            self._loaded = False
    
    def _load_from_dict(self, data: Dict[str, Any]) -> None:
        """Load settings from a dictionary."""
        if 'grammar' in data:
            self.grammar = GrammarSettings(**data['grammar'])
        if 'ui' in data:
            self.ui = UISettings(**data['ui'])
        if 'exercise' in data:
            self.exercise = ExerciseSettings(**data['exercise'])
        if 'statistics' in data:
            self.statistics = StatisticsSettings(**data['statistics'])
        if 'accessibility' in data:
            self.accessibility = AccessibilitySettings(**data['accessibility'])
        if 'custom' in data:
            self.custom = CustomExerciseSettings(**data['custom'])
    
    def save(self) -> None:
        """Save settings to configuration file."""
        data = self.to_dict()
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to a dictionary for serialization."""
        return {
            'grammar': self.grammar.__dict__,
            'ui': self.ui.__dict__,
            'exercise': self.exercise.__dict__,
            'statistics': self.statistics.__dict__,
            'accessibility': self.accessibility.__dict__,
            'custom': self.custom.__dict__,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Settings':
        """Create Settings instance from a dictionary."""
        settings = cls()
        settings._load_from_dict(data)
        settings._loaded = True
        return settings
    
    def get(self, *keys, default=None) -> Any:
        """
        Get a nested setting value by keys.
        
        Example: settings.get('ui', 'theme') returns the theme setting.
        """
        current = self
        for key in keys:
            if hasattr(current, key):
                current = getattr(current, key)
            elif isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def set(self, *keys, value: Any) -> None:
        """
        Set a nested setting value by keys.
        
        Example: settings.set('ui', 'theme', 'dark')
        """
        if not keys:
            return
        
        # Navigate to the parent
        current = self
        for key in keys[:-1]:
            if hasattr(current, key):
                current = getattr(current, key)
            else:
                return
        
        # Set the final key
        final_key = keys[-1]
        if hasattr(current, final_key):
            setattr(current, final_key, value)
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to their default values."""
        self.grammar = GrammarSettings()
        self.ui = UISettings()
        self.exercise = ExerciseSettings()
        self.statistics = StatisticsSettings()
        self.accessibility = AccessibilitySettings()
        self.custom = CustomExerciseSettings()
        self._loaded = True
