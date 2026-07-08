"""
Dashboard Window for Grammar Pro.

Displays statistics, progress, and analytics to the user.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTabWidget,
    QScrollArea,
    QSizePolicy,
)

if TYPE_CHECKING:
    from ..core.addon_manager import AddonManager


class DashboardWindow(QMainWindow):
    """
    Dashboard Window for Grammar Pro.
    
    Displays user statistics, progress, and analytics.
    """
    
    def __init__(self, addon_manager: 'AddonManager', parent: QWidget = None):
        """
        Initialize the dashboard window.
        
        Args:
            addon_manager: Addon manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.addon_manager = addon_manager
        self.settings = addon_manager.settings
        
        # Window setup
        self.setWindowTitle("Grammar Pro - Dashboard")
        self.setMinimumSize(QSize(900, 600))
        
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
        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Header
        self.header_label = QLabel("Grammar Pro Dashboard")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setBold(True)
        self.header_label.setFont(header_font)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Overview tab
        self.overview_tab = QWidget()
        self._create_overview_tab()
        
        # Statistics tab
        self.statistics_tab = QWidget()
        self._create_statistics_tab()
        
        # Progress tab
        self.progress_tab = QWidget()
        self._create_progress_tab()
        
        # Weak Areas tab
        self.weak_areas_tab = QWidget()
        self._create_weak_areas_tab()
        
        # Add tabs
        self.tab_widget.addTab(self.overview_tab, "Overview")
        self.tab_widget.addTab(self.statistics_tab, "Statistics")
        self.tab_widget.addTab(self.progress_tab, "Progress")
        self.tab_widget.addTab(self.weak_areas_tab, "Weak Areas")
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Add to main layout
        self.main_layout.addWidget(self.header_label)
        self.main_layout.addWidget(self.tab_widget, 1)
        self.main_layout.addWidget(self.close_button, 0, Qt.AlignmentFlag.AlignRight)
    
    def _create_layout(self) -> None:
        """Create the layout."""
        pass  # Layout is created in _create_widgets
    
    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        self.close_button.clicked.connect(self.close)
    
    def _load_data(self) -> None:
        """Load data for the dashboard."""
        # Update all tabs
        self._update_overview_tab()
        self._update_statistics_tab()
        self._update_progress_tab()
        self._update_weak_areas_tab()
    
    def _create_overview_tab(self) -> None:
        """Create the overview tab."""
        layout = QVBoxLayout(self.overview_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Summary frame
        summary_frame = QFrame()
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setContentsMargins(15, 15, 15, 15)
        summary_layout.setSpacing(20)
        
        # Total exercises
        self.total_exercises_label = QLabel("Total Exercises: 0")
        total_font = QFont()
        total_font.setPointSize(16)
        total_font.setBold(True)
        self.total_exercises_label.setFont(total_font)
        
        # Accuracy
        self.accuracy_label = QLabel("Accuracy: 0%")
        accuracy_font = QFont()
        accuracy_font.setPointSize(16)
        accuracy_font.setBold(True)
        self.accuracy_label.setFont(accuracy_font)
        
        # Mastery
        self.mastery_label = QLabel("Mastery: 0%")
        mastery_font = QFont()
        mastery_font.setPointSize(16)
        mastery_font.setBold(True)
        self.mastery_label.setFont(mastery_font)
        
        summary_layout.addWidget(self.total_exercises_label)
        summary_layout.addWidget(self.accuracy_label)
        summary_layout.addWidget(self.mastery_label)
        
        # Recent activity
        recent_frame = QFrame()
        recent_layout = QVBoxLayout(recent_frame)
        recent_layout.setContentsMargins(15, 15, 15, 15)
        recent_layout.setSpacing(10)
        
        recent_label = QLabel("Recent Activity")
        recent_label.setFont(QFont("", 14, QFont.Weight.Bold))
        
        self.recent_activity_label = QLabel("No recent activity")
        self.recent_activity_label.setWordWrap(True)
        
        recent_layout.addWidget(recent_label)
        recent_layout.addWidget(self.recent_activity_label)
        
        # Add to main layout
        layout.addWidget(summary_frame)
        layout.addWidget(recent_frame, 1)
        layout.addStretch()
    
    def _create_statistics_tab(self) -> None:
        """Create the statistics tab."""
        layout = QVBoxLayout(self.statistics_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Statistics by category
        self.category_stats_frame = QFrame()
        self.category_stats_layout = QVBoxLayout(self.category_stats_frame)
        self.category_stats_layout.setContentsMargins(10, 10, 10, 10)
        self.category_stats_layout.setSpacing(10)
        
        category_label = QLabel("Statistics by Category")
        category_label.setFont(QFont("", 14, QFont.Weight.Bold))
        
        self.category_stats_label = QLabel("No statistics available")
        self.category_stats_label.setWordWrap(True)
        
        self.category_stats_layout.addWidget(category_label)
        self.category_stats_layout.addWidget(self.category_stats_label)
        
        # Statistics by exercise type
        self.type_stats_frame = QFrame()
        self.type_stats_layout = QVBoxLayout(self.type_stats_frame)
        self.type_stats_layout.setContentsMargins(10, 10, 10, 10)
        self.type_stats_layout.setSpacing(10)
        
        type_label = QLabel("Statistics by Exercise Type")
        type_label.setFont(QFont("", 14, QFont.Weight.Bold))
        
        self.type_stats_label = QLabel("No statistics available")
        self.type_stats_label.setWordWrap(True)
        
        self.type_stats_layout.addWidget(type_label)
        self.type_stats_layout.addWidget(self.type_stats_label)
        
        # Add to main layout
        layout.addWidget(self.category_stats_frame)
        layout.addWidget(self.type_stats_frame)
        layout.addStretch()
    
    def _create_progress_tab(self) -> None:
        """Create the progress tab."""
        layout = QVBoxLayout(self.progress_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Progress chart placeholder
        self.progress_chart_frame = QFrame()
        self.progress_chart_layout = QVBoxLayout(self.progress_chart_frame)
        self.progress_chart_layout.setContentsMargins(10, 10, 10, 10)
        
        chart_label = QLabel("Learning Progress")
        chart_label.setFont(QFont("", 14, QFont.Weight.Bold))
        chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progress_chart_label = QLabel("Progress chart will be displayed here")
        self.progress_chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progress_chart_layout.addWidget(chart_label)
        self.progress_chart_layout.addWidget(self.progress_chart_label)
        
        # Daily stats
        self.daily_stats_frame = QFrame()
        self.daily_stats_layout = QVBoxLayout(self.daily_stats_frame)
        self.daily_stats_layout.setContentsMargins(10, 10, 10, 10)
        self.daily_stats_layout.setSpacing(10)
        
        daily_label = QLabel("Daily Statistics")
        daily_label.setFont(QFont("", 14, QFont.Weight.Bold))
        
        self.daily_stats_label = QLabel("No daily statistics available")
        self.daily_stats_label.setWordWrap(True)
        
        self.daily_stats_layout.addWidget(daily_label)
        self.daily_stats_layout.addWidget(self.daily_stats_label)
        
        # Add to main layout
        layout.addWidget(self.progress_chart_frame, 1)
        layout.addWidget(self.daily_stats_frame)
        layout.addStretch()
    
    def _create_weak_areas_tab(self) -> None:
        """Create the weak areas tab."""
        layout = QVBoxLayout(self.weak_areas_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Weak areas list
        self.weak_areas_frame = QFrame()
        self.weak_areas_layout = QVBoxLayout(self.weak_areas_frame)
        self.weak_areas_layout.setContentsMargins(10, 10, 10, 10)
        self.weak_areas_layout.setSpacing(10)
        
        weak_label = QLabel("Your Weak Areas")
        weak_label.setFont(QFont("", 14, QFont.Weight.Bold))
        
        self.weak_areas_label = QLabel("No weak areas identified yet")
        self.weak_areas_label.setWordWrap(True)
        
        self.weak_areas_layout.addWidget(weak_label)
        self.weak_areas_layout.addWidget(self.weak_areas_label)
        
        # Recommendations
        self.recommendations_frame = QFrame()
        self.recommendations_layout = QVBoxLayout(self.recommendations_frame)
        self.recommendations_layout.setContentsMargins(10, 10, 10, 10)
        self.recommendations_layout.setSpacing(10)
        
        rec_label = QLabel("Recommendations")
        rec_label.setFont(QFont("", 14, QFont.Weight.Bold))
        
        self.recommendations_label = QLabel("No recommendations yet")
        self.recommendations_label.setWordWrap(True)
        
        self.recommendations_layout.addWidget(rec_label)
        self.recommendations_layout.addWidget(self.recommendations_label)
        
        # Add to main layout
        layout.addWidget(self.weak_areas_frame)
        layout.addWidget(self.recommendations_frame)
        layout.addStretch()
    
    def _update_overview_tab(self) -> None:
        """Update the overview tab with current data."""
        summary = self.addon_manager.get_statistics_summary()
        
        total_exercises = summary.get('total_exercises', 0)
        accuracy = summary.get('accuracy', 0.0)
        mastery = summary.get('completion_percentage', 0.0)
        
        self.total_exercises_label.setText(f"Total Exercises: {total_exercises}")
        self.accuracy_label.setText(f"Accuracy: {accuracy:.1%}")
        self.mastery_label.setText(f"Mastery: {mastery:.0f}%")
        
        # Update recent activity
        progress = self.addon_manager.statistics_manager.get_learning_progress()
        last_activity = progress.get('last_activity', '')
        
        if last_activity:
            self.recent_activity_label.setText(f"Last activity: {last_activity}")
        else:
            self.recent_activity_label.setText("No recent activity")
    
    def _update_statistics_tab(self) -> None:
        """Update the statistics tab with current data."""
        # Get category stats
        mastery_by_category = self.addon_manager.statistics_manager.get_mastery_by_category()
        
        if mastery_by_category:
            stats_text = "<ul>"
            for category, mastery in mastery_by_category.items():
                stats_text += f"<li>{category.replace('_', ' ').title()}: {mastery:.0%} mastery</li>"
            stats_text += "</ul>"
            self.category_stats_label.setText(stats_text)
        else:
            self.category_stats_label.setText("No statistics available")
        
        # Get exercise type distribution
        type_dist = self.addon_manager.statistics_manager.get_exercise_distribution()
        
        if type_dist:
            type_text = "<ul>"
            for ex_type, count in type_dist.items():
                type_text += f"<li>{ex_type.replace('_', ' ').title()}: {count} exercises</li>"
            type_text += "</ul>"
            self.type_stats_label.setText(type_text)
        else:
            self.type_stats_label.setText("No statistics available")
    
    def _update_progress_tab(self) -> None:
        """Update the progress tab with current data."""
        # Get daily stats
        daily_stats = self.addon_manager.statistics_manager.get_daily_stats(7)
        
        if daily_stats:
            stats_text = "<table border='1' cellpadding='5'>"
            stats_text += "<tr><th>Date</th><th>Exercises</th><th>Accuracy</th></tr>"
            
            for date, stats in daily_stats.items():
                total = stats.get('total', 0)
                accuracy = stats.get('accuracy', 0.0)
                stats_text += f"<tr><td>{date}</td><td>{total}</td><td>{accuracy:.0%}</td></tr>"
            
            stats_text += "</table>"
            self.daily_stats_label.setText(stats_text)
        else:
            self.daily_stats_label.setText("No daily statistics available")
    
    def _update_weak_areas_tab(self) -> None:
        """Update the weak areas tab with current data."""
        # Get weak areas
        weak_areas = self.addon_manager.statistics_manager.get_weak_areas(10)
        
        if weak_areas:
            areas_text = "<ol>"
            for area in weak_areas:
                category = area.get('category', 'Unknown')
                accuracy = area.get('accuracy', 0.0)
                total = area.get('total_exercises', 0)
                areas_text += f"<li><b>{category.replace('_', ' ').title()}</b>: {accuracy:.0%} accuracy ({total} exercises)</li>"
            areas_text += "</ol>"
            self.weak_areas_label.setText(areas_text)
        else:
            self.weak_areas_label.setText("No weak areas identified yet. Keep practicing!")
        
        # Get recommendations
        recommendations = self.addon_manager.statistics_manager.get_adaptive_recommendations(5)
        
        if recommendations:
            rec_text = "<ul>"
            for rec in recommendations:
                ex_type = rec.get('exercise_type', 'Unknown')
                category = rec.get('category', 'Unknown')
                reason = rec.get('reason', '')
                rec_text += f"<li><b>{ex_type.replace('_', ' ').title()}</b> ({category}): {reason}</li>"
            rec_text += "</ul>"
            self.recommendations_label.setText(rec_text)
        else:
            self.recommendations_label.setText("No recommendations yet. Complete more exercises to get personalized recommendations.")
    
    def showEvent(self, event: Any) -> None:
        """Handle show event."""
        super().showEvent(event)
        self._load_data()
    
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
