"""
Main Window for Grammar Pro.

The primary window that users interact with to access all features.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QStackedWidget,
    QFrame,
    QSizePolicy,
)

if TYPE_CHECKING:
    from ..core.addon_manager import AddonManager


class MainWindow(QMainWindow):
    """
    Main window for Grammar Pro.
    
    Provides access to all exercise modes, statistics, and settings.
    """
    
    # Signals
    mode_selected = pyqtSignal(str)
    language_changed = pyqtSignal(str)
    settings_requested = pyqtSignal()
    dashboard_requested = pyqtSignal()
    exercise_builder_requested = pyqtSignal()
    
    def __init__(self, addon_manager: 'AddonManager', parent: QWidget = None):
        """
        Initialize the main window.
        
        Args:
            addon_manager: Addon manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.addon_manager = addon_manager
        self.settings = addon_manager.settings
        
        # Window setup
        self.setWindowTitle("Grammar Pro")
        self.setMinimumSize(QSize(800, 600))
        
        # Apply settings
        self._apply_settings()
        
        # Create UI
        self._create_menu()
        self._create_widgets()
        self._create_layout()
        
        # Connect signals
        self._connect_signals()
        
        # Load data
        self._load_data()
    
    def _apply_settings(self) -> None:
        """Apply settings to the window."""
        if self.settings:
            # Apply theme
            if self.settings.ui.theme == "dark":
                self._apply_dark_theme()
            elif self.settings.ui.theme == "light":
                self._apply_light_theme()
            
            # Apply font
            if self.settings.ui.font_family:
                font = QFont(self.settings.ui.font_family, self.settings.ui.font_size)
                self.setFont(font)
            
            # Apply window size
            if self.settings.ui.window_width > 0 and self.settings.ui.window_height > 0:
                self.resize(self.settings.ui.window_width, self.settings.ui.window_height)
    
    def _apply_dark_theme(self) -> None:
        """Apply dark theme stylesheet."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
            QPushButton:pressed {
                background-color: #2c2c2c;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #e0e0e0;
            }
            QFrame {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 4px;
            }
        """)
    
    def _apply_light_theme(self) -> None:
        """Apply light theme stylesheet."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                color: #333;
            }
            QWidget {
                background-color: #f0f0f0;
                color: #333;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #ccc;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QComboBox {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 4px;
            }
            QFrame {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
    
    def _create_menu(self) -> None:
        """Create the menu bar."""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self._show_settings)
        file_menu.addAction(settings_action)
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        
        # Dashboard action
        dashboard_action = QAction("Dashboard", self)
        dashboard_action.triggered.connect(self._show_dashboard)
        view_menu.addAction(dashboard_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        # About action
        about_action = QAction("About Grammar Pro", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_widgets(self) -> None:
        """Create all widgets."""
        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Header
        self.header_label = QLabel("Grammar Pro")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        self.header_label.setFont(header_font)
        
        # Subtitle
        self.subtitle_label = QLabel("Learn sentence construction through thousands of small grammar decisions")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        self.subtitle_label.setFont(subtitle_font)
        
        # Controls
        self.controls_frame = QFrame()
        self.controls_layout = QHBoxLayout(self.controls_frame)
        self.controls_layout.setContentsMargins(10, 10, 10, 10)
        self.controls_layout.setSpacing(15)
        
        # Language selector
        self.language_label = QLabel("Language:")
        self.language_combo = QComboBox()
        self._populate_language_combo()
        
        # Mode selector
        self.mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self._populate_mode_combo()
        
        # Start button
        self.start_button = QPushButton("Start Exercise")
        self.start_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Quick start buttons
        self.quick_start_frame = QFrame()
        self.quick_start_layout = QHBoxLayout(self.quick_start_frame)
        self.quick_start_layout.setContentsMargins(10, 10, 10, 10)
        self.quick_start_layout.setSpacing(10)
        
        # Add quick start buttons for each mode
        self.quick_start_buttons = {}
        modes = self.addon_manager.get_available_modes()
        for mode in modes[:5]:  # Show first 5 modes as quick start
            button = QPushButton(mode['name'])
            button.setProperty("mode_id", mode['id'])
            button.clicked.connect(self._on_quick_start_clicked)
            self.quick_start_buttons[mode['id']] = button
            self.quick_start_layout.addWidget(button)
        
        # Statistics summary
        self.stats_frame = QFrame()
        self.stats_layout = QHBoxLayout(self.stats_frame)
        self.stats_layout.setContentsMargins(15, 15, 15, 15)
        self.stats_layout.setSpacing(20)
        
        # Create stat labels
        self.total_exercises_label = QLabel("Total Exercises: 0")
        self.accuracy_label = QLabel("Accuracy: 0%")
        self.mastery_label = QLabel("Mastery: 0%")
        
        self.stats_layout.addWidget(self.total_exercises_label)
        self.stats_layout.addWidget(self.accuracy_label)
        self.stats_layout.addWidget(self.mastery_label)
        
        # Stacked widget for different views
        self.stacked_widget = QStackedWidget()
        
        # Main view (default)
        self.main_view = QWidget()
        self._create_main_view()
        
        # Add views to stacked widget
        self.stacked_widget.addWidget(self.main_view)
        
        # Add to main layout
        self.main_layout.addWidget(self.header_label)
        self.main_layout.addWidget(self.subtitle_label)
        self.main_layout.addWidget(self.controls_frame)
        self.main_layout.addWidget(self.quick_start_frame)
        self.main_layout.addWidget(self.stats_frame)
        self.main_layout.addWidget(self.stacked_widget, 1)  # Take remaining space
    
    def _create_main_view(self) -> None:
        """Create the main view."""
        layout = QVBoxLayout(self.main_view)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Description
        description_label = QLabel("""
        <p><b>Welcome to Grammar Pro!</b></p>
        <p>Grammar Pro is a comprehensive Anki addon for learning sentence construction and grammar.</p>
        <p>Instead of memorizing complete sentences, you'll learn how to THINK when building a sentence through thousands of small grammar decisions.</p>
        <p>Choose a language and mode above, then click "Start Exercise" to begin.</p>
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description_label)
        
        # Features list
        features_label = QLabel("""
        <p><b>Features:</b></p>
        <ul>
            <li>10 different exercise modes</li>
            <li>14 progressive difficulty levels</li>
            <li>Adaptive learning based on your performance</li>
            <li>Detailed statistics and progress tracking</li>
            <li>Custom exercise builder</li>
            <li>Support for multiple languages (starting with Danish)</li>
        </ul>
        """)
        features_label.setWordWrap(True)
        layout.addWidget(features_label)
        
        layout.addStretch()
    
    def _create_layout(self) -> None:
        """Create the main layout."""
        # Add controls to layout
        self.controls_layout.addWidget(self.language_label)
        self.controls_layout.addWidget(self.language_combo)
        self.controls_layout.addWidget(self.mode_label)
        self.controls_layout.addWidget(self.mode_combo)
        self.controls_layout.addWidget(self.start_button)
    
    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        self.start_button.clicked.connect(self._start_exercise)
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)
    
    def _load_data(self) -> None:
        """Load initial data."""
        # Update statistics
        self._update_statistics()
    
    def _populate_language_combo(self) -> None:
        """Populate the language combo box."""
        languages = self.addon_manager.get_available_languages()
        
        for lang in languages:
            self.language_combo.addItem(lang['name'], lang['code'])
        
        # Set default language
        default_lang = self.settings.grammar.default_language if self.settings else "da"
        index = self.language_combo.findData(default_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
    
    def _populate_mode_combo(self) -> None:
        """Populate the mode combo box."""
        modes = self.addon_manager.get_available_modes()
        
        for mode in modes:
            self.mode_combo.addItem(mode['name'], mode['id'])
        
        # Set default mode
        if self.mode_combo.count() > 0:
            self.mode_combo.setCurrentIndex(0)
    
    def _update_statistics(self) -> None:
        """Update the statistics display."""
        summary = self.addon_manager.get_statistics_summary()
        
        total_exercises = summary.get('total_exercises', 0)
        accuracy = summary.get('accuracy', 0.0)
        mastery = summary.get('completion_percentage', 0.0)
        
        self.total_exercises_label.setText(f"Total Exercises: {total_exercises}")
        self.accuracy_label.setText(f"Accuracy: {accuracy:.1%}")
        self.mastery_label.setText(f"Mastery: {mastery:.0f}%")
    
    def _start_exercise(self) -> None:
        """Start a new exercise."""
        language = self.language_combo.currentData()
        mode = self.mode_combo.currentData()
        
        if language and mode:
            self.addon_manager.start_exercise_session(mode, language)
    
    def _on_quick_start_clicked(self) -> None:
        """Handle quick start button click."""
        button = self.sender()
        if isinstance(button, QPushButton):
            mode_id = button.property("mode_id")
            language = self.language_combo.currentData()
            
            if mode_id and language:
                self.addon_manager.start_exercise_session(mode_id, language)
    
    def _on_language_changed(self, text: str) -> None:
        """Handle language change."""
        language_code = self.language_combo.currentData()
        self.language_changed.emit(language_code)
    
    def _on_mode_changed(self, text: str) -> None:
        """Handle mode change."""
        mode_id = self.mode_combo.currentData()
        self.mode_selected.emit(mode_id)
    
    def _show_settings(self) -> None:
        """Show the settings dialog."""
        self.settings_requested.emit()
    
    def _show_dashboard(self) -> None:
        """Show the dashboard."""
        self.dashboard_requested.emit()
    
    def _show_about(self) -> None:
        """Show the about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        
        about_text = """
        <h2>Grammar Pro</h2>
        <p>Version 1.0.0</p>
        <p>A comprehensive Anki addon for learning sentence construction and grammar.</p>
        <p>Teaches language learners how to THINK when building sentences through thousands of small grammar decisions.</p>
        <p>&copy; 2024 Grammar Pro Team</p>
        """
        
        QMessageBox.about(self, "About Grammar Pro", about_text)
    
    def showEvent(self, event: Any) -> None:
        """Handle show event."""
        super().showEvent(event)
        self._update_statistics()
    
    def closeEvent(self, event: Any) -> None:
        """Handle close event."""
        # Save settings
        if self.settings:
            # Save window size
            size = self.size()
            self.settings.ui.window_width = size.width()
            self.settings.ui.window_height = size.height()
            self.settings.save()
        
        super().closeEvent(event)
