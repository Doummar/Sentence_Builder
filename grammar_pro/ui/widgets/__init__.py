"""
Widgets module for Grammar Pro UI.

Provides custom widgets for different exercise types.
"""

from .sentence_builder_widget import SentenceBuilderWidget
from .grammar_decision_widget import GrammarDecisionWidget
from .find_mistake_widget import FindMistakeWidget
from .missing_word_widget import MissingWordWidget
from .word_drag_widget import WordDragWidget
from .progress_bar import ProgressBar
from .statistics_chart import StatisticsChart

__all__ = [
    "SentenceBuilderWidget",
    "GrammarDecisionWidget",
    "FindMistakeWidget",
    "MissingWordWidget",
    "WordDragWidget",
    "ProgressBar",
    "StatisticsChart",
]
