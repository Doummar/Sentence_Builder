"""
Sentence Builder Widget for Grammar Pro.

Widget for the Sentence Builder exercise type.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
)

from .word_drag_widget import WordDragWidget

if TYPE_CHECKING:
    from ..exercise_window import ExerciseWindow
    from ...exercises.sentence_builder import SentenceBuilderExercise


class SentenceBuilderWidget(QWidget):
    """
    Sentence Builder Widget.
    
    Provides the UI for the Sentence Builder exercise.
    """
    
    # Signals
    answer_submitted = pyqtSignal(list)
    
    def __init__(
        self,
        exercise: 'SentenceBuilderExercise',
        parent: QWidget = None
    ):
        """
        Initialize the sentence builder widget.
        
        Args:
            exercise: Sentence builder exercise
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
        
        # Instruction
        self.instruction_label = QLabel("Arrange the words to form a correct sentence.")
        self.instruction_label.setWordWrap(True)
        instruction_font = QFont()
        instruction_font.setPointSize(12)
        self.instruction_label.setFont(instruction_font)
        
        # Word drag widget
        self.word_drag_widget = WordDragWidget(
            self.exercise.get_shuffled_words(),
            self
        )
        self.word_drag_widget.answer_submitted.connect(self._on_answer_submitted)
        
        # Add to main layout
        self.main_layout.addWidget(self.instruction_label)
        self.main_layout.addWidget(self.word_drag_widget, 1)
    
    def _create_layout(self) -> None:
        """Create the layout."""
        pass  # Layout is created in _create_widgets
    
    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        pass
    
    def _initialize(self) -> None:
        """Initialize with exercise data."""
        # Set words
        self.word_drag_widget.set_words(self.exercise.get_shuffled_words())
        
        # Set instruction
        if self.exercise.current_step:
            self.instruction_label.setText(self.exercise.current_step.question)
    
    def _on_answer_submitted(self, answer: List[str]) -> None:
        """Handle answer submission."""
        self.answer_submitted.emit(answer)
    
    def get_answer(self) -> List[str]:
        """Get the current answer."""
        return self.word_drag_widget.get_answer()
    
    def update_exercise(self, exercise: 'SentenceBuilderExercise') -> None:
        """Update with a new exercise."""
        self.exercise = exercise
        self._initialize()
    
    def show_feedback(self, is_correct: bool, message: str) -> None:
        """Show feedback to the user."""
        # This could be implemented to show feedback in the widget
        pass
