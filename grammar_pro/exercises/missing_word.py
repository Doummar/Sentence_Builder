"""
Missing Word Exercise for Grammar Pro.

Mode 4: Some words are already placed. The learner inserts the missing parts.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class MissingWordExercise(BaseExercise):
    """
    Missing Word Exercise.
    
    Some words are already placed. The learner inserts the missing parts.
    """
    
    exercise_type = ExerciseType.MISSING_WORD
    name = "Missing Word Order"
    description = "Some words are already placed. Insert the missing parts."
    difficulty = ExerciseDifficulty.LEVEL_5
    grammar_categories = ["word_order", "grammar_rules"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Missing Word exercise."""
        self.correct_sentence: List[Word] = []
        self.partial_sentence: List[Optional[Word]] = []  # None for missing positions
        self.missing_positions: List[int] = []
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.correct_sentence = []
        self.partial_sentence = []
        self.missing_positions = []
    
    def generate(self) -> None:
        """Generate a new Missing Word exercise."""
        # Generate a correct sentence
        level = self.difficulty.value if isinstance(self.difficulty, ExerciseDifficulty) else 1
        self.correct_sentence = self.grammar_engine.generate_sentence(
            level=level,
            language_code=self.language
        )
        
        # Create partial sentence with some words missing
        self.partial_sentence, self.missing_positions = self._create_partial_sentence()
        
        # Create steps for each missing word
        self.steps = []
        for i, pos in enumerate(self.missing_positions):
            step_number = i + 1
            
            # Get the correct word
            correct_word = self.correct_sentence[pos]
            
            # Get options (correct word + some wrong options)
            options = self._get_options(correct_word)
            
            self.steps.append(ExerciseStep(
                step_number=step_number,
                question=f"What word should go in position {pos + 1}?",
                options=options,
                correct_answer=correct_word.text,
                explanation=self._get_explanation(pos),
                grammar_rule_id=self._get_relevant_rule_id(pos)
            ))
        
        self.current_step_index = 0
    
    def _create_partial_sentence(self) -> Tuple[List[Optional[Word]], List[int]]:
        """Create a partial sentence with some words missing."""
        if not self.correct_sentence:
            return [], []
        
        # Decide how many words to hide based on difficulty
        num_missing = min(3, len(self.correct_sentence) // 2)
        
        # Choose positions to hide (avoid hiding subject or finite verb in early levels)
        all_positions = list(range(len(self.correct_sentence)))
        
        # Don't hide subject or finite verb for beginners
        subject_pos = next((i for i, w in enumerate(self.correct_sentence) if w.word_type == WordType.SUBJECT), None)
        verb_pos = next((i for i, w in enumerate(self.correct_sentence) if w.word_type == WordType.VERB and w.is_finite), None)
        
        protected_positions = set()
        if subject_pos is not None:
            protected_positions.add(subject_pos)
        if verb_pos is not None:
            protected_positions.add(verb_pos)
        
        # Choose missing positions
        available_positions = [p for p in all_positions if p not in protected_positions]
        missing_positions = random.sample(available_positions, min(num_missing, len(available_positions)))
        
        # Create partial sentence
        partial = []
        for i in range(len(self.correct_sentence)):
            if i in missing_positions:
                partial.append(None)
            else:
                partial.append(self.correct_sentence[i])
        
        return partial, missing_positions
    
    def _get_options(self, correct_word: Word) -> List[str]:
        """Get options for a missing word."""
        # Get some wrong options from the sentence
        options = []
        for word in self.correct_sentence:
            if word.text != correct_word.text and len(options) < 3:
                options.append(word.text)
        
        # Add the correct option
        options.append(correct_word.text)
        random.shuffle(options)
        
        return options
    
    def _get_explanation(self, position: int) -> str:
        """Get explanation for a position."""
        correct_word = self.correct_sentence[position]
        
        if correct_word.word_type == WordType.SUBJECT:
            return f"This is the subject position. The subject is '{correct_word.text}'."
        elif correct_word.word_type == WordType.VERB and correct_word.is_finite:
            return f"This is the finite verb position. In Danish main clauses, the verb must be in position 2."
        elif correct_word.word_type == WordType.NEGATION:
            return f"The negation 'ikke' comes immediately after the finite verb."
        else:
            return f"The correct word is '{correct_word.text}'."
    
    def _get_relevant_rule_id(self, position: int) -> str:
        """Get the relevant grammar rule ID."""
        correct_word = self.correct_sentence[position]
        
        if correct_word.word_type == WordType.SUBJECT:
            return "da_subject_verb"
        elif correct_word.word_type == WordType.VERB and correct_word.is_finite:
            return "da_v2_rule"
        elif correct_word.word_type == WordType.NEGATION:
            return "da_negation_ikke"
        
        return ""
    
    def validate_answer(self, answer: Any) -> Tuple[bool, str, List[str]]:
        """
        Validate the user's answer.
        
        Args:
            answer: The user's answer (word text)
            
        Returns:
            Tuple of (is_correct, explanation, list_of_mistake_categories)
        """
        current_step = self.current_step
        if not current_step:
            return False, "No current step.", ["internal_error"]
        
        if answer == current_step.correct_answer:
            # Fill in the missing word
            if self.current_step_index < len(self.missing_positions):
                pos = self.missing_positions[self.current_step_index]
                self.partial_sentence[pos] = self.correct_sentence[pos]
            
            return True, current_step.explanation, []
        
        # Determine mistake category
        mistake_categories = []
        if current_step.grammar_rule_id:
            if "v2" in current_step.grammar_rule_id:
                mistake_categories.append("word_order")
            elif "negation" in current_step.grammar_rule_id:
                mistake_categories.append("negation")
            else:
                mistake_categories.append("grammar")
        
        return False, current_step.explanation, mistake_categories
    
    def get_partial_sentence(self) -> List[str]:
        """Get the partial sentence with placeholders for missing words."""
        result = []
        for word in self.partial_sentence:
            if word is None:
                result.append("___")
            else:
                result.append(word.text)
        return result
    
    def get_partial_sentence_text(self) -> str:
        """Get the partial sentence as text."""
        return ' '.join(self.get_partial_sentence())
    
    def get_correct_sentence_text(self) -> str:
        """Get the correct sentence as text."""
        return ' '.join(word.text for word in self.correct_sentence)
    
    def get_missing_positions(self) -> List[int]:
        """Get the positions of missing words."""
        return self.missing_positions
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        self.hints = [
            Hint(
                level=1,
                content=f"Think about what type of word should go here.",
                hint_type="text"
            ),
            Hint(
                level=2,
                content=current_step.explanation,
                hint_type="text"
            ),
            Hint(
                level=5,
                content=f"The correct word is: '{current_step.correct_answer}'",
                hint_type="reveal_word"
            ),
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'correct_sentence': [word.text for word in self.correct_sentence],
            'partial_sentence': [word.text if word else None for word in self.partial_sentence],
            'missing_positions': self.missing_positions,
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
