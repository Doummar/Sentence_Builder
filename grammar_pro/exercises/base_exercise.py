"""
Base Exercise class for Grammar Pro.

Defines the interface that all exercise types must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..grammar.grammar_engine import GrammarEngine
    from ..config.settings import Settings


class ExerciseType(Enum):
    """Types of exercises."""
    SENTENCE_BUILDER = "sentence_builder"
    GRAMMAR_DECISION = "grammar_decision"
    FIND_MISTAKE = "find_mistake"
    MISSING_WORD = "missing_word"
    CLAUSE_TRAINER = "clause_trainer"
    TRANSFORMATION = "transformation"
    INVERSION = "inversion"
    NEGATION = "negation"
    SUBORDINATE_CLAUSE = "subordinate_clause"
    MIXED_CHALLENGE = "mixed_challenge"


class ExerciseMode(Enum):
    """Exercise modes (difficulty levels)."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class ExerciseDifficulty(Enum):
    """Difficulty levels for exercises."""
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5
    LEVEL_6 = 6
    LEVEL_7 = 7
    LEVEL_8 = 8
    LEVEL_9 = 9
    LEVEL_10 = 10
    LEVEL_11 = 11
    LEVEL_12 = 12
    LEVEL_13 = 13
    LEVEL_14 = 14


@dataclass
class ExerciseResult:
    """Result of an exercise attempt."""
    exercise_id: str
    is_correct: bool
    answer: Any
    expected_answer: Any
    response_time: float = 0.0
    confidence: int = 0  # 0-100
    mistakes: List[str] = field(default_factory=list)
    grammar_categories: List[str] = field(default_factory=list)
    hint_level: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'exercise_id': self.exercise_id,
            'is_correct': self.is_correct,
            'answer': self.answer,
            'expected_answer': self.expected_answer,
            'response_time': self.response_time,
            'confidence': self.confidence,
            'mistakes': self.mistakes,
            'grammar_categories': self.grammar_categories,
            'hint_level': self.hint_level,
            'timestamp': self.timestamp,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExerciseResult':
        """Create from dictionary."""
        return cls(
            exercise_id=data.get('exercise_id', ''),
            is_correct=data.get('is_correct', False),
            answer=data.get('answer'),
            expected_answer=data.get('expected_answer'),
            response_time=data.get('response_time', 0.0),
            confidence=data.get('confidence', 0),
            mistakes=data.get('mistakes', []),
            grammar_categories=data.get('grammar_categories', []),
            hint_level=data.get('hint_level', 0),
            timestamp=data.get('timestamp', datetime.now().isoformat()),
        )


@dataclass
class ExerciseStep:
    """A single step in a multi-step exercise."""
    step_number: int
    question: str
    options: List[str] = field(default_factory=list)
    correct_answer: Any = None
    explanation: str = ""
    grammar_rule_id: str = ""
    is_completed: bool = False
    user_answer: Any = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'step_number': self.step_number,
            'question': self.question,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'grammar_rule_id': self.grammar_rule_id,
            'is_completed': self.is_completed,
            'user_answer': self.user_answer,
        }


@dataclass
class Hint:
    """A hint for an exercise."""
    level: int  # 1-5
    content: str
    hint_type: str = "text"  # 'text', 'highlight', 'template', 'reveal_word', 'reveal_answer'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'level': self.level,
            'content': self.content,
            'hint_type': self.hint_type,
        }


class BaseExercise(ABC):
    """
    Abstract base class for all exercise types.
    
    All exercise types must inherit from this class and implement
    the required methods.
    """
    
    # Exercise metadata
    exercise_type: ExerciseType = ExerciseType.SENTENCE_BUILDER
    exercise_id: str = ""
    name: str = "Exercise"
    description: str = ""
    difficulty: ExerciseDifficulty = ExerciseDifficulty.LEVEL_1
    grammar_categories: List[str] = []
    language: str = "da"
    
    def __init__(
        self,
        grammar_engine: 'GrammarEngine',
        settings: 'Settings',
        exercise_id: str = None,
        language: str = None,
        difficulty: ExerciseDifficulty = None
    ):
        """
        Initialize the exercise.
        
        Args:
            grammar_engine: Grammar engine instance
            settings: Settings instance
            exercise_id: Optional exercise ID
            language: Optional language code
            difficulty: Optional difficulty level
        """
        self.grammar_engine = grammar_engine
        self.settings = settings
        self.exercise_id = exercise_id or self._generate_id()
        self.language = language or (settings.grammar.default_language if settings else "da")
        self.difficulty = difficulty or self.difficulty
        
        # Exercise state
        self.is_completed = False
        self.is_started = False
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.steps: List[ExerciseStep] = []
        self.current_step_index = 0
        self.results: List[ExerciseResult] = []
        self.hints: List[Hint] = []
        self.mistakes: List[str] = []
        
        # Initialize the exercise
        self._initialize()
    
    @abstractmethod
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        pass
    
    
    def _generate_id(self) -> str:
        """Generate a unique exercise ID."""
        import uuid
        return str(uuid.uuid4())
    
    @property
    def current_step(self) -> Optional[ExerciseStep]:
        """Get the current step."""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    @property
    def is_first_step(self) -> bool:
        """Check if this is the first step."""
        return self.current_step_index == 0
    
    @property
    def is_last_step(self) -> bool:
        """Check if this is the last step."""
        return self.current_step_index >= len(self.steps) - 1
    
    @abstractmethod
    def generate(self) -> None:
        """
        Generate the exercise content.
        
        This should create the sentence, questions, options, etc.
        """
        pass
    
    @abstractmethod
    def validate_answer(self, answer: Any) -> Tuple[bool, str, List[str]]:
        """
        Validate a user's answer.
        
        Args:
            answer: The user's answer
            
        Returns:
            Tuple of (is_correct, explanation, list_of_mistake_categories)
        """
        pass
    
    def start(self) -> None:
        """Start the exercise timer."""
        self.is_started = True
        self.start_time = datetime.now()
    
    def complete(self) -> None:
        """Mark the exercise as completed."""
        self.is_completed = True
        self.end_time = datetime.now()
    
    def next_step(self) -> bool:
        """
        Move to the next step.
        
        Returns:
            True if there is a next step, False if this was the last step
        """
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            return True
        return False
    
    def previous_step(self) -> bool:
        """
        Move to the previous step.
        
        Returns:
            True if there is a previous step, False if this was the first step
        """
        if self.current_step_index > 0:
            self.current_step_index -= 1
            return True
        return False
    
    def go_to_step(self, step_index: int) -> bool:
        """
        Go to a specific step.
        
        Args:
            step_index: Index of the step to go to
            
        Returns:
            True if the step exists, False otherwise
        """
        if 0 <= step_index < len(self.steps):
            self.current_step_index = step_index
            return True
        return False
    
    def submit_answer(self, answer: Any, confidence: int = 0) -> ExerciseResult:
        """
        Submit an answer and record the result.
        
        Args:
            answer: The user's answer
            confidence: User's confidence level (0-100)
            
        Returns:
            ExerciseResult with the result
        """
        if not self.is_started:
            self.start()
        
        end_time = datetime.now()
        response_time = (end_time - self.start_time).total_seconds() if self.start_time else 0
        
        is_correct, explanation, mistake_categories = self.validate_answer(answer)
        
        # Get current step info
        current_step = self.current_step
        grammar_rule_id = current_step.grammar_rule_id if current_step else ""
        
        result = ExerciseResult(
            exercise_id=self.exercise_id,
            is_correct=is_correct,
            answer=answer,
            expected_answer=current_step.correct_answer if current_step else None,
            response_time=response_time,
            confidence=confidence,
            mistakes=[explanation] if not is_correct else [],
            grammar_categories=mistake_categories,
            hint_level=0,
        )
        
        self.results.append(result)
        
        # Record the answer in the current step
        if current_step:
            current_step.user_answer = answer
            current_step.is_completed = True
        
        # If answer is correct, move to next step
        if is_correct and not self.is_last_step:
            self.next_step()
        
        return result
    
    def get_hint(self, hint_level: int = 1) -> Optional[Hint]:
        """
        Get a hint for the current step.
        
        Args:
            hint_level: Level of hint to get (1-5)
            
        Returns:
            Hint object, or None if no hint available
        """
        # Generate hints if not already generated
        if not self.hints:
            self._generate_hints()
        
        # Find hint of the requested level
        for hint in self.hints:
            if hint.level == hint_level:
                return hint
        
        # Return the closest hint
        available_levels = [h.level for h in self.hints]
        if available_levels:
            # Find the smallest level >= hint_level
            for level in sorted(available_levels):
                if level >= hint_level:
                    for hint in self.hints:
                        if hint.level == level:
                            return hint
                    break
        
        return None
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        # Default implementation - subclasses should override
        current_step = self.current_step
        if current_step:
            self.hints = [
                Hint(
                    level=1,
                    content=f"Think about the rule: {current_step.grammar_rule_id}",
                    hint_type="text"
                ),
                Hint(
                    level=2,
                    content=current_step.explanation,
                    hint_type="text"
                ),
                Hint(
                    level=5,
                    content=f"The correct answer is: {current_step.correct_answer}",
                    hint_type="reveal_answer"
                ),
            ]
    
    def get_explanation(self) -> str:
        """
        Get the explanation for the current step or exercise.
        
        Returns:
            Explanation text
        """
        current_step = self.current_step
        if current_step:
            return current_step.explanation
        return self.description
    
    def get_progress(self) -> float:
        """
        Get the progress through the exercise (0.0 to 1.0).
        
        Returns:
            Progress as a float
        """
        if not self.steps:
            return 0.0
        return self.current_step_index / len(self.steps)
    
    def get_accuracy(self) -> float:
        """
        Get the accuracy for this exercise (0.0 to 1.0).
        
        Returns:
            Accuracy as a float
        """
        if not self.results:
            return 0.0
        correct = sum(1 for r in self.results if r.is_correct)
        return correct / len(self.results)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exercise to dictionary for serialization."""
        return {
            'exercise_type': self.exercise_type.value,
            'exercise_id': self.exercise_id,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty.value,
            'grammar_categories': self.grammar_categories,
            'language': self.language,
            'is_completed': self.is_completed,
            'is_started': self.is_started,
            'current_step_index': self.current_step_index,
            'steps': [s.to_dict() for s in self.steps],
            'results': [r.to_dict() for r in self.results],
            'mistakes': self.mistakes,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], grammar_engine: 'GrammarEngine', settings: 'Settings') -> 'BaseExercise':
        """
        Create an exercise from a dictionary.
        
        This is a factory method that creates the appropriate exercise type.
        """
        exercise_type = data.get('exercise_type', '')
        
        # Map exercise type to class
        exercise_classes = {
            'sentence_builder': SentenceBuilderExercise,
            'grammar_decision': GrammarDecisionExercise,
            'find_mistake': FindMistakeExercise,
            'missing_word': MissingWordExercise,
            'clause_trainer': ClauseTrainerExercise,
            'transformation': TransformationExercise,
            'inversion': InversionExercise,
            'negation': NegationExercise,
            'subordinate_clause': SubordinateClauseExercise,
            'mixed_challenge': MixedChallengeExercise,
        }
        
        exercise_class = exercise_classes.get(exercise_type)
        if exercise_class:
            exercise = exercise_class(grammar_engine, settings)
            # Restore state from dict
            exercise.exercise_id = data.get('exercise_id', '')
            exercise.name = data.get('name', '')
            exercise.description = data.get('description', '')
            exercise.difficulty = ExerciseDifficulty(data.get('difficulty', 1))
            exercise.grammar_categories = data.get('grammar_categories', [])
            exercise.language = data.get('language', 'da')
            exercise.is_completed = data.get('is_completed', False)
            exercise.is_started = data.get('is_started', False)
            exercise.current_step_index = data.get('current_step_index', 0)
            
            # Restore steps
            for step_data in data.get('steps', []):
                step = ExerciseStep(
                    step_number=step_data.get('step_number', 0),
                    question=step_data.get('question', ''),
                    options=step_data.get('options', []),
                    correct_answer=step_data.get('correct_answer'),
                    explanation=step_data.get('explanation', ''),
                    grammar_rule_id=step_data.get('grammar_rule_id', ''),
                    is_completed=step_data.get('is_completed', False),
                    user_answer=step_data.get('user_answer'),
                )
                exercise.steps.append(step)
            
            # Restore results
            for result_data in data.get('results', []):
                result = ExerciseResult.from_dict(result_data)
                exercise.results.append(result)
            
            exercise.mistakes = data.get('mistakes', [])
            
            return exercise
        
        # Fallback to base class
        raise ValueError(f"Unknown exercise type: {exercise_type}")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.exercise_id}, type={self.exercise_type.value})"


# Import concrete exercise classes for from_dict to work
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
