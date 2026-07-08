"""
Settings Dialog for Grammar Pro.

Dialog for configuring addon settings.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QTabWidget,
    QFrame,
    QFormLayout,
    QDialogButtonBox,
)

if TYPE_CHECKING:
    from ..core.addon_manager import AddonManager


class SettingsDialog(QDialog):
    """
    Settings Dialog for Grammar Pro.
    
    Allows users to configure all addon settings.
    """
    
    def __init__(self, addon_manager: 'AddonManager', parent: QWidget = None):
        """
        Initialize the settings dialog.
        
        Args:
            addon_manager: Addon manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.addon_manager = addon_manager
        self.settings = addon_manager.settings
        
        # Window setup
        self.setWindowTitle("Grammar Pro - Settings")
        self.setMinimumSize(QSize(600, 500))
        
        # Apply settings
        self._apply_settings()
        
        # Create UI
        self._create_widgets()
        self._create_layout()
        self._connect_signals()
        
        # Load settings
        self._load_settings()
    
    def _apply_settings(self) -> None:
        """Apply settings to the dialog."""
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
    
    def _apply_dark_theme(self) -> None:
        """Apply dark theme stylesheet."""
        self.setStyleSheet("""
            QDialog {
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
            QComboBox {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
            }
            QCheckBox {
                spacing: 8px;
            }
            QTabWidget::pane {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: #e0e0e0;
                padding: 8px 16px;
            }
            QTabBar::tab:selected {
                background-color: #4c4c4c;
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
            QDialog {
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
            QComboBox {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 4px;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 4px;
            }
            QCheckBox {
                spacing: 8px;
            }
            QTabWidget::pane {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #ffffff;
                color: #333;
                padding: 8px 16px;
            }
            QTabBar::tab:selected {
                background-color: #e0e0e0;
            }
            QFrame {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
    
    def _create_widgets(self) -> None:
        """Create all widgets."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Header
        self.header_label = QLabel("Grammar Pro Settings")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        self.header_label.setFont(header_font)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # General tab
        self.general_tab = QWidget()
        self._create_general_tab()
        
        # Grammar tab
        self.grammar_tab = QWidget()
        self._create_grammar_tab()
        
        # Exercise tab
        self.exercise_tab = QWidget()
        self._create_exercise_tab()
        
        # UI tab
        self.ui_tab = QWidget()
        self._create_ui_tab()
        
        # Statistics tab
        self.statistics_tab = QWidget()
        self._create_statistics_tab()
        
        # Accessibility tab
        self.accessibility_tab = QWidget()
        self._create_accessibility_tab()
        
        # Add tabs
        self.tab_widget.addTab(self.general_tab, "General")
        self.tab_widget.addTab(self.grammar_tab, "Grammar")
        self.tab_widget.addTab(self.exercise_tab, "Exercise")
        self.tab_widget.addTab(self.ui_tab, "UI")
        self.tab_widget.addTab(self.statistics_tab, "Statistics")
        self.tab_widget.addTab(self.accessibility_tab, "Accessibility")
        
        # Button box
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Apply
        )
        
        # Add to main layout
        self.main_layout.addWidget(self.header_label)
        self.main_layout.addWidget(self.tab_widget, 1)
        self.main_layout.addWidget(self.button_box)
    
    def _create_layout(self) -> None:
        """Create the layout."""
        pass  # Layout is created in _create_widgets
    
    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.clicked.connect(self._on_button_clicked)
    
    def _create_general_tab(self) -> None:
        """Create the general settings tab."""
        layout = QVBoxLayout(self.general_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Default language
        self.default_language_label = QLabel("Default Language:")
        self.default_language_combo = QComboBox()
        languages = self.addon_manager.get_available_languages()
        for lang in languages:
            self.default_language_combo.addItem(lang['name'], lang['code'])
        
        form_layout.addRow(self.default_language_label, self.default_language_combo)
        
        # Add to main layout
        layout.addLayout(form_layout)
        layout.addStretch()
    
    def _create_grammar_tab(self) -> None:
        """Create the grammar settings tab."""
        layout = QVBoxLayout(self.grammar_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Adaptive learning
        self.adaptive_learning_check = QCheckBox()
        form_layout.addRow(QLabel("Enable Adaptive Learning:"), self.adaptive_learning_check)
        
        # Weak area exercises
        self.weak_area_exercises_spin = QSpinBox()
        self.weak_area_exercises_spin.setRange(10, 100)
        form_layout.addRow(QLabel("Weak Area Exercises:"), self.weak_area_exercises_spin)
        
        # Mastery threshold
        self.mastery_threshold_spin = QDoubleSpinBox()
        self.mastery_threshold_spin.setRange(0.5, 1.0)
        self.mastery_threshold_spin.setSingleStep(0.05)
        form_layout.addRow(QLabel("Mastery Threshold:"), self.mastery_threshold_spin)
        
        # Progressive difficulty
        self.progressive_difficulty_check = QCheckBox()
        form_layout.addRow(QLabel("Progressive Difficulty:"), self.progressive_difficulty_check)
        
        # Current level
        self.current_level_spin = QSpinBox()
        self.current_level_spin.setRange(1, 14)
        form_layout.addRow(QLabel("Current Level:"), self.current_level_spin)
        
        # Add to main layout
        layout.addLayout(form_layout)
        layout.addStretch()
    
    def _create_exercise_tab(self) -> None:
        """Create the exercise settings tab."""
        layout = QVBoxLayout(self.exercise_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Exercises per session
        self.exercises_per_session_spin = QSpinBox()
        self.exercises_per_session_spin.setRange(5, 100)
        form_layout.addRow(QLabel("Exercises per Session:"), self.exercises_per_session_spin)
        
        # Enable hints
        self.enable_hints_check = QCheckBox()
        form_layout.addRow(QLabel("Enable Hints:"), self.enable_hints_check)
        
        # Max hint level
        self.max_hint_level_spin = QSpinBox()
        self.max_hint_level_spin.setRange(1, 5)
        form_layout.addRow(QLabel("Max Hint Level:"), self.max_hint_level_spin)
        
        # Show explanations
        self.show_explanations_check = QCheckBox()
        form_layout.addRow(QLabel("Show Explanations:"), self.show_explanations_check)
        
        # Explanation detail
        self.explanation_detail_combo = QComboBox()
        self.explanation_detail_combo.addItems(["Brief", "Standard", "Detailed"])
        form_layout.addRow(QLabel("Explanation Detail:"), self.explanation_detail_combo)
        
        # Immediate feedback
        self.immediate_feedback_check = QCheckBox()
        form_layout.addRow(QLabel("Immediate Feedback:"), self.immediate_feedback_check)
        
        # Track response time
        self.track_response_time_check = QCheckBox()
        form_layout.addRow(QLabel("Track Response Time:"), self.track_response_time_check)
        
        # Track confidence
        self.track_confidence_check = QCheckBox()
        form_layout.addRow(QLabel("Track Confidence:"), self.track_confidence_check)
        
        # Auto-advance delay
        self.auto_advance_spin = QDoubleSpinBox()
        self.auto_advance_spin.setRange(0.5, 5.0)
        self.auto_advance_spin.setSingleStep(0.5)
        form_layout.addRow(QLabel("Auto-advance Delay (s):"), self.auto_advance_spin)
        
        # Add to main layout
        layout.addLayout(form_layout)
        layout.addStretch()
    
    def _create_ui_tab(self) -> None:
        """Create the UI settings tab."""
        layout = QVBoxLayout(self.ui_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Light", "Dark"])
        form_layout.addRow(QLabel("Theme:"), self.theme_combo)
        
        # Font family
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(["Default", "Arial", "Times New Roman", "Courier New"])
        form_layout.addRow(QLabel("Font Family:"), self.font_family_combo)
        
        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        form_layout.addRow(QLabel("Font Size:"), self.font_size_spin)
        
        # Keyboard shortcuts
        self.keyboard_shortcuts_check = QCheckBox()
        form_layout.addRow(QLabel("Enable Keyboard Shortcuts:"), self.keyboard_shortcuts_check)
        
        # Drag and drop
        self.enable_drag_drop_check = QCheckBox()
        form_layout.addRow(QLabel("Enable Drag and Drop:"), self.enable_drag_drop_check)
        
        # Keyboard navigation
        self.keyboard_navigation_check = QCheckBox()
        form_layout.addRow(QLabel("Enable Keyboard Navigation:"), self.keyboard_navigation_check)
        
        # High DPI scaling
        self.high_dpi_check = QCheckBox()
        form_layout.addRow(QLabel("High DPI Scaling:"), self.high_dpi_check)
        
        # Add to main layout
        layout.addLayout(form_layout)
        layout.addStretch()
    
    def _create_statistics_tab(self) -> None:
        """Create the statistics settings tab."""
        layout = QVBoxLayout(self.statistics_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Enable statistics
        self.enable_statistics_check = QCheckBox()
        form_layout.addRow(QLabel("Enable Statistics Collection:"), self.enable_statistics_check)
        
        # Show dashboard on startup
        self.show_dashboard_startup_check = QCheckBox()
        form_layout.addRow(QLabel("Show Dashboard on Startup:"), self.show_dashboard_startup_check)
        
        # Retention days
        self.retention_days_spin = QSpinBox()
        self.retention_days_spin.setRange(7, 3650)
        form_layout.addRow(QLabel("Statistics Retention (days):"), self.retention_days_spin)
        
        # Export format
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["JSON", "CSV", "Both"])
        form_layout.addRow(QLabel("Export Format:"), self.export_format_combo)
        
        # Add to main layout
        layout.addLayout(form_layout)
        layout.addStretch()
    
    def _create_accessibility_tab(self) -> None:
        """Create the accessibility settings tab."""
        layout = QVBoxLayout(self.accessibility_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Screen reader support
        self.screen_reader_check = QCheckBox()
        form_layout.addRow(QLabel("Enable Screen Reader Support:"), self.screen_reader_check)
        
        # High contrast
        self.high_contrast_check = QCheckBox()
        form_layout.addRow(QLabel("High Contrast Mode:"), self.high_contrast_check)
        
        # Colorblind mode
        self.colorblind_combo = QComboBox()
        self.colorblind_combo.addItems(["None", "Deuteranopia", "Protanopia", "Tritanopia"])
        form_layout.addRow(QLabel("Colorblind Mode:"), self.colorblind_combo)
        
        # Minimum button size
        self.min_button_size_spin = QSpinBox()
        self.min_button_size_spin.setRange(20, 100)
        form_layout.addRow(QLabel("Minimum Button Size:"), self.min_button_size_spin)
        
        # Add to main layout
        layout.addLayout(form_layout)
        layout.addStretch()
    
    def _load_settings(self) -> None:
        """Load settings from the settings object."""
        if not self.settings:
            return
        
        # General settings
        if hasattr(self.settings, 'grammar'):
            default_lang = self.settings.grammar.default_language
            index = self.default_language_combo.findData(default_lang)
            if index >= 0:
                self.default_language_combo.setCurrentIndex(index)
        
        # Grammar settings
        if hasattr(self.settings, 'grammar'):
            self.adaptive_learning_check.setChecked(self.settings.grammar.adaptive_learning)
            self.weak_area_exercises_spin.setValue(self.settings.grammar.weak_area_exercises)
            self.mastery_threshold_spin.setValue(self.settings.grammar.mastery_threshold)
            self.progressive_difficulty_check.setChecked(self.settings.grammar.progressive_difficulty)
            self.current_level_spin.setValue(self.settings.grammar.current_level)
        
        # Exercise settings
        if hasattr(self.settings, 'exercise'):
            self.exercises_per_session_spin.setValue(self.settings.exercise.exercises_per_session)
            self.enable_hints_check.setChecked(self.settings.exercise.enable_hints)
            self.max_hint_level_spin.setValue(self.settings.exercise.max_hint_level)
            self.show_explanations_check.setChecked(self.settings.exercise.show_explanations)
            
            # Map explanation detail
            detail = self.settings.exercise.explanation_detail
            if detail == "brief":
                self.explanation_detail_combo.setCurrentIndex(0)
            elif detail == "standard":
                self.explanation_detail_combo.setCurrentIndex(1)
            else:
                self.explanation_detail_combo.setCurrentIndex(2)
            
            self.immediate_feedback_check.setChecked(self.settings.exercise.immediate_feedback)
            self.track_response_time_check.setChecked(self.settings.exercise.track_response_time)
            self.track_confidence_check.setChecked(self.settings.exercise.track_confidence)
            self.auto_advance_spin.setValue(self.settings.exercise.auto_advance_delay)
        
        # UI settings
        if hasattr(self.settings, 'ui'):
            # Map theme
            theme = self.settings.ui.theme
            if theme == "system":
                self.theme_combo.setCurrentIndex(0)
            elif theme == "light":
                self.theme_combo.setCurrentIndex(1)
            else:
                self.theme_combo.setCurrentIndex(2)
            
            # Font family
            font_family = self.settings.ui.font_family
            index = self.font_family_combo.findText(font_family if font_family else "Default")
            if index >= 0:
                self.font_family_combo.setCurrentIndex(index)
            
            self.font_size_spin.setValue(self.settings.ui.font_size)
            self.keyboard_shortcuts_check.setChecked(self.settings.ui.keyboard_shortcuts)
            self.enable_drag_drop_check.setChecked(self.settings.ui.enable_drag_drop)
            self.keyboard_navigation_check.setChecked(self.settings.ui.keyboard_navigation)
            self.high_dpi_check.setChecked(self.settings.ui.high_dpi_scaling)
        
        # Statistics settings
        if hasattr(self.settings, 'statistics'):
            self.enable_statistics_check.setChecked(self.settings.statistics.enable_statistics)
            self.show_dashboard_startup_check.setChecked(self.settings.statistics.show_dashboard_startup)
            self.retention_days_spin.setValue(self.settings.statistics.retention_days)
            
            # Map export format
            fmt = self.settings.statistics.export_format
            if fmt == "csv":
                self.export_format_combo.setCurrentIndex(0)
            elif fmt == "json":
                self.export_format_combo.setCurrentIndex(1)
            else:
                self.export_format_combo.setCurrentIndex(2)
        
        # Accessibility settings
        if hasattr(self.settings, 'accessibility'):
            self.screen_reader_check.setChecked(self.settings.accessibility.screen_reader_support)
            self.high_contrast_check.setChecked(self.settings.accessibility.high_contrast)
            
            # Map colorblind mode
            mode = self.settings.accessibility.colorblind_mode
            if mode == "none":
                self.colorblind_combo.setCurrentIndex(0)
            elif mode == "deuteranopia":
                self.colorblind_combo.setCurrentIndex(1)
            elif mode == "protanopia":
                self.colorblind_combo.setCurrentIndex(2)
            else:
                self.colorblind_combo.setCurrentIndex(3)
            
            self.min_button_size_spin.setValue(self.settings.accessibility.min_button_size)
    
    def _save_settings(self) -> None:
        """Save settings to the settings object."""
        if not self.settings:
            return
        
        # General settings
        if hasattr(self.settings, 'grammar'):
            self.settings.grammar.default_language = self.default_language_combo.currentData()
        
        # Grammar settings
        if hasattr(self.settings, 'grammar'):
            self.settings.grammar.adaptive_learning = self.adaptive_learning_check.isChecked()
            self.settings.grammar.weak_area_exercises = self.weak_area_exercises_spin.value()
            self.settings.grammar.mastery_threshold = self.mastery_threshold_spin.value()
            self.settings.grammar.progressive_difficulty = self.progressive_difficulty_check.isChecked()
            self.settings.grammar.current_level = self.current_level_spin.value()
        
        # Exercise settings
        if hasattr(self.settings, 'exercise'):
            self.settings.exercise.exercises_per_session = self.exercises_per_session_spin.value()
            self.settings.exercise.enable_hints = self.enable_hints_check.isChecked()
            self.settings.exercise.max_hint_level = self.max_hint_level_spin.value()
            self.settings.exercise.show_explanations = self.show_explanations_check.isChecked()
            
            # Map explanation detail
            index = self.explanation_detail_combo.currentIndex()
            if index == 0:
                self.settings.exercise.explanation_detail = "brief"
            elif index == 1:
                self.settings.exercise.explanation_detail = "standard"
            else:
                self.settings.exercise.explanation_detail = "detailed"
            
            self.settings.exercise.immediate_feedback = self.immediate_feedback_check.isChecked()
            self.settings.exercise.track_response_time = self.track_response_time_check.isChecked()
            self.settings.exercise.track_confidence = self.track_confidence_check.isChecked()
            self.settings.exercise.auto_advance_delay = self.auto_advance_spin.value()
        
        # UI settings
        if hasattr(self.settings, 'ui'):
            # Map theme
            index = self.theme_combo.currentIndex()
            if index == 0:
                self.settings.ui.theme = "system"
            elif index == 1:
                self.settings.ui.theme = "light"
            else:
                self.settings.ui.theme = "dark"
            
            # Font family
            font_family = self.font_family_combo.currentText()
            self.settings.ui.font_family = font_family if font_family != "Default" else ""
            
            self.settings.ui.font_size = self.font_size_spin.value()
            self.settings.ui.keyboard_shortcuts = self.keyboard_shortcuts_check.isChecked()
            self.settings.ui.enable_drag_drop = self.enable_drag_drop_check.isChecked()
            self.settings.ui.keyboard_navigation = self.keyboard_navigation_check.isChecked()
            self.settings.ui.high_dpi_scaling = self.high_dpi_check.isChecked()
        
        # Statistics settings
        if hasattr(self.settings, 'statistics'):
            self.settings.statistics.enable_statistics = self.enable_statistics_check.isChecked()
            self.settings.statistics.show_dashboard_startup = self.show_dashboard_startup_check.isChecked()
            self.settings.statistics.retention_days = self.retention_days_spin.value()
            
            # Map export format
            index = self.export_format_combo.currentIndex()
            if index == 0:
                self.settings.statistics.export_format = "csv"
            elif index == 1:
                self.settings.statistics.export_format = "json"
            else:
                self.settings.statistics.export_format = "both"
        
        # Accessibility settings
        if hasattr(self.settings, 'accessibility'):
            self.settings.accessibility.screen_reader_support = self.screen_reader_check.isChecked()
            self.settings.accessibility.high_contrast = self.high_contrast_check.isChecked()
            
            # Map colorblind mode
            index = self.colorblind_combo.currentIndex()
            if index == 0:
                self.settings.accessibility.colorblind_mode = "none"
            elif index == 1:
                self.settings.accessibility.colorblind_mode = "deuteranopia"
            elif index == 2:
                self.settings.accessibility.colorblind_mode = "protanopia"
            else:
                self.settings.accessibility.colorblind_mode = "tritanopia"
            
            self.settings.accessibility.min_button_size = self.min_button_size_spin.value()
        
        # Save to file
        self.settings.save()
    
    def _on_button_clicked(self, button: QPushButton) -> None:
        """Handle button box button click."""
        role = self.button_box.buttonRole(button)
        
        if role == QDialogButtonBox.ButtonRole.ApplyRole:
            self._save_settings()
            self._apply_settings()
    
    def accept(self) -> None:
        """Handle accept (OK) button."""
        self._save_settings()
        super().accept()
    
    def reject(self) -> None:
        """Handle reject (Cancel) button."""
        super().reject()
