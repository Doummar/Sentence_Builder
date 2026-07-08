"""
Exercise Builder Window for Grammar Pro.

Allows users to create custom grammar exercises.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QFormLayout,
    QSizePolicy,
    QMessageBox,
    QFileDialog,
)

if TYPE_CHECKING:
    from ..core.addon_manager import AddonManager


class ExerciseBuilderWindow(QMainWindow):
    """
    Exercise Builder Window for Grammar Pro.
    
    Allows users to create and manage custom grammar exercises.
    """
    
    def __init__(self, addon_manager: 'AddonManager', parent: QWidget = None):
        """
        Initialize the exercise builder window.
        
        Args:
            addon_manager: Addon manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.addon_manager = addon_manager
        self.settings = addon_manager.settings
        
        # Window setup
        self.setWindowTitle("Grammar Pro - Exercise Builder")
        self.setMinimumSize(QSize(800, 600))
        
        # Apply settings
        self._apply_settings()
        
        # Create UI
        self._create_widgets()
        self._create_layout()
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
            QLineEdit, QTextEdit, QComboBox {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                border-radius: 4px;
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
            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QFrame {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
    
    def _create_widgets(self) -> None:
        """Create all widgets."""
        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Left panel - Exercise list
        self.left_panel = QFrame()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(15, 15, 15, 15)
        self.left_layout.setSpacing(15)
        
        self.exercise_list_label = QLabel("Custom Exercises")
        self.exercise_list_label.setFont(QFont("", 14, QFont.Weight.Bold))
        
        self.exercise_list = QListWidget()
        self.exercise_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.new_exercise_button = QPushButton("New Exercise")
        self.delete_exercise_button = QPushButton("Delete Exercise")
        self.export_button = QPushButton("Export Exercises")
        self.import_button = QPushButton("Import Exercises")
        
        self.left_layout.addWidget(self.exercise_list_label)
        self.left_layout.addWidget(self.exercise_list, 1)
        self.left_layout.addWidget(self.new_exercise_button)
        self.left_layout.addWidget(self.delete_exercise_button)
        self.left_layout.addWidget(self.export_button)
        self.left_layout.addWidget(self.import_button)
        
        # Right panel - Exercise editor
        self.right_panel = QFrame()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(15, 15, 15, 15)
        self.right_layout.setSpacing(15)
        
        self.editor_label = QLabel("Exercise Editor")
        self.editor_label.setFont(QFont("", 14, QFont.Weight.Bold))
        
        # Form for exercise properties
        self.form_frame = QFrame()
        self.form_layout = QFormLayout(self.form_frame)
        self.form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Exercise name
        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.form_layout.addRow(self.name_label, self.name_edit)
        
        # Exercise type
        self.type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Sentence Builder",
            "Grammar Decision",
            "Find Mistake",
            "Missing Word",
            "Clause Trainer",
            "Transformation",
            "Inversion Practice",
            "Negation Trainer",
            "Subordinate Clause",
            "Mixed Challenge"
        ])
        self.form_layout.addRow(self.type_label, self.type_combo)
        
        # Language
        self.language_label = QLabel("Language:")
        self.language_combo = QComboBox()
        languages = self.addon_manager.get_available_languages()
        for lang in languages:
            self.language_combo.addItem(lang['name'], lang['code'])
        self.form_layout.addRow(self.language_label, self.language_combo)
        
        # Difficulty
        self.difficulty_label = QLabel("Difficulty:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems([
            "Level 1 - Subject + Verb",
            "Level 2 - Subject + Verb + Object",
            "Level 3 - Adjectives",
            "Level 4 - Adverbs",
            "Level 5 - Time Expressions",
            "Level 6 - Place Expressions",
            "Level 7 - Negation",
            "Level 8 - Questions",
            "Level 9 - Modal Verbs",
            "Level 10 - Fronting",
            "Level 11 - V2 Rule",
            "Level 12 - Subordinate Clauses",
            "Level 13 - Relative Clauses",
            "Level 14 - Long Sentences"
        ])
        self.form_layout.addRow(self.difficulty_label, self.difficulty_combo)
        
        # Description
        self.description_label = QLabel("Description:")
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.form_layout.addRow(self.description_label, self.description_edit)
        
        # Sentence/Words
        self.sentence_label = QLabel("Sentence/Words:")
        self.sentence_edit = QLineEdit()
        self.sentence_edit.setPlaceholderText("Enter words separated by spaces")
        self.form_layout.addRow(self.sentence_label, self.sentence_edit)
        
        # Grammar categories
        self.categories_label = QLabel("Grammar Categories:")
        self.categories_edit = QLineEdit()
        self.categories_edit.setPlaceholderText("Comma-separated list of categories")
        self.form_layout.addRow(self.categories_label, self.categories_edit)
        
        self.right_layout.addWidget(self.editor_label)
        self.right_layout.addWidget(self.form_frame)
        
        # Save button
        self.save_button = QPushButton("Save Exercise")
        self.save_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.right_layout.addWidget(self.save_button, 0, Qt.AlignmentFlag.AlignRight)
        
        # Add to main layout
        self.main_layout.addWidget(self.left_panel, 1)
        self.main_layout.addWidget(self.right_panel, 2)
    
    def _create_layout(self) -> None:
        """Create the layout."""
        pass  # Layout is created in _create_widgets
    
    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        self.new_exercise_button.clicked.connect(self._new_exercise)
        self.delete_exercise_button.clicked.connect(self._delete_exercise)
        self.export_button.clicked.connect(self._export_exercises)
        self.import_button.clicked.connect(self._import_exercises)
        self.save_button.clicked.connect(self._save_exercise)
        self.exercise_list.itemSelectionChanged.connect(self._on_exercise_selected)
    
    def _load_data(self) -> None:
        """Load custom exercises."""
        # Load custom exercises from data manager
        custom_exercises = self.addon_manager.data_manager.list_custom_exercises()
        
        self.exercise_list.clear()
        
        for exercise in custom_exercises:
            item = QListWidgetItem(exercise.get('name', 'Unnamed Exercise'))
            item.setData(Qt.ItemDataRole.UserRole, exercise.get('id', ''))
            self.exercise_list.addItem(item)
    
    def _new_exercise(self) -> None:
        """Create a new exercise."""
        # Clear the form
        self.name_edit.clear()
        self.type_combo.setCurrentIndex(0)
        self.language_combo.setCurrentIndex(0)
        self.difficulty_combo.setCurrentIndex(0)
        self.description_edit.clear()
        self.sentence_edit.clear()
        self.categories_edit.clear()
        
        # Clear selection
        self.exercise_list.clearSelection()
    
    def _delete_exercise(self) -> None:
        """Delete the selected exercise."""
        selected_items = self.exercise_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "Delete Exercise", "Please select an exercise to delete.")
            return
        
        item = selected_items[0]
        exercise_id = item.data(Qt.ItemDataRole.UserRole)
        
        if exercise_id:
            result = QMessageBox.question(
                self, "Delete Exercise",
                "Are you sure you want to delete this exercise?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if result == QMessageBox.StandardButton.Yes:
                # Delete from data manager
                self.addon_manager.data_manager.delete_custom_exercise(exercise_id)
                
                # Remove from list
                row = self.exercise_list.row(item)
                self.exercise_list.takeItem(row)
                
                # Clear the form
                self._new_exercise()
    
    def _export_exercises(self) -> None:
        """Export custom exercises."""
        # Get export format from settings
        export_format = self.settings.statistics.export_format if self.settings else "json"
        
        # Export data
        data = self.addon_manager.data_manager.export_data(export_format)
        
        if not data:
            QMessageBox.warning(self, "Export", "No data to export.")
            return
        
        # Show save dialog
        options = QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Exercises", "",
            f"Grammar Pro Exercises (*.{export_format});;All Files (*)",
            options=options
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
                QMessageBox.information(self, "Export", "Exercises exported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Export", f"Error exporting exercises: {e}")
    
    def _import_exercises(self) -> None:
        """Import custom exercises."""
        # Show open dialog
        options = QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Exercises", "",
            "Grammar Pro Exercises (*.json);;All Files (*)",
            options=options
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                
                # Import data
                success = self.addon_manager.data_manager.import_data(data, "json")
                
                if success:
                    QMessageBox.information(self, "Import", "Exercises imported successfully.")
                    self._load_data()
                else:
                    QMessageBox.warning(self, "Import", "No exercises were imported.")
            except Exception as e:
                QMessageBox.critical(self, "Import", f"Error importing exercises: {e}")
    
    def _save_exercise(self) -> None:
        """Save the current exercise."""
        # Get values from form
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Save Exercise", "Please enter a name for the exercise.")
            return
        
        exercise_type = self.type_combo.currentText()
        language = self.language_combo.currentData()
        difficulty = self.difficulty_combo.currentIndex() + 1
        description = self.description_edit.toPlainText().strip()
        sentence = self.sentence_edit.text().strip()
        categories = self.categories_edit.text().strip()
        
        # Map exercise type to ID
        type_map = {
            "Sentence Builder": "sentence_builder",
            "Grammar Decision": "grammar_decision",
            "Find Mistake": "find_mistake",
            "Missing Word": "missing_word",
            "Clause Trainer": "clause_trainer",
            "Transformation": "transformation",
            "Inversion Practice": "inversion",
            "Negation Trainer": "negation",
            "Subordinate Clause": "subordinate_clause",
            "Mixed Challenge": "mixed_challenge"
        }
        
        exercise_data = {
            'name': name,
            'type': type_map.get(exercise_type, 'sentence_builder'),
            'language': language,
            'difficulty': difficulty,
            'description': description,
            'sentence': sentence,
            'categories': [c.strip() for c in categories.split(',')] if categories else [],
        }
        
        # Save to data manager
        success = self.addon_manager.data_manager.save_custom_exercise(exercise_data)
        
        if success:
            QMessageBox.information(self, "Save Exercise", "Exercise saved successfully.")
            self._load_data()
            
            # Find and select the new exercise
            for i in range(self.exercise_list.count()):
                item = self.exercise_list.item(i)
                if item.text() == name:
                    self.exercise_list.setCurrentItem(item)
                    break
        else:
            QMessageBox.warning(self, "Save Exercise", "Failed to save exercise.")
    
    def _on_exercise_selected(self) -> None:
        """Handle exercise selection."""
        selected_items = self.exercise_list.selectedItems()
        
        if not selected_items:
            return
        
        item = selected_items[0]
        exercise_id = item.data(Qt.ItemDataRole.UserRole)
        
        if exercise_id:
            # Load exercise data
            exercise_data = self.addon_manager.data_manager.load_custom_exercise(exercise_id)
            
            if exercise_data:
                # Populate form
                self.name_edit.setText(exercise_data.get('name', ''))
                
                # Map type back to display name
                type_map = {
                    'sentence_builder': "Sentence Builder",
                    'grammar_decision': "Grammar Decision",
                    'find_mistake': "Find Mistake",
                    'missing_word': "Missing Word",
                    'clause_trainer': "Clause Trainer",
                    'transformation': "Transformation",
                    'inversion': "Inversion Practice",
                    'negation': "Negation Trainer",
                    'subordinate_clause': "Subordinate Clause",
                    'mixed_challenge': "Mixed Challenge"
                }
                
                exercise_type = exercise_data.get('type', 'sentence_builder')
                display_type = type_map.get(exercise_type, "Sentence Builder")
                index = self.type_combo.findText(display_type)
                if index >= 0:
                    self.type_combo.setCurrentIndex(index)
                
                # Set language
                language = exercise_data.get('language', 'da')
                index = self.language_combo.findData(language)
                if index >= 0:
                    self.language_combo.setCurrentIndex(index)
                
                # Set difficulty
                difficulty = exercise_data.get('difficulty', 1)
                index = difficulty - 1
                if 0 <= index < self.difficulty_combo.count():
                    self.difficulty_combo.setCurrentIndex(index)
                
                self.description_edit.setPlainText(exercise_data.get('description', ''))
                self.sentence_edit.setText(exercise_data.get('sentence', ''))
                self.categories_edit.setText(', '.join(exercise_data.get('categories', [])))
    
    def closeEvent(self, event: Any) -> None:
        """Handle close event."""
        # Save settings
        if self.settings:
            size = self.size()
            self.settings.ui.window_width = size.width()
            self.settings.ui.window_height = size.height()
            self.settings.save()
        
        super().closeEvent(event)


# Import Any for type hints
from typing import Any
