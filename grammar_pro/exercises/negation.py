"""
Negation Trainer Exercise for Grammar Pro.

Mode 8: Practice only placement of "ikke".
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class NegationExercise(BaseExercise):
    """
    Negation Trainer Exercise.
    
    Practice the placement of the negation word "ikke" in Danish sentences.
    """
    
    exercise_type = ExerciseType.NEGATION
    name = "Negation Trainer"
    description = "Practice the placement of 'ikke' (not) in Danish sentences."
    difficulty = ExerciseDifficulty.LEVEL_7
    grammar_categories = ["negation"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Negation exercise."""
        self.positive_sentence: List[Word] = []
        self.negative_sentence: List[Word] = []
        self.verb_position: int = -1
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.positive_sentence = []
        self.negative_sentence = []
        self.verb_position = -1
    
    def generate(self) -> None:
        """Generate a new Negation exercise."""
        # Generate a positive sentence
        level = self.difficulty.value if isinstance(self.difficulty, ExerciseDifficulty) else 7
        self.positive_sentence = self.grammar_engine.generate_sentence(
            level=level,
            language_code=self.language
        )
        
        # Find the finite verb position
        verb_indices = [i for i, w in enumerate(self.positive_sentence) if w.word_type == WordType.VERB and w.is_finite]
        if verb_indices:
            self.verb_position = verb_indices[0]
        
        # Create the negative sentence by adding "ikke" after the verb
        self.negative_sentence = self.positive_sentence.copy()
        ikke = self.grammar_engine.get_word("ikke", self.language)
        if ikke and self.verb_position >= 0:
            self.negative_sentence.insert(self.verb_position + 1, ikke)
        
        # Create steps
        self.steps = [
            ExerciseStep(
                step_number=1,
                question=f"Where should 'ikke' be placed in this sentence?",
                options=self._get_position_options(),
                correct_answer=self.verb_position + 1,  # Position after the verb
                explanation=f"In Danish, 'ikke' comes immediately after the finite verb. The verb is at position {self.verb_position + 1}, so 'ikke' goes at position {self.verb_position + 2}.",
                grammar_rule_id="da_negation_ikke"
            )
        ]
        
        self.current_step_index = 0
    
    def _get_position_options(self) -> List[str]:
        """Get position options for placing 'ikke'."""
        if not self.positive_sentence:
            return []
        
        options = []
        for i in range(len(self.positive_sentence) + 1):
            if i == 0:
                options.append("Before the first word")
            elif i == len(self.positive_sentence):
                options.append("After the last word")
            else:
                options.append(f"After position {i}")
        
        return options
    
    def validate_answer(self, answer: Any) -> Tuple[bool, str, List[str]]:
        """
        Validate the user's answer.
        
        Args:
            answer: The user's answer (position index or description)
            
        Returns:
            Tuple of (is_correct, explanation, list_of_mistake_categories)
        """
        current_step = self.current_step
        if not current_step:
            return False, "No current step.", ["internal_error"]
        
        # Parse the answer
        if isinstance(answer, int):
            user_position = answer
        elif isinstance(answer, str):
            # Parse string descriptions like "After position 2"
            if answer.startswith("After position "):
                try:
                    user_position = int(answer.replace("After position ", ""))
                except ValueError:
                    user_position = -1
            elif answer == "Before the first word":
                user_position = 0
            elif answer == "After the last word":
                user_position = len(self.positive_sentence)
            else:
                user_position = -1
        else:
            user_position = -1
        
        if user_position == self.verb_position + 1:
            return True, current_step.explanation, []
        
        return False, current_step.explanation, ["negation"]
    
    def get_positive_sentence(self) -> List[str]:
        """Get the positive sentence."""
        return [word.text for word in self.positive_sentence]
    
    def get_negative_sentence(self) -> List[str]:
        """Get the negative sentence."""
        return [word.text for word in self.negative_sentence]
    
    def get_verb_position(self) -> int:
        """Get the position of the finite verb."""
        return self.verb_position
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        verb_word = None
        if self.verb_position >= 0 and self.verb_position < len(self.positive_sentence):
            verb_word = self.positive_sentence[self.verb_position].text
        
        self.hints = [
            Hint(
                level=1,
                content="In Danish, 'ikke' comes immediately after the finite verb.",
                hint_type="text"
            ),
            Hint(
                level=2,
                content=f"The finite verb is '{verb_word}'. 'ikke' should come right after it." if verb_word else "Find the finite verb first.",
                hint_type="text"
            ),
            Hint(
                level=3,
                content=f"The verb is at position {self.verb_position + 1}. 'ikke' goes at position {self.verb_position + 2}.",
                hint_type="text"
            ),
            Hint(
                level=5,
                content=f"'ikke' should be placed after '{verb_word}'" if verb_word else "",
                hint_type="reveal_word"
            ),
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'positive_sentence': [word.text for word in self.positive_sentence],
            'negative_sentence': [word.text for word in self.negative_sentence],
            'verb_position': self.verb_position,
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
