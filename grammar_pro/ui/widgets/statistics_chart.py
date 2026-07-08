"""
Statistics Chart Widget for Grammar Pro.

Simple chart widget for displaying statistics.
"""

from typing import Any, Dict, List, Tuple

from PyQt6.QtCore import Qt, QSize, QPointF, QRectF
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PyQt6.QtWidgets import QWidget, QSizePolicy


class StatisticsChart(QWidget):
    """
    Simple Statistics Chart Widget.
    
    Displays data as a bar chart or line chart.
    """
    
    def __init__(self, parent: QWidget = None):
        """
        Initialize the statistics chart.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Properties
        self._chart_type = "bar"  # 'bar' or 'line'
        self._data: List[Tuple[str, float]] = []
        self._title = ""
        self._x_label = ""
        self._y_label = ""
        
        # Colors
        self._background_color = QColor(255, 255, 255)
        self._grid_color = QColor(220, 220, 220)
        self._bar_color = QColor(76, 175, 80)  # Green
        self._line_color = QColor(76, 175, 80)
        self._text_color = QColor(0, 0, 0)
        
        # Size policy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(QSize(300, 200))
    
    def setChartType(self, chart_type: str) -> None:
        """Set the chart type."""
        if chart_type in ["bar", "line"]:
            self._chart_type = chart_type
            self.update()
    
    def setData(self, data: List[Tuple[str, float]]) -> None:
        """Set the data to display."""
        self._data = data
        self.update()
    
    def setTitle(self, title: str) -> None:
        """Set the chart title."""
        self._title = title
        self.update()
    
    def setXLabel(self, label: str) -> None:
        """Set the X-axis label."""
        self._x_label = label
        self.update()
    
    def setYLabel(self, label: str) -> None:
        """Set the Y-axis label."""
        self._y_label = label
        self.update()
    
    def setBackgroundColor(self, color: QColor) -> None:
        """Set the background color."""
        self._background_color = color
        self.update()
    
    def setBarColor(self, color: QColor) -> None:
        """Set the bar color."""
        self._bar_color = color
        self.update()
    
    def setLineColor(self, color: QColor) -> None:
        """Set the line color."""
        self._line_color = color
        self.update()
    
    def paintEvent(self, event: Any) -> None:
        """Paint the chart."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self._background_color)
        
        # Draw border
        painter.setPen(QPen(self._text_color, 1))
        painter.drawRect(self.rect())
        
        # Calculate dimensions
        width = self.width()
        height = self.height()
        
        # Margins
        left_margin = 50
        right_margin = 20
        top_margin = 50
        bottom_margin = 40
        
        # Draw area
        draw_width = width - left_margin - right_margin
        draw_height = height - top_margin - bottom_margin
        draw_rect = QRectF(left_margin, top_margin, draw_width, draw_height)
        
        # Draw title
        if self._title:
            painter.setFont(QFont("", 12, QFont.Weight.Bold))
            painter.drawText(
                left_margin, 20,
                width - left_margin - right_margin, 30,
                Qt.AlignmentFlag.AlignCenter,
                self._title
            )
        
        # Draw grid
        painter.setPen(QPen(self._grid_color, 1))
        
        # Horizontal grid lines
        num_h_lines = 5
        for i in range(num_h_lines + 1):
            y = top_margin + draw_height - (i * draw_height / num_h_lines)
            painter.drawLine(left_margin, y, width - right_margin, y)
            
            # Draw Y-axis labels
            value = i * 100 / num_h_lines
            painter.setPen(QPen(self._text_color))
            painter.drawText(
                10, y - 10, 40, 20,
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"{value:.0f}%"
            )
        
        # Draw data
        if not self._data:
            return
        
        # Calculate max value
        max_value = max(value for _, value in self._data) if self._data else 100
        
        # Draw bars or lines
        num_items = len(self._data)
        if num_items == 0:
            return
        
        bar_width = draw_width / num_items * 0.8
        bar_spacing = draw_width / num_items * 0.2
        
        if self._chart_type == "bar":
            # Draw bars
            for i, (label, value) in enumerate(self._data):
                x = left_margin + i * (bar_width + bar_spacing) + bar_spacing
                bar_height = (value / max_value) * draw_height
                y = top_margin + draw_height - bar_height
                
                painter.fillRect(
                    QRectF(x, y, bar_width, bar_height),
                    self._bar_color
                )
                
                # Draw bar border
                painter.setPen(QPen(self._text_color, 1))
                painter.drawRect(
                    QRectF(x, y, bar_width, bar_height)
                )
                
                # Draw value label
                painter.drawText(
                    x, y - 20, bar_width, 20,
                    Qt.AlignmentFlag.AlignCenter,
                    f"{value:.0f}%"
                )
                
                # Draw X-axis label
                painter.drawText(
                    x, top_margin + draw_height + 10, bar_width, 20,
                    Qt.AlignmentFlag.AlignCenter,
                    label
                )
        
        else:  # line chart
            # Draw line
            painter.setPen(QPen(self._line_color, 2))
            
            points = []
            for i, (label, value) in enumerate(self._data):
                x = left_margin + i * (draw_width / (num_items - 1)) if num_items > 1 else left_margin + draw_width / 2
                y = top_margin + draw_height - (value / max_value) * draw_height
                points.append(QPointF(x, y))
            
            painter.drawPolyline(points)
            
            # Draw points
            for point in points:
                painter.setBrush(QBrush(self._line_color))
                painter.drawEllipse(point, 4, 4)
            
            # Draw X-axis labels
            for i, (label, value) in enumerate(self._data):
                x = left_margin + i * (draw_width / (num_items - 1)) if num_items > 1 else left_margin + draw_width / 2
                painter.drawText(
                    x - 30, top_margin + draw_height + 10, 60, 20,
                    Qt.AlignmentFlag.AlignCenter,
                    label
                )
        
        # Draw X-axis label
        if self._x_label:
            painter.drawText(
                left_margin + draw_width / 2 - 30, top_margin + draw_height + 30,
                60, 20,
                Qt.AlignmentFlag.AlignCenter,
                self._x_label
            )
        
        # Draw Y-axis label
        if self._y_label:
            painter.save()
            painter.translate(20, top_margin + draw_height / 2)
            painter.rotate(-90)
            painter.drawText(
                0, 0, 100, 20,
                Qt.AlignmentFlag.AlignCenter,
                self._y_label
            )
            painter.restore()
