"""
Progress Bar Widget for Grammar Pro.

Custom progress bar with additional features.
"""

from typing import Any, Optional

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush
from PyQt6.QtWidgets import QWidget, QSizePolicy


class ProgressBar(QWidget):
    """
    Custom Progress Bar Widget.
    
    Displays progress with a smooth gradient and optional text.
    """
    
    def __init__(self, parent: QWidget = None):
        """
        Initialize the progress bar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Properties
        self._minimum = 0
        self._maximum = 100
        self._value = 0
        self._text = ""
        self._text_visible = True
        self._orientation = Qt.Orientation.Horizontal
        
        # Colors
        self._background_color = QColor(240, 240, 240)
        self._foreground_color = QColor(76, 175, 80)  # Green
        self._text_color = QColor(0, 0, 0)
        self._border_color = QColor(200, 200, 200)
        
        # Size policy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(20)
    
    def setMinimum(self, minimum: int) -> None:
        """Set the minimum value."""
        self._minimum = minimum
        self.update()
    
    def setMaximum(self, maximum: int) -> None:
        """Set the maximum value."""
        self._maximum = maximum
        self.update()
    
    def setValue(self, value: int) -> None:
        """Set the current value."""
        self._value = max(self._minimum, min(value, self._maximum))
        self.update()
    
    def setText(self, text: str) -> None:
        """Set the text to display."""
        self._text = text
        self.update()
    
    def setTextVisible(self, visible: bool) -> None:
        """Set whether text is visible."""
        self._text_visible = visible
        self.update()
    
    def setOrientation(self, orientation: Qt.Orientation) -> None:
        """Set the orientation."""
        self._orientation = orientation
        self.update()
    
    def setBackgroundColor(self, color: QColor) -> None:
        """Set the background color."""
        self._background_color = color
        self.update()
    
    def setForegroundColor(self, color: QColor) -> None:
        """Set the foreground (progress) color."""
        self._foreground_color = color
        self.update()
    
    def setTextColor(self, color: QColor) -> None:
        """Set the text color."""
        self._text_color = color
        self.update()
    
    def setBorderColor(self, color: QColor) -> None:
        """Set the border color."""
        self._border_color = color
        self.update()
    
    def value(self) -> int:
        """Get the current value."""
        return self._value
    
    def minimum(self) -> int:
        """Get the minimum value."""
        return self._minimum
    
    def maximum(self) -> int:
        """Get the maximum value."""
        return self._maximum
    
    def paintEvent(self, event: Any) -> None:
        """Paint the progress bar."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self._background_color)
        
        # Draw border
        painter.setPen(QPen(self._border_color, 1))
        painter.drawRect(self.rect())
        
        # Calculate progress
        if self._maximum <= self._minimum:
            progress = 0
        else:
            progress = (self._value - self._minimum) / (self._maximum - self._minimum)
        
        # Draw progress
        if self._orientation == Qt.Orientation.Horizontal:
            width = int(self.width() * progress)
            painter.fillRect(0, 0, width, self.height(), self._foreground_color)
        else:
            height = int(self.height() * progress)
            painter.fillRect(0, self.height() - height, self.width(), height, self._foreground_color)
        
        # Draw text
        if self._text_visible:
            text = self._text if self._text else f"{int(progress * 100)}%"
            
            painter.setPen(QPen(self._text_color))
            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                text
            )
    
    def sizeHint(self) -> QSize:
        """Get the recommended size."""
        return QSize(200, 20)
