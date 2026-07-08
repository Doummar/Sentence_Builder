"""
Missing Word Widget for Grammar Pro.

Widget for the Missing Word exercise type.
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
    QComboBox,
    QFrame,
    QSizePolicy,
)

if TYPE_CHECKING:
    from ..exercise_window import ExerciseWindow
    from ...exercises.missing_word import MissingWordExercise


class MissingWordWidget(QWidget):
    """
    Missing Word Widget.
    
    Provides the UI for the Missing Word exercise.
    """
    
    # Signals
    answer_submitted = pyqtSignal(str)
    
    def __init__(
        self,
        exercise: 'MissingWordExercise',
        parent: QWidget = None
    ):
        """
        Initialize the missing word widget.
        
        Args:
            exercise: Missing word exercise
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
        self.instruction_label = QLabel("Fill in the missing words.")
        self.instruction_label.setWordWrap(True)
        instruction_font = QFont()
        instruction_font.setPointSize(12)
        self.instruction_label.setFont(instruction_font)
        
        # Sentence frame
        self.sentence_frame = QFrame()
        self.sentence_layout = QHBoxLayout(self.sentence_frame)
        self.sentence_layout.setContentsMargins(10, 10, 10, 10)
        self.sentence_layout.setSpacing(10)
        self.sentence_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.sentence_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sentence_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.sentence_frame.setLineWidth(1)
        
        # Word labels and dropdowns
        self.word_widgets: List[QWidget] = []
        
        # Submit button
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Add to main layout
        self.main_layout.addWidget(self.instruction_label)
        self.main_layout.addWidget(self.sentence_frame)
        self.main_layout.addWidget(self.submit_button, 0, Qt.AlignmentFlag.AlignRight)
    
    def _create_layout(self) -> None:
        """Create the layout."""
        pass  # Layout is created in _create_widgets
    
    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        self.submit_button.clicked.connect(self._submit_answer)
    
    def _initialize(self) -> None:
        """Initialize with exercise data."""
        # Clear existing widgets
        while self.sentence_layout.count():
            item = self.sentence_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        self.word_widgets.clear()
        
        # Get partial sentence
        partial = self.exercise.get_partial_sentence()
        missing_positions = self.exercise.get_missing_positions()
        
        # Create widgets for each position
        for i, word in enumerate(partial):
            if word == "___":
                # Missing word - create dropdown
                combo = QComboBox()
                
                # Get options from exercise
                if i < len(self.exercise.steps):
                    step = self.exercise.steps[i]
                    combo.addItems(step.options)
                
                combo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                combo.setMinimumWidth(100)
                
                self.word_widgets.append(combo)
                self.sentence_layout.addWidget(combo)
            else:
                # Regular word - create label
                label = QLabel(word)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFrameShape(QFrame.Shape.Panel)
                label.setFrameShadow(QFrame.Shadow.Raised)
                label.setLineWidth(1)
                label.setMargin(8)
                label.setStyleSheet("""
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 8px;
                """)
                
                self.word_widgets.append(label)
                self.sentence_layout.addWidget(label)
    
    def _submit_answer(self) -> None:
        """Submit the current answer."""
        # Get answers from dropdowns
        answers = []
        for widget in self.word_widgets:
            if isinstance(widget, QComboBox):
                answers.append(widget.currentText())
        
        # For now, just submit the first answer
        if answers:
            self.answer_submitted.emit(answers[0])
    
    def get_answer(self) -> List[str]:
        """Get the current answer."""
        answers = []
        for widget in self.word_widgets:
            if isinstance(widget, QComboBox):
                answers.append(widget.currentText())
        
        return answers
    
    def update_exercise(self, exercise: 'MissingWordExercise') -> None:
        """Update with a new exercise."""
        self.exercise = exercise
        self._initialize()
    
    def show_feedback(self, is_correct: bool, message: str) -> None:
        """Show feedback to the user."""
        # This could be implemented to show feedback in the widget
        pass
