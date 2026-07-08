"""
Mixed Challenge Exercise for Grammar Pro.

Mode 10: Everything combined - a comprehensive challenge.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class MixedChallengeExercise(BaseExercise):
    """
    Mixed Challenge Exercise.
    
    A comprehensive challenge that combines multiple grammar concepts.
    """
    
    exercise_type = ExerciseType.MIXED_CHALLENGE
    name = "Mixed Challenge"
    description = "A comprehensive challenge combining multiple grammar concepts."
    difficulty = ExerciseDifficulty.LEVEL_14
    grammar_categories = ["word_order", "negation", "questions", "clauses", "verbs"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Mixed Challenge exercise."""
        self.correct_sentence: List[Word] = []
        self.shuffled_words: List[Word] = []
        self.challenge_type: str = ""
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.correct_sentence = []
        self.shuffled_words = []
        self.challenge_type = ""
    
    def generate(self) -> None:
        """Generate a new Mixed Challenge exercise."""
        # Choose a challenge type randomly
        challenge_types = [
            "complex_sentence",
            "question_with_negation",
            "subordinate_with_negation",
            "multi_clause",
        ]
        
        self.challenge_type = random.choice(challenge_types)
        
        # Generate sentence based on challenge type
        if self.challenge_type == "complex_sentence":
            self._generate_complex_sentence()
        elif self.challenge_type == "question_with_negation":
            self._generate_question_with_negation()
        elif self.challenge_type == "subordinate_with_negation":
            self._generate_subordinate_with_negation()
        else:
            self._generate_multi_clause()
        
        # Shuffle the words
        self.shuffled_words = self.correct_sentence.copy()
        random.shuffle(self.shuffled_words)
        
        # Create step
        self.steps = [
            ExerciseStep(
                step_number=1,
                question=self._get_question_text(),
                options=[word.text for word in self.shuffled_words],
                correct_answer=[word.text for word in self.correct_sentence],
                explanation=self._generate_explanation(),
                grammar_rule_id=self._get_relevant_rule_id()
            )
        ]
        
        self.current_step_index = 0
    
    def _generate_complex_sentence(self) -> None:
        """Generate a complex sentence with multiple elements."""
        # Generate a sentence with subject, verb, object, adverb, time, place
        level = 14
        self.correct_sentence = self.grammar_engine.generate_sentence(
            level=level,
            language_code=self.language
        )
    
    def _generate_question_with_negation(self) -> None:
        """Generate a question with negation."""
        # Generate a simple sentence
        sentence = self.grammar_engine.generate_sentence(
            level=8,
            language_code=self.language
        )
        
        if sentence:
            # Convert to question (swap subject and verb)
            subject_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.SUBJECT), 0)
            verb_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.VERB and w.is_finite), 1)
            
            if subject_idx < len(sentence) and verb_idx < len(sentence):
                sentence[subject_idx], sentence[verb_idx] = sentence[verb_idx], sentence[subject_idx]
            
            # Add negation after the verb
            ikke = self.grammar_engine.get_word("ikke", self.language)
            if ikke and verb_idx < len(sentence):
                sentence.insert(verb_idx + 1, ikke)
            
            self.correct_sentence = sentence
    
    def _generate_subordinate_with_negation(self) -> None:
        """Generate a subordinate clause with negation."""
        # Generate a simple clause
        sentence = self.grammar_engine.generate_sentence(
            level=12,
            language_code=self.language
        )
        
        if sentence:
            # Convert to subordinate order
            subject_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.SUBJECT), 0)
            verb_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.VERB and w.is_finite), 1)
            
            if subject_idx < len(sentence) and verb_idx < len(sentence):
                # Remove verb and add at end
                verb = sentence.pop(verb_idx)
                sentence.append(verb)
            
            # Add negation before the verb (which is now at the end)
            ikke = self.grammar_engine.get_word("ikke", self.language)
            if ikke:
                sentence.insert(-1, ikke)
            
            # Add conjunction
            conjunction = self.grammar_engine.get_word("at", self.language)
            if conjunction:
                sentence.insert(0, conjunction)
            
            self.correct_sentence = sentence
    
    def _generate_multi_clause(self) -> None:
        """Generate a sentence with multiple clauses."""
        # Generate main clause
        main_clause = self.grammar_engine.generate_sentence(
            level=8,
            language_code=self.language
        )
        
        # Generate subordinate clause
        sub_clause = self.grammar_engine.generate_sentence(
            level=12,
            language_code=self.language
        )
        
        if main_clause and sub_clause:
            # Add conjunction to subordinate
            conjunction = self.grammar_engine.get_word("fordi", self.language)
            if conjunction:
                sub_clause.insert(0, conjunction)
            
            # Combine
            self.correct_sentence = main_clause + [Word(text=",", word_type=WordType.OTHER)] + sub_clause
    
    def _get_question_text(self) -> str:
        """Get the question text based on challenge type."""
        if self.challenge_type == "complex_sentence":
            return "Arrange the words to form a grammatically correct Danish sentence."
        elif self.challenge_type == "question_with_negation":
            return "Arrange the words to form a negative yes/no question."
        elif self.challenge_type == "subordinate_with_negation":
            return "Arrange the words to form a subordinate clause with negation."
        else:
            return "Arrange the words to form a sentence with multiple clauses."
    
    def _generate_explanation(self) -> str:
        """Generate explanation based on challenge type."""
        if not self.correct_sentence:
            return ""
        
        sentence_text = ' '.join(word.text for word in self.correct_sentence)
        
        if self.challenge_type == "complex_sentence":
            return f"This complex sentence follows Danish word order rules. Correct: '{sentence_text}'."
        elif self.challenge_type == "question_with_negation":
            return f"This negative question uses subject-verb inversion and places 'ikke' after the verb. Correct: '{sentence_text}'."
        elif self.challenge_type == "subordinate_with_negation":
            return f"This subordinate clause has the verb at the end with 'ikke' before it. Correct: '{sentence_text}'."
        else:
            return f"This multi-clause sentence combines main and subordinate clauses. Correct: '{sentence_text}'."
    
    def _get_relevant_rule_id(self) -> str:
        """Get the relevant grammar rule ID."""
        if self.challenge_type == "complex_sentence":
            return "da_v2_rule"
        elif self.challenge_type == "question_with_negation":
            return "da_question_inversion"
        elif self.challenge_type == "subordinate_with_negation":
            return "da_subordinate_order"
        else:
            return "da_v2_rule"
    
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
            return True, "Correct! The sentence is grammatically valid.", []
        
        # Validate against grammar rules
        user_words = []
        for word_text in answer:
            word = self.grammar_engine.get_word(word_text, self.language)
            if word:
                user_words.append(word)
            else:
                user_words.append(Word(text=word_text, word_type=WordType.OTHER))
        
        is_valid, errors = self.grammar_engine.validate_sentence(user_words, self.language)
        
        if not is_valid:
            mistake_categories = []
            for error in errors:
                if "V2" in error or "second position" in error:
                    mistake_categories.append("word_order")
                elif "negation" in error or "ikke" in error:
                    mistake_categories.append("negation")
                elif "subject" in error and "verb" in error:
                    mistake_categories.append("word_order")
                else:
                    mistake_categories.append("grammar")
            
            return False, errors[0] if errors else "The sentence is not correct.", mistake_categories
        
        return False, "The word order is not correct.", ["word_order"]
    
    def get_shuffled_words(self) -> List[str]:
        """Get the shuffled words."""
        return [word.text for word in self.shuffled_words]
    
    def get_correct_sentence(self) -> List[str]:
        """Get the correct sentence."""
        return [word.text for word in self.correct_sentence]
    
    def get_challenge_type(self) -> str:
        """Get the challenge type."""
        return self.challenge_type
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        correct_words = [word.text for word in self.correct_sentence]
        
        self.hints = [
            Hint(
                level=1,
                content=self._get_hint_text(),
                hint_type="text"
            ),
            Hint(
                level=2,
                content=current_step.explanation,
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
    
    def _get_hint_text(self) -> str:
        """Get hint text based on challenge type."""
        if self.challenge_type == "complex_sentence":
            return "Remember: Danish follows V2 rule in main clauses."
        elif self.challenge_type == "question_with_negation":
            return "Questions use inversion. 'ikke' comes after the verb."
        elif self.challenge_type == "subordinate_with_negation":
            return "In subordinate clauses, the verb comes at the end. 'ikke' comes before the verb."
        else:
            return "Combine the clauses following Danish word order rules."
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'correct_sentence': [word.text for word in self.correct_sentence],
            'shuffled_words': [word.text for word in self.shuffled_words],
            'challenge_type': self.challenge_type,
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
