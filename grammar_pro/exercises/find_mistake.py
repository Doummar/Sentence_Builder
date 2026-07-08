"""
Find the Mistake Exercise for Grammar Pro.

Mode 3: Show an incorrect sentence. The learner clicks the mistake, then corrects it.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class FindMistakeExercise(BaseExercise):
    """
    Find the Mistake Exercise.
    
    The learner is shown an incorrect sentence, clicks on the mistake,
    and then corrects it.
    """
    
    exercise_type = ExerciseType.FIND_MISTAKE
    name = "Find the Mistake"
    description = "Find and correct the mistake in the sentence."
    difficulty = ExerciseDifficulty.LEVEL_4
    grammar_categories = ["error_detection", "grammar_rules"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Find Mistake exercise."""
        self.correct_sentence: List[Word] = []
        self.incorrect_sentence: List[Word] = []
        self.mistake_position: int = -1
        self.mistake_type: str = ""
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.correct_sentence = []
        self.incorrect_sentence = []
        self.mistake_position = -1
        self.mistake_type = ""
    
    def generate(self) -> None:
        """Generate a new Find the Mistake exercise."""
        # Generate a correct sentence
        level = self.difficulty.value if isinstance(self.difficulty, ExerciseDifficulty) else 1
        self.correct_sentence = self.grammar_engine.generate_sentence(
            level=level,
            language_code=self.language
        )
        
        # Create an incorrect version by introducing a common mistake
        self.incorrect_sentence, self.mistake_position, self.mistake_type = self._introduce_mistake()
        
        # Create steps
        self.steps = [
            ExerciseStep(
                step_number=1,
                question="Click on the word that is incorrect or in the wrong position.",
                options=[word.text for word in self.incorrect_sentence],
                correct_answer=self.mistake_position,
                explanation=self._generate_explanation(),
                grammar_rule_id=self._get_relevant_rule_id()
            ),
            ExerciseStep(
                step_number=2,
                question="What should the correct word/position be?",
                options=self._get_correction_options(),
                correct_answer=self.correct_sentence[self.mistake_position].text,
                explanation=f"The correct word is '{self.correct_sentence[self.mistake_position].text}'.",
                grammar_rule_id=self._get_relevant_rule_id()
            )
        ]
        
        self.current_step_index = 0
    
    def _introduce_mistake(self) -> Tuple[List[Word], int, str]:
        """
        Introduce a common mistake into the sentence.
        
        Returns:
            Tuple of (incorrect_sentence, mistake_position, mistake_type)
        """
        if not self.correct_sentence:
            return [], -1, ""
        
        # Make a copy
        incorrect = self.correct_sentence.copy()
        
        # Choose a mistake type based on difficulty
        mistake_types = [
            self._swap_subject_verb,
            self._misplace_negation,
            self._wrong_verb_position,
            self._wrong_article,
        ]
        
        # Choose a random mistake
        mistake_func = random.choice(mistake_types)
        return mistake_func(incorrect)
    
    def _swap_subject_verb(self, sentence: List[Word]) -> Tuple[List[Word], int, str]:
        """Swap subject and verb (common mistake)."""
        subject_indices = [i for i, w in enumerate(sentence) if w.word_type == WordType.SUBJECT]
        verb_indices = [i for i, w in enumerate(sentence) if w.word_type == WordType.VERB and w.is_finite]
        
        if subject_indices and verb_indices:
            subj_idx = subject_indices[0]
            verb_idx = verb_indices[0]
            
            # Swap them
            sentence[subj_idx], sentence[verb_idx] = sentence[verb_idx], sentence[subj_idx]
            return sentence, subj_idx, "subject_verb_swap"
        
        return sentence, -1, ""
    
    def _misplace_negation(self, sentence: List[Word]) -> Tuple[List[Word], int, str]:
        """Place negation in the wrong position."""
        negation_indices = [i for i, w in enumerate(sentence) if w.word_type == WordType.NEGATION]
        verb_indices = [i for i, w in enumerate(sentence) if w.word_type == WordType.VERB and w.is_finite]
        
        if negation_indices and verb_indices:
            neg_idx = negation_indices[0]
            verb_idx = verb_indices[0]
            
            # Move negation to before the verb (wrong position for Danish)
            if neg_idx > verb_idx:
                # Already after verb, move it before
                sentence.insert(verb_idx, sentence.pop(neg_idx))
                return sentence, verb_idx, "negation_position"
            else:
                # Move it to the end
                sentence.append(sentence.pop(neg_idx))
                return sentence, len(sentence) - 1, "negation_position"
        
        return sentence, -1, ""
    
    def _wrong_verb_position(self, sentence: List[Word]) -> Tuple[List[Word], int, str]:
        """Put the verb in the wrong position."""
        verb_indices = [i for i, w in enumerate(sentence) if w.word_type == WordType.VERB and w.is_finite]
        
        if verb_indices and verb_indices[0] != 1:  # Not already in position 1
            verb_idx = verb_indices[0]
            # Move it to position 0
            sentence.insert(0, sentence.pop(verb_idx))
            return sentence, 0, "verb_position"
        
        return sentence, -1, ""
    
    def _wrong_article(self, sentence: List[Word]) -> Tuple[List[Word], int, str]:
        """Use the wrong article."""
        article_indices = [i for i, w in enumerate(sentence) if w.word_type == WordType.ARTICLE]
        
        if article_indices:
            art_idx = article_indices[0]
            # Change the article
            if sentence[art_idx].text == "en":
                sentence[art_idx] = Word(text="et", word_type=WordType.ARTICLE)
            else:
                sentence[art_idx] = Word(text="en", word_type=WordType.ARTICLE)
            return sentence, art_idx, "article"
        
        return sentence, -1, ""
    
    def _generate_explanation(self) -> str:
        """Generate explanation for the mistake."""
        if self.mistake_type == "subject_verb_swap":
            return "In Danish main clauses, the subject must come before the finite verb."
        elif self.mistake_type == "negation_position":
            return "In Danish, the negation 'ikke' comes immediately after the finite verb."
        elif self.mistake_type == "verb_position":
            return "In Danish main clauses, the finite verb must be in the second position (V2 rule)."
        elif self.mistake_type == "article":
            return "The article must match the gender of the noun. 'en' for common gender, 'et' for neuter."
        return "There is a mistake in the sentence."
    
    def _get_relevant_rule_id(self) -> str:
        """Get the relevant grammar rule ID."""
        if self.mistake_type == "subject_verb_swap":
            return "da_subject_verb"
        elif self.mistake_type == "negation_position":
            return "da_negation_ikke"
        elif self.mistake_type == "verb_position":
            return "da_v2_rule"
        elif self.mistake_type == "article":
            return "da_articles"
        return ""
    
    def _get_correction_options(self) -> List[str]:
        """Get options for correcting the mistake."""
        if self.mistake_position < 0 or self.mistake_position >= len(self.correct_sentence):
            return []
        
        correct_word = self.correct_sentence[self.mistake_position].text
        
        # Get some wrong options
        wrong_options = []
        for word in self.correct_sentence:
            if word.text != correct_word and len(wrong_options) < 3:
                wrong_options.append(word.text)
        
        # Add the correct option
        options = wrong_options + [correct_word]
        random.shuffle(options)
        
        return options
    
    def validate_answer(self, answer: Any) -> Tuple[bool, str, List[str]]:
        """
        Validate the user's answer.
        
        Args:
            answer: The user's answer (position for step 1, word for step 2)
            
        Returns:
            Tuple of (is_correct, explanation, list_of_mistake_categories)
        """
        current_step = self.current_step
        if not current_step:
            return False, "No current step.", ["internal_error"]
        
        # Step 1: User clicks on the mistake position
        if current_step.step_number == 1:
            if answer == self.mistake_position:
                return True, "Correct! Now fix the mistake.", []
            return False, "That's not the mistake. Try again.", ["error_detection"]
        
        # Step 2: User provides the correction
        if current_step.step_number == 2:
            if answer == self.correct_sentence[self.mistake_position].text:
                return True, current_step.explanation, []
            return False, f"The correct word is '{self.correct_sentence[self.mistake_position].text}'.", [self.mistake_type]
        
        return False, "Invalid answer.", ["internal_error"]
    
    def get_sentence(self) -> List[str]:
        """Get the current sentence (incorrect for step 1, correct for step 2)."""
        if self.current_step_index == 0:
            return [word.text for word in self.incorrect_sentence]
        else:
            return [word.text for word in self.correct_sentence]
    
    def get_sentence_text(self) -> str:
        """Get the current sentence as text."""
        return ' '.join(self.get_sentence())
    
    def get_mistake_position(self) -> int:
        """Get the position of the mistake."""
        return self.mistake_position
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        if current_step.step_number == 1:
            self.hints = [
                Hint(
                    level=1,
                    content="Look for words that don't follow Danish word order rules.",
                    hint_type="text"
                ),
                Hint(
                    level=2,
                    content=self._generate_explanation(),
                    hint_type="text"
                ),
                Hint(
                    level=3,
                    content=f"The mistake is at position {self.mistake_position + 1}.",
                    hint_type="highlight"
                ),
            ]
        else:
            self.hints = [
                Hint(
                    level=1,
                    content=f"The correct word should be: '{self.correct_sentence[self.mistake_position].text}'",
                    hint_type="text"
                ),
            ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'correct_sentence': [word.text for word in self.correct_sentence],
            'incorrect_sentence': [word.text for word in self.incorrect_sentence],
            'mistake_position': self.mistake_position,
            'mistake_type': self.mistake_type,
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
