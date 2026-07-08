"""
Grammar Decision Widget for Grammar Pro.

Widget for the Grammar Decision exercise type.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QButtonGroup,
    QRadioButton,
    QFrame,
    QSizePolicy,
)

if TYPE_CHECKING:
    from ..exercise_window import ExerciseWindow
    from ...exercises.grammar_decision import GrammarDecisionExercise


class GrammarDecisionWidget(QWidget):
    """
    Grammar Decision Widget.
    
    Provides the UI for the Grammar Decision exercise.
    """
    
    # Signals
    answer_submitted = pyqtSignal(str)
    
    def __init__(
        self,
        exercise: 'GrammarDecisionExercise',
        parent: QWidget = None
    ):
        """
        Initialize the grammar decision widget.
        
        Args:
            exercise: Grammar decision exercise
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.exercise = exercise
        
        # Create UI
        self._create_widgets()
        self._create_layout()
        self._connect_signals()
        
        # Initialize with exercise data
        self._initialize()
    
    def _create_widgets(self) -> None:
        """Create all widgets."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)
        
        # Question
        self.question_label = QLabel("Loading question...")
        self.question_label.setWordWrap(True)
        question_font = QFont()
        question_font.setPointSize(14)
        question_font.setBold(True)
        self.question_label.setFont(question_font)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Options frame
        self.options_frame = QFrame()
        self.options_layout = QVBoxLayout(self.options_frame)
        self.options_layout.setContentsMargins(10, 10, 10, 10)
        self.options_layout.setSpacing(10)
        
        # Button group for options
        self.button_group = QButtonGroup(self)
        self.option_buttons: List[QRadioButton] = []
        
        # Add some default radio buttons (will be populated with actual options)
        for i in range(5):
            radio = QRadioButton(f"Option {i+1}")
            radio.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.button_group.addButton(radio)
            self.option_buttons.append(radio)
            self.options_layout.addWidget(radio)
        
        # Submit button
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Add to main layout
        self.main_layout.addWidget(self.question_label)
        self.main_layout.addWidget(self.options_frame)
        self.main_layout.addWidget(self.submit_button, 0, Qt.AlignmentFlag.AlignRight)
    
    def _create_layout(self) -> None:
        """Create the layout."""
        pass  # Layout is created in _create_widgets
    
    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        self.submit_button.clicked.connect(self._submit_answer)
    
    def _initialize(self) -> None:
        """Initialize with exercise data."""
        # Set question
        if self.exercise.current_step:
            self.question_label.setText(self.exercise.current_step.question)
            
            # Set options
            options = self.exercise.current_step.options
            
            # Update radio buttons
            for i, option in enumerate(options):
                if i < len(self.option_buttons):
                    self.option_buttons[i].setText(option)
                    self.option_buttons[i].show()
                else:
                    # Create new radio button if needed
                    radio = QRadioButton(option)
                    radio.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    self.button_group.addButton(radio)
                    self.option_buttons.append(radio)
                    self.options_layout.addWidget(radio)
            
            # Hide extra buttons
            for i in range(len(options), len(self.option_buttons)):
                self.option_buttons[i].hide()
    
    def _submit_answer(self) -> None:
        """Submit the selected answer."""
        selected_button = self.button_group.checkedButton()
        
        if selected_button:
            answer = selected_button.text()
            self.answer_submitted.emit(answer)
    
    def get_answer(self) -> str:
        """Get the current answer."""
        selected_button = self.button_group.checkedButton()
        return selected_button.text() if selected_button else ""
    
    def update_exercise(self, exercise: 'GrammarDecisionExercise') -> None:
        """Update with a new exercise."""
        self.exercise = exercise
        self._initialize()
    
    def show_feedback(self, is_correct: bool, message: str) -> None:
        """Show feedback to the user."""
        # This could be implemented to show feedback in the widget
        pass
