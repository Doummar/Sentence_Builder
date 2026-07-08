"""
Exercises module for Grammar Pro.

Provides exercise generation, validation, and management.
"""

from .exercise_manager import ExerciseManager
from .base_exercise import BaseExercise, ExerciseType, ExerciseMode
from .sentence_builder import SentenceBuilderExercise
from .grammar_decision import GrammarDecisionExercise
from .find_mistake import FindMistakeExercise
from .missing_word import MissingWordExercise
from .clause_trainer import ClauseTrainerExercise
from .transformation import TransformationExercise
from .inversion import InversionExercise
from .negation import NegationExercise
from .subordinate_clause import SubordinateClauseExercise
from .mixed_challenge import MixedChallengeExercise

__all__ = [
    "ExerciseManager",
    "BaseExercise",
    "ExerciseType",
    "ExerciseMode",
    "SentenceBuilderExercise",
    "GrammarDecisionExercise",
    "FindMistakeExercise",
    "MissingWordExercise",
    "ClauseTrainerExercise",
    "TransformationExercise",
    "InversionExercise",
    "NegationExercise",
    "SubordinateClauseExercise",
    "MixedChallengeExercise",
]
