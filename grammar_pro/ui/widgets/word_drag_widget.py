"""
Word Drag Widget for Grammar Pro.

Provides drag-and-drop functionality for word rearrangement exercises.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QMimeData, QSize
from PyQt6.QtGui import QDrag, QFont, QColor, QPalette
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy,
)

if TYPE_CHECKING:
    from ..exercise_window import ExerciseWindow


class DraggableWordLabel(QLabel):
    """
    Label that can be dragged.
    
    Represents a word that can be dragged and dropped.
    """
    
    def __init__(self, text: str, parent: QWidget = None):
        """
        Initialize the draggable word label.
        
        Args:
            text: Word text
            parent: Parent widget
        """
        super().__init__(text, parent)
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFrameShape(QFrame.Shape.Panel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(1)
        self.setMargin(8)
        
        # Make it look draggable
        self.setStyleSheet("""
            DraggableWordLabel {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
                cursor: move;
            }
            DraggableWordLabel:hover {
                background-color: #d0d0d0;
            }
        """)
        
        # Enable drag
        self.setAcceptDrops(False)
    
    def mousePressEvent(self, event: Any) -> None:
        """Handle mouse press event."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_drag()
        
        super().mousePressEvent(event)
    
    def _start_drag(self) -> None:
        """Start a drag operation."""
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)
        
        # Set drag icon (optional)
        # drag.setPixmap(QPixmap("icon.png"))
        
        # Start the drag
        drag.exec(Qt.DropAction.MoveAction)


class DropZoneFrame(QFrame):
    """
    Frame that accepts dropped words.
    
    Represents a target area for dropping words.
    """
    
    def __init__(self, parent: QWidget = None):
        """
        Initialize the drop zone frame.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setLineWidth(2)
        self.setMinimumHeight(50)
        
        # Layout for dropped words
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Words in this zone
        self.words: List[str] = []
        
        # Style
        self.setStyleSheet("""
            DropZoneFrame {
                background-color: #f8f8f8;
                border: 2px dashed #ccc;
                border-radius: 4px;
                min-height: 50px;
            }
        """)
        
        # Enable drop
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event: Any) -> None:
        """Handle drag enter event."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)
    
    def dropEvent(self, event: Any) -> None:
        """Handle drop event."""
        if event.mimeData().hasText():
            word = event.mimeData().text()
            self._add_word(word)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
    
    def _add_word(self, word: str) -> None:
        """Add a word to this drop zone."""
        if word not in self.words:
            self.words.append(word)
            
            # Create label for the word
            label = QLabel(word)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFrameShape(QFrame.Shape.Panel)
            label.setFrameShadow(QFrame.Shadow.Raised)
            label.setLineWidth(1)
            label.setMargin(5)
            label.setStyleSheet("""
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            """)
            
            self.layout.addWidget(label)
    
    def clear(self) -> None:
        """Clear all words from this drop zone."""
        self.words.clear()
        
        # Remove all widgets
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
    
    def get_words(self) -> List[str]:
        """Get all words in this drop zone."""
        return self.words.copy()


class WordDragWidget(QWidget):
    """
    Word Drag Widget for Grammar Pro.
    
    Provides a complete drag-and-drop interface for word rearrangement exercises.
    """
    
    # Signals
    answer_submitted = pyqtSignal(list)
    
    def __init__(self, words: List[str], parent: QWidget = None):
        """
        Initialize the word drag widget.
        
        Args:
            words: List of words to arrange
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.words = words
        self.user_order: List[str] = []
        
        # Create UI
        self._create_widgets()
        self._create_layout()
    
    def _create_widgets(self) -> None:
        """Create all widgets."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)
        
        # Instruction
        self.instruction_label = QLabel("Drag words to arrange them in the correct order:")
        self.instruction_label.setWordWrap(True)
        
        # Word source (available words)
        self.source_frame = QFrame()
        self.source_layout = QHBoxLayout(self.source_frame)
        self.source_layout.setContentsMargins(10, 10, 10, 10)
        self.source_layout.setSpacing(10)
        self.source_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.source_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.source_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.source_frame.setLineWidth(1)
        
        # Create draggable word labels
        self.word_labels = []
        for word in self.words:
            label = DraggableWordLabel(word)
            self.word_labels.append(label)
            self.source_layout.addWidget(label)
        
        # Target area (where user drops words)
        self.target_frame = DropZoneFrame()
        
        # Submit button area
        self.submit_frame = QFrame()
        self.submit_layout = QHBoxLayout(self.submit_frame)
        self.submit_layout.setContentsMargins(10, 10, 10, 10)
        
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self._submit_answer)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._clear_answer)
        
        self.submit_layout.addWidget(self.submit_button)
        self.submit_layout.addWidget(self.clear_button)
        
        # Add to main layout
        self.main_layout.addWidget(self.instruction_label)
        self.main_layout.addWidget(self.source_frame)
        self.main_layout.addWidget(self.target_frame, 1)
        self.main_layout.addWidget(self.submit_frame)
    
    def _create_layout(self) -> None:
        """Create the layout."""
        pass  # Layout is created in _create_widgets
    
    def _submit_answer(self) -> None:
        """Submit the current answer."""
        answer = self.target_frame.get_words()
        self.answer_submitted.emit(answer)
    
    def _clear_answer(self) -> None:
        """Clear the current answer."""
        self.target_frame.clear()
        self.user_order = []
    
    def get_answer(self) -> List[str]:
        """Get the current answer."""
        return self.target_frame.get_words()
    
    def set_words(self, words: List[str]) -> None:
        """Set the words to arrange."""
        self.words = words
        self.user_order = []
        
        # Clear existing words
        while self.source_layout.count():
            item = self.source_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        self.word_labels.clear()
        
        # Add new words
        for word in words:
            label = DraggableWordLabel(word)
            self.word_labels.append(label)
            self.source_layout.addWidget(label)
        
        # Clear target
        self.target_frame.clear()
    
    def set_instruction(self, text: str) -> None:
        """Set the instruction text."""
        self.instruction_label.setText(text)
