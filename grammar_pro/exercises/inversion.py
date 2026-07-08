"""
Inversion Practice Exercise for Grammar Pro.

Mode 7: Practice only V2 word order with hundreds of examples.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class InversionExercise(BaseExercise):
    """
    Inversion Practice Exercise.
    
    Practice the V2 word order rule with various sentence patterns.
    """
    
    exercise_type = ExerciseType.INVERSION
    name = "Inversion Practice"
    description = "Practice V2 word order: the finite verb must be in the second position."
    difficulty = ExerciseDifficulty.LEVEL_11
    grammar_categories = ["word_order", "v2_rule"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Inversion exercise."""
        self.correct_sentence: List[Word] = []
        self.shuffled_words: List[Word] = []
        self.first_element_type: str = ""
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.correct_sentence = []
        self.shuffled_words = []
        self.first_element_type = ""
    
    def generate(self) -> None:
        """Generate a new Inversion exercise."""
        # Generate a sentence that demonstrates V2 rule
        # We want sentences where the first element is NOT the subject
        # to really test the V2 rule
        
        # Try to generate a sentence with an adverb or time expression first
        level = self.difficulty.value if isinstance(self.difficulty, ExerciseDifficulty) else 11
        
        # Generate multiple sentences until we get one with non-subject first
        for _ in range(10):
            sentence = self.grammar_engine.generate_sentence(
                level=level,
                language_code=self.language
            )
            
            if sentence and len(sentence) >= 2:
                first_word = sentence[0]
                if first_word.word_type != WordType.SUBJECT:
                    self.correct_sentence = sentence
                    self.first_element_type = first_word.word_type.value
                    break
        
        # If we didn't find a good one, use any sentence
        if not self.correct_sentence:
            self.correct_sentence = self.grammar_engine.generate_sentence(
                level=level,
                language_code=self.language
            )
            if self.correct_sentence:
                self.first_element_type = self.correct_sentence[0].word_type.value
        
        # Shuffle the words
        self.shuffled_words = self.correct_sentence.copy()
        random.shuffle(self.shuffled_words)
        
        # Create step
        self.steps = [
            ExerciseStep(
                step_number=1,
                question="Arrange the words so that the finite verb is in the second position (V2 rule).",
                options=[word.text for word in self.shuffled_words],
                correct_answer=[word.text for word in self.correct_sentence],
                explanation=self._generate_explanation(),
                grammar_rule_id="da_v2_rule"
            )
        ]
        
        self.current_step_index = 0
    
    def _generate_explanation(self) -> str:
        """Generate explanation for V2 rule."""
        if not self.correct_sentence or len(self.correct_sentence) < 2:
            return "The V2 rule states that the finite verb must be in the second position."
        
        first_word = self.correct_sentence[0]
        verb_word = self.correct_sentence[1] if len(self.correct_sentence) > 1 else None
        
        if verb_word and verb_word.word_type == WordType.VERB and verb_word.is_finite:
            return (f"The sentence starts with '{first_word.text}' (a {self.first_element_type}). "
                    f"The finite verb '{verb_word.text}' is in the second position, following the V2 rule.")
        
        return "In Danish main clauses, the finite verb must always be in the second position."
    
    def validate_answer(self, answer: Any) -> Tuple[bool, str, List[str]]:
        """
        Validate the user's answer.
        
        Args:
            answer: List of word texts
            
        Returns:
            Tuple of (is_correct, explanation, list_of_mistake_categories)
        """
        if not isinstance(answer, list):
            return False, "Please provide a list of words.", ["invalid_answer"]
        
        # Check if the order matches
        correct_texts = [word.text for word in self.correct_sentence]
        if answer == correct_texts:
            return True, "Correct! The finite verb is in the second position.", []
        
        # Check if verb is in second position
        user_words = []
        for word_text in answer:
            word = self.grammar_engine.get_word(word_text, self.language)
            if word:
                user_words.append(word)
            else:
                user_words.append(Word(text=word_text, word_type=WordType.OTHER))
        
        verb_indices = [i for i, w in enumerate(user_words) if w.word_type == WordType.VERB and w.is_finite]
        
        if verb_indices and verb_indices[0] == 1:
            # Verb is in second position, but other words are wrong
            return False, "The verb is in the correct position, but other words are not in the right order.", ["word_order"]
        elif verb_indices:
            return False, f"The finite verb should be in the second position, but it's in position {verb_indices[0] + 1}.", ["v2_rule"]
        else:
            return False, "There should be a finite verb in the sentence.", ["verbs"]
    
    def get_shuffled_words(self) -> List[str]:
        """Get the shuffled words."""
        return [word.text for word in self.shuffled_words]
    
    def get_correct_sentence(self) -> List[str]:
        """Get the correct sentence."""
        return [word.text for word in self.correct_sentence]
    
    def get_first_element_type(self) -> str:
        """Get the type of the first element."""
        return self.first_element_type
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        correct_words = [word.text for word in self.correct_sentence]
        
        self.hints = [
            Hint(
                level=1,
                content="The V2 rule: the finite verb must be in the second position.",
                hint_type="text"
            ),
            Hint(
                level=2,
                content=f"The first word is '{correct_words[0]}' (a {self.first_element_type}).",
                hint_type="text"
            ),
            Hint(
                level=3,
                content=f"The finite verb is '{correct_words[1] if len(correct_words) > 1 else ''}'.",
                hint_type="text"
            ),
            Hint(
                level=4,
                content=f"The first word is: '{correct_words[0]}'",
                hint_type="reveal_word"
            ),
            Hint(
                level=5,
                content=f"The correct sentence is: '{' '.join(correct_words)}'",
                hint_type="reveal_answer"
            ),
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'correct_sentence': [word.text for word in self.correct_sentence],
            'shuffled_words': [word.text for word in self.shuffled_words],
            'first_element_type': self.first_element_type,
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
