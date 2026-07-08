"""
Exercise Manager for Grammar Pro.

Manages exercise generation, selection, and tracking.
"""

import random
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from .base_exercise import (
    BaseExercise,
    ExerciseDifficulty,
    ExerciseMode,
    ExerciseType,
)
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

if TYPE_CHECKING:
    from ..grammar.grammar_engine import GrammarEngine
    from ..config.settings import Settings
    from ..statistics.statistics_manager import StatisticsManager


class ExerciseManager:
    """
    Manages all exercises for Grammar Pro.
    
    Responsibilities:
    - Generate exercises based on criteria
    - Track exercise history
    - Manage adaptive learning (more exercises for weak areas)
    - Provide exercise recommendations
    """
    
    def __init__(
        self,
        grammar_engine: 'GrammarEngine',
        settings: 'Settings',
        statistics_manager: 'StatisticsManager' = None
    ):
        """
        Initialize the Exercise Manager.
        
        Args:
            grammar_engine: Grammar engine instance
            settings: Settings instance
            statistics_manager: Optional statistics manager for adaptive learning
        """
        self.grammar_engine = grammar_engine
        self.settings = settings
        self.statistics_manager = statistics_manager
        
        # Exercise registry
        self._exercise_classes = {
            ExerciseType.SENTENCE_BUILDER: SentenceBuilderExercise,
            ExerciseType.GRAMMAR_DECISION: GrammarDecisionExercise,
            ExerciseType.FIND_MISTAKE: FindMistakeExercise,
            ExerciseType.MISSING_WORD: MissingWordExercise,
            ExerciseType.CLAUSE_TRAINER: ClauseTrainerExercise,
            ExerciseType.TRANSFORMATION: TransformationExercise,
            ExerciseType.INVERSION: InversionExercise,
            ExerciseType.NEGATION: NegationExercise,
            ExerciseType.SUBORDINATE_CLAUSE: SubordinateClauseExercise,
            ExerciseType.MIXED_CHALLENGE: MixedChallengeExercise,
        }
        
        # Exercise history
        self._exercise_history: List[BaseExercise] = []
        
        # Current session
        self._current_session: List[BaseExercise] = []
        
        # Adaptive learning state
        self._weak_areas: Dict[str, int] = {}  # category -> count
        self._strong_areas: Dict[str, int] = {}  # category -> count
    
    def shutdown(self) -> None:
        """Clean up resources."""
        self._exercise_history.clear()
        self._current_session.clear()
        self._weak_areas.clear()
        self._strong_areas.clear()
    
    def get_available_modes(self) -> List[Dict[str, Any]]:
        """
        Get list of available exercise modes.
        
        Returns:
            List of mode descriptors
        """
        modes = []
        for exercise_type, exercise_class in self._exercise_classes.items():
            modes.append({
                'id': exercise_type.value,
                'name': exercise_class.exercise_type.name.replace('_', ' ').title(),
                'description': getattr(exercise_class, 'description', ''),
                'difficulty': getattr(exercise_class, 'difficulty', ExerciseDifficulty.LEVEL_1).value,
                'categories': getattr(exercise_class, 'grammar_categories', []),
            })
        return modes
    
    def get_mode_by_id(self, mode_id: str) -> Optional[ExerciseType]:
        """
        Get exercise type by mode ID.
        
        Args:
            mode_id: Mode identifier
            
        Returns:
            ExerciseType, or None if not found
        """
        for exercise_type in ExerciseType:
            if exercise_type.value == mode_id:
                return exercise_type
        return None
    
    def create_exercise(
        self,
        exercise_type: ExerciseType = None,
        language: str = None,
        difficulty: ExerciseDifficulty = None,
        grammar_category: str = None,
        template_id: str = None,
        level: int = None
    ) -> BaseExercise:
        """
        Create a new exercise.
        
        Args:
            exercise_type: Type of exercise to create
            language: Language code
            difficulty: Difficulty level
            grammar_category: Specific grammar category to focus on
            template_id: Specific template to use
            level: Specific level to use
            
        Returns:
            New exercise instance
        """
        # Determine exercise type
        if exercise_type is None:
            # Choose based on adaptive learning or random
            exercise_type = self._select_exercise_type(grammar_category)
        
        # Get the exercise class
        exercise_class = self._exercise_classes.get(exercise_type)
        if exercise_class is None:
            raise ValueError(f"Unknown exercise type: {exercise_type}")
        
        # Determine language
        if language is None:
            language = self.settings.grammar.default_language if self.settings else "da"
        
        # Determine difficulty
        if difficulty is None:
            if self.settings and self.settings.grammar.progressive_difficulty:
                # Use the user's current level
                current_level = getattr(self.settings.grammar, 'current_level', 1)
                difficulty = ExerciseDifficulty(current_level)
            else:
                difficulty = ExerciseDifficulty.LEVEL_1
        
        # Create the exercise
        exercise = exercise_class(
            grammar_engine=self.grammar_engine,
            settings=self.settings,
            language=language,
            difficulty=difficulty
        )
        
        # Set additional parameters
        if grammar_category:
            exercise.grammar_categories = [grammar_category]
        if template_id:
            exercise.template_id = template_id
        if level:
            exercise.difficulty = ExerciseDifficulty(level)
        
        # Generate the exercise
        exercise.generate()
        
        return exercise
    
    def _select_exercise_type(self, grammar_category: str = None) -> ExerciseType:
        """
        Select an exercise type based on adaptive learning.
        
        Args:
            grammar_category: Optional grammar category to focus on
            
        Returns:
            Selected ExerciseType
        """
        # If a specific category is requested, choose exercises that target it
        if grammar_category:
            # Map categories to exercise types
            category_exercises = {
                'word_order': [ExerciseType.SENTENCE_BUILDER, ExerciseType.INVERSION],
                'negation': [ExerciseType.NEGATION, ExerciseType.FIND_MISTAKE],
                'questions': [ExerciseType.GRAMMAR_DECISION, ExerciseType.TRANSFORMATION],
                'clauses': [ExerciseType.CLAUSE_TRAINER, ExerciseType.SUBORDINATE_CLAUSE],
                'verbs': [ExerciseType.TRANSFORMATION, ExerciseType.SENTENCE_BUILDER],
            }
            
            if grammar_category in category_exercises:
                return random.choice(category_exercises[grammar_category])
        
        # Check for weak areas from adaptive learning
        if self.statistics_manager and self.settings and self.settings.grammar.adaptive_learning:
            weak_areas = self.statistics_manager.get_weak_areas(limit=5)
            if weak_areas:
                # Map weak area categories to exercise types
                for weak_area in weak_areas:
                    category = weak_area.get('category', '')
                    if category in category_exercises:
                        return random.choice(category_exercises[category])
        
        # Default: choose randomly from all types
        return random.choice(list(self._exercise_classes.keys()))
    
    def create_session(
        self,
        num_exercises: int = 20,
        mode: str = None,
        language: str = None,
        difficulty: ExerciseDifficulty = None,
        grammar_categories: List[str] = None
    ) -> List[BaseExercise]:
        """
        Create a session with multiple exercises.
        
        Args:
            num_exercises: Number of exercises to create
            mode: Specific mode to use (optional)
            language: Language code
            difficulty: Difficulty level
            grammar_categories: List of grammar categories to focus on
            
        Returns:
            List of exercises
        """
        exercises = []
        
        # Determine mode
        exercise_type = None
        if mode:
            exercise_type = self.get_mode_by_id(mode)
        
        # Create exercises
        for _ in range(num_exercises):
            # Choose a category if multiple are specified
            category = None
            if grammar_categories:
                category = random.choice(grammar_categories)
            
            exercise = self.create_exercise(
                exercise_type=exercise_type,
                language=language,
                difficulty=difficulty,
                grammar_category=category
            )
            exercises.append(exercise)
        
        # Start a new session
        self._current_session = exercises
        
        return exercises
    
    def get_next_exercise(
        self,
        mode: str = None,
        language: str = None,
        difficulty: ExerciseDifficulty = None
    ) -> BaseExercise:
        """
        Get the next exercise in the current session or create a new one.
        
        Args:
            mode: Specific mode to use
            language: Language code
            difficulty: Difficulty level
            
        Returns:
            Next exercise
        """
        # If there are exercises in the current session, return the next one
        if self._current_session:
            exercise = self._current_session.pop(0)
            return exercise
        
        # Otherwise, create a new exercise
        exercise_type = None
        if mode:
            exercise_type = self.get_mode_by_id(mode)
        
        return self.create_exercise(
            exercise_type=exercise_type,
            language=language,
            difficulty=difficulty
        )
    
    def record_exercise_result(self, exercise: BaseExercise) -> None:
        """
        Record the result of an exercise.
        
        Args:
            exercise: Completed exercise
        """
        # Add to history
        self._exercise_history.append(exercise)
        
        # Keep history size manageable
        max_history = 1000
        if len(self._exercise_history) > max_history:
            self._exercise_history = self._exercise_history[-max_history:]
        
        # Update adaptive learning state
        self._update_adaptive_learning(exercise)
        
        # Update statistics
        if self.statistics_manager:
            self.statistics_manager.record_exercise(exercise)
    
    def _update_adaptive_learning(self, exercise: BaseExercise) -> None:
        """
        Update adaptive learning state based on exercise results.
        
        Args:
            exercise: Completed exercise
        """
        if not self.settings or not self.settings.grammar.adaptive_learning:
            return
        
        # Analyze mistakes
        for result in exercise.results:
            for category in result.grammar_categories:
                if not result.is_correct:
                    # Increment weak area count
                    self._weak_areas[category] = self._weak_areas.get(category, 0) + 1
                else:
                    # Increment strong area count
                    self._strong_areas[category] = self._strong_areas.get(category, 0) + 1
    
    def get_weak_areas(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the user's weakest grammar areas.
        
        Args:
            limit: Maximum number of weak areas to return
            
        Returns:
            List of weak area descriptors
        """
        # Sort by count (descending)
        sorted_weak = sorted(self._weak_areas.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        for category, count in sorted_weak[:limit]:
            result.append({
                'category': category,
                'mistake_count': count,
                'type': 'weak'
            })
        
        return result
    
    def get_strong_areas(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the user's strongest grammar areas.
        
        Args:
            limit: Maximum number of strong areas to return
            
        Returns:
            List of strong area descriptors
        """
        # Sort by count (descending)
        sorted_strong = sorted(self._strong_areas.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        for category, count in sorted_strong[:limit]:
            result.append({
                'category': category,
                'correct_count': count,
                'type': 'strong'
            })
        
        return result
    
    def get_recommended_exercises(
        self,
        num_recommendations: int = 10,
        language: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get recommended exercises based on adaptive learning.
        
        Args:
            num_recommendations: Number of recommendations to return
            language: Language code
            
        Returns:
            List of exercise recommendations
        """
        recommendations = []
        
        # Get weak areas
        weak_areas = self.get_weak_areas()
        
        # Map categories to exercise types
        category_exercises = {
            'word_order': [ExerciseType.SENTENCE_BUILDER, ExerciseType.INVERSION],
            'negation': [ExerciseType.NEGATION, ExerciseType.FIND_MISTAKE],
            'questions': [ExerciseType.GRAMMAR_DECISION, ExerciseType.TRANSFORMATION],
            'clauses': [ExerciseType.CLAUSE_TRAINER, ExerciseType.SUBORDINATE_CLAUSE],
            'verbs': [ExerciseType.TRANSFORMATION, ExerciseType.SENTENCE_BUILDER],
        }
        
        # Recommend exercises for weak areas
        for weak_area in weak_areas:
            category = weak_area['category']
            if category in category_exercises:
                for exercise_type in category_exercises[category]:
                    recommendations.append({
                        'exercise_type': exercise_type.value,
                        'name': exercise_type.name.replace('_', ' ').title(),
                        'category': category,
                        'reason': f"You struggle with {category}",
                        'priority': weak_area['mistake_count']
                    })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        # Return top recommendations
        return recommendations[:num_recommendations]
    
    def get_exercise_history(self, limit: int = 100) -> List[BaseExercise]:
        """
        Get the user's exercise history.
        
        Args:
            limit: Maximum number of exercises to return
            
        Returns:
            List of exercises
        """
        return self._exercise_history[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about exercises.
        
        Returns:
            Dictionary with statistics
        """
        total_exercises = len(self._exercise_history)
        
        if total_exercises == 0:
            return {
                'total_exercises': 0,
                'correct_count': 0,
                'incorrect_count': 0,
                'accuracy': 0.0,
                'average_response_time': 0.0,
                'exercises_by_type': {},
                'exercises_by_category': {},
            }
        
        # Count correct/incorrect
        correct_count = 0
        incorrect_count = 0
        total_response_time = 0.0
        exercises_by_type: Dict[str, int] = {}
        exercises_by_category: Dict[str, int] = {}
        
        for exercise in self._exercise_history:
            # Count by type
            exercise_type = exercise.exercise_type.value
            exercises_by_type[exercise_type] = exercises_by_type.get(exercise_type, 0) + 1
            
            # Count by category
            for category in exercise.grammar_categories:
                exercises_by_category[category] = exercises_by_category.get(category, 0) + 1
            
            # Count results
            for result in exercise.results:
                if result.is_correct:
                    correct_count += 1
                else:
                    incorrect_count += 1
                total_response_time += result.response_time
        
        accuracy = correct_count / (correct_count + incorrect_count) if (correct_count + incorrect_count) > 0 else 0.0
        average_response_time = total_response_time / total_exercises if total_exercises > 0 else 0.0
        
        return {
            'total_exercises': total_exercises,
            'correct_count': correct_count,
            'incorrect_count': incorrect_count,
            'accuracy': accuracy,
            'average_response_time': average_response_time,
            'exercises_by_type': exercises_by_type,
            'exercises_by_category': exercises_by_category,
        }
    
    def clear_history(self) -> None:
        """Clear the exercise history."""
        self._exercise_history.clear()
        self._weak_areas.clear()
        self._strong_areas.clear()
    
    def get_exercise_by_id(self, exercise_id: str) -> Optional[BaseExercise]:
        """
        Get an exercise by its ID.
        
        Args:
            exercise_id: Exercise ID
            
        Returns:
            Exercise, or None if not found
        """
        # Search in history
        for exercise in self._exercise_history:
            if exercise.exercise_id == exercise_id:
                return exercise
        
        # Search in current session
        for exercise in self._current_session:
            if exercise.exercise_id == exercise_id:
                return exercise
        
        return None
