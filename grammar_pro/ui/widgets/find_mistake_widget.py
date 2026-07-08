"""
Find Mistake Widget for Grammar Pro.

Widget for the Find Mistake exercise type.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
)

if TYPE_CHECKING:
    from ..exercise_window import ExerciseWindow
    from ...exercises.find_mistake import FindMistakeExercise


class ClickableWordLabel(QLabel):
    """
    Label that can be clicked to select a word.
    """
    
    def __init__(self, text: str, position: int, parent: QWidget = None):
        """
        Initialize the clickable word label.
        
        Args:
            text: Word text
            position: Position in sentence
            parent: Parent widget
        """
        super().__init__(text, parent)
        
        self.position = position
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFrameShape(QFrame.Shape.Panel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(1)
        self.setMargin(8)
        
        # Style
        self.setStyleSheet("""
            ClickableWordLabel {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
                cursor: pointer;
            }
            ClickableWordLabel:hover {
                background-color: #e0e0e0;
            }
            ClickableWordLabel:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)
    
    def mousePressEvent(self, event: Any) -> None:
        """Handle mouse press event."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet("""
                ClickableWordLabel {
                    background-color: #4CAF50;
                    color: white;
                    border: 1px solid #45a049;
                    border-radius: 4px;
                    padding: 8px;
                    cursor: pointer;
                }
            """)
        
        super().mousePressEvent(event)


class FindMistakeWidget(QWidget):
    """
    Find Mistake Widget.
    
    Provides the UI for the Find Mistake exercise.
    """
    
    # Signals
    answer_submitted = pyqtSignal(int)
    
    def __init__(
        self,
        exercise: 'FindMistakeExercise',
        parent: QWidget = None
    ):
        """
        Initialize the find mistake widget.
        
        Args:
            exercise: Find mistake exercise
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.exercise = exercise
        self.selected_position = -1
        
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
        self.instruction_label = QLabel("Click on the word that is incorrect or in the wrong position.")
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
        
        # Word labels
        self.word_labels: List[ClickableWordLabel] = []
        
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
        # Clear existing words
        while self.sentence_layout.count():
            item = self.sentence_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        self.word_labels.clear()
        self.selected_position = -1
        
        # Get sentence
        sentence = self.exercise.get_sentence()
        
        # Create word labels
        for i, word in enumerate(sentence):
            label = ClickableWordLabel(word, i)
            label.setProperty("position", i)
            label.mousePressEvent = lambda event, pos=i: self._on_word_clicked(event, pos)
            self.word_labels.append(label)
            self.sentence_layout.addWidget(label)
    
    def _on_word_clicked(self, event: Any, position: int) -> None:
        """Handle word click."""
        # Deselect previous selection
        if self.selected_position >= 0 and self.selected_position < len(self.word_labels):
            self.word_labels[self.selected_position].setStyleSheet("""
                ClickableWordLabel {
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 8px;
                    cursor: pointer;
                }
                ClickableWordLabel:hover {
                    background-color: #e0e0e0;
                }
            """)
        
        # Select new word
        self.selected_position = position
        self.word_labels[position].setStyleSheet("""
            ClickableWordLabel {
                background-color: #4CAF50;
                color: white;
                border: 1px solid #45a049;
                border-radius: 4px;
                padding: 8px;
                cursor: pointer;
            }
        """)
    
    def _submit_answer(self) -> None:
        """Submit the selected answer."""
        if self.selected_position >= 0:
            self.answer_submitted.emit(self.selected_position)
    
    def get_answer(self) -> int:
        """Get the current answer (selected position)."""
        return self.selected_position
    
    def update_exercise(self, exercise: 'FindMistakeExercise') -> None:
        """Update with a new exercise."""
        self.exercise = exercise
        self._initialize()
    
    def show_feedback(self, is_correct: bool, message: str) -> None:
        """Show feedback to the user."""
        # Highlight the mistake if not correct
        if not is_correct and self.exercise.get_mistake_position() >= 0:
            mistake_pos = self.exercise.get_mistake_position()
            if mistake_pos < len(self.word_labels):
                self.word_labels[mistake_pos].setStyleSheet("""
                    ClickableWordLabel {
                        background-color: #F44336;
                        color: white;
                        border: 1px solid #d32f2f;
                        border-radius: 4px;
                        padding: 8px;
                        cursor: pointer;
                    }
                """)
