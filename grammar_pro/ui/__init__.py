"""
UI module for Grammar Pro.

Provides all user interface components for the addon.
"""

from .main_window import MainWindow
from .exercise_window import ExerciseWindow
from .dashboard import DashboardWindow
from .settings_dialog import SettingsDialog
from .exercise_builder import ExerciseBuilderWindow
from .widgets import (
    WordDragWidget,
    SentenceBuilderWidget,
    GrammarDecisionWidget,
    FindMistakeWidget,
    ProgressBar,
    StatisticsChart,
)

__all__ = [
    "MainWindow",
    "ExerciseWindow",
    "DashboardWindow",
    "SettingsDialog",
    "ExerciseBuilderWindow",
    "WordDragWidget",
    "SentenceBuilderWidget",
    "GrammarDecisionWidget",
    "FindMistakeWidget",
    "ProgressBar",
    "StatisticsChart",
]
