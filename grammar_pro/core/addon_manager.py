"""
Addon Manager for Grammar Pro.

Central class that manages all addon components and coordinates between them.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..grammar.grammar_engine import GrammarEngine
    from ..exercises.exercise_manager import ExerciseManager
    from ..statistics.statistics_manager import StatisticsManager
    from ..ui.main_window import MainWindow
    from ..persistence.data_manager import DataManager
    from ..config.settings import Settings


class AddonManager:
    """
    Central manager for the Grammar Pro addon.
    
    Coordinates all components:
    - Grammar Engine
    - Exercise Manager
    - Statistics Manager
    - UI Manager
    - Data Manager
    - Settings
    
    Provides a unified interface for the addon's functionality.
    """
    
    def __init__(self):
        """Initialize the Addon Manager."""
        self._initialized = False
        self._grammar_engine: Optional['GrammarEngine'] = None
        self._exercise_manager: Optional['ExerciseManager'] = None
        self._statistics_manager: Optional['StatisticsManager'] = None
        self._data_manager: Optional['DataManager'] = None
        self._settings: Optional['Settings'] = None
        self._main_window: Optional['MainWindow'] = None
        
        self._components: Dict[str, Any] = {}
    
    def initialize(self) -> None:
        """
        Initialize all addon components.
        
        This should be called when the addon is loaded by Anki.
        """
        if self._initialized:
            return
        
        # Import and initialize components
        from ..config.settings import Settings
        from ..persistence.data_manager import DataManager
        from ..grammar.grammar_engine import GrammarEngine
        from ..exercises.exercise_manager import ExerciseManager
        from ..statistics.statistics_manager import StatisticsManager
        
        # Initialize settings first (other components may need them)
        self._settings = Settings()
        self._settings.load()
        
        # Initialize data manager
        self._data_manager = DataManager(self._settings)
        
        # Initialize grammar engine
        self._grammar_engine = GrammarEngine(self._settings)
        
        # Initialize exercise manager
        self._exercise_manager = ExerciseManager(
            self._grammar_engine, 
            self._settings
        )
        
        # Initialize statistics manager
        self._statistics_manager = StatisticsManager(
            self._data_manager,
            self._settings
        )
        
        # Register components
        self._components = {
            'settings': self._settings,
            'data_manager': self._data_manager,
            'grammar_engine': self._grammar_engine,
            'exercise_manager': self._exercise_manager,
            'statistics_manager': self._statistics_manager,
        }
        
        self._initialized = True
    
    def shutdown(self) -> None:
        """
        Shutdown all addon components.
        
        This should be called when Anki is closing.
        """
        if not self._initialized:
            return
        
        # Save settings
        if self._settings:
            self._settings.save()
        
        # Shutdown components in reverse order
        if self._statistics_manager:
            self._statistics_manager.shutdown()
        if self._exercise_manager:
            self._exercise_manager.shutdown()
        if self._grammar_engine:
            self._grammar_engine.shutdown()
        if self._data_manager:
            self._data_manager.shutdown()
        
        self._initialized = False
    
    @property
    def is_initialized(self) -> bool:
        """Check if the addon is initialized."""
        return self._initialized
    
    @property
    def settings(self) -> 'Settings':
        """Get the settings instance."""
        if not self._initialized:
            self.initialize()
        return self._settings
    
    @property
    def grammar_engine(self) -> 'GrammarEngine':
        """Get the grammar engine instance."""
        if not self._initialized:
            self.initialize()
        return self._grammar_engine
    
    @property
    def exercise_manager(self) -> 'ExerciseManager':
        """Get the exercise manager instance."""
        if not self._initialized:
            self.initialize()
        return self._exercise_manager
    
    @property
    def statistics_manager(self) -> 'StatisticsManager':
        """Get the statistics manager instance."""
        if not self._initialized:
            self.initialize()
        return self._statistics_manager
    
    @property
    def data_manager(self) -> 'DataManager':
        """Get the data manager instance."""
        if not self._initialized:
            self.initialize()
        return self._data_manager
    
    @property
    def main_window(self) -> Optional['MainWindow']:
        """Get the main window instance."""
        return self._main_window
    
    @main_window.setter
    def main_window(self, window: 'MainWindow') -> None:
        """Set the main window instance."""
        self._main_window = window
    
    def get_component(self, name: str) -> Any:
        """
        Get a component by name.
        
        Args:
            name: Component name ('settings', 'grammar_engine', etc.)
            
        Returns:
            The component instance, or None if not found.
        """
        return self._components.get(name)
    
    def show_main_window(self) -> None:
        """Show the main Grammar Pro window."""
        if self._main_window is None:
            from ..ui.main_window import MainWindow
            self._main_window = MainWindow(self)
        
        self._main_window.show()
        self._main_window.raise_()
        self._main_window.activateWindow()
    
    def show_dashboard(self) -> None:
        """Show the statistics dashboard."""
        from ..ui.dashboard import DashboardWindow
        dashboard = DashboardWindow(self)
        dashboard.show()
    
    def show_settings_dialog(self) -> None:
        """Show the settings dialog."""
        from ..ui.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def show_exercise_builder(self) -> None:
        """Show the custom exercise builder."""
        from ..ui.exercise_builder import ExerciseBuilderWindow
        builder = ExerciseBuilderWindow(self)
        builder.show()
    
    def start_exercise_session(self, mode: str, language: str = None) -> None:
        """
        Start an exercise session.
        
        Args:
            mode: Exercise mode identifier
            language: Language code (optional, uses default if not specified)
        """
        if language is None:
            language = self.settings.grammar.default_language
        
        from ..ui.exercise_window import ExerciseWindow
        window = ExerciseWindow(self, mode, language)
        window.show()
    
    def get_available_modes(self) -> List[Dict[str, Any]]:
        """
        Get list of available exercise modes.
        
        Returns:
            List of mode descriptors with id, name, description, etc.
        """
        return self.exercise_manager.get_available_modes()
    
    def get_available_languages(self) -> List[Dict[str, Any]]:
        """
        Get list of available languages.
        
        Returns:
            List of language descriptors with code, name, etc.
        """
        return self.grammar_engine.get_available_languages()
    
    def get_statistics_summary(self) -> Dict[str, Any]:
        """
        Get a summary of user statistics.
        
        Returns:
            Dictionary with statistics summary.
        """
        return self.statistics_manager.get_summary()
    
    def get_weak_areas(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the user's weakest grammar areas.
        
        Args:
            limit: Maximum number of weak areas to return
            
        Returns:
            List of weak area descriptors.
        """
        return self.statistics_manager.get_weak_areas(limit)
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """
        Get the user's learning progress.
        
        Returns:
            Dictionary with progress information.
        """
        return self.statistics_manager.get_learning_progress()
