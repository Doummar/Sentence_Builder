"""
Subordinate Clause Trainer Exercise for Grammar Pro.

Mode 9: Practice only subordinate clause word order.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class SubordinateClauseExercise(BaseExercise):
    """
    Subordinate Clause Trainer Exercise.
    
    Practice the word order in Danish subordinate clauses.
    """
    
    exercise_type = ExerciseType.SUBORDINATE_CLAUSE
    name = "Subordinate Clause Trainer"
    description = "Practice subordinate clause word order: Subject-Object-Verb."
    difficulty = ExerciseDifficulty.LEVEL_12
    grammar_categories = ["clauses", "word_order"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Subordinate Clause exercise."""
        self.correct_clause: List[Word] = []
        self.shuffled_words: List[Word] = []
        self.conjunction: str = ""
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.correct_clause = []
        self.shuffled_words = []
        self.conjunction = ""
    
    def generate(self) -> None:
        """Generate a new Subordinate Clause exercise."""
        # Generate a subordinate clause
        # For now, we'll generate a simple clause and convert it to subordinate order
        level = self.difficulty.value if isinstance(self.difficulty, ExerciseDifficulty) else 12
        
        # Generate a simple clause
        sentence = self.grammar_engine.generate_sentence(
            level=min(level, 8),  # Use simpler sentences
            language_code=self.language
        )
        
        if sentence:
            # Convert to subordinate clause order: move verb to end
            # Find subject and finite verb
            subject_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.SUBJECT), 0)
            verb_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.VERB and w.is_finite), 1)
            
            if subject_idx < len(sentence) and verb_idx < len(sentence):
                # Create subordinate order: subject, object, verb
                self.correct_clause = []
                
                # Add all words except the verb
                for i, word in enumerate(sentence):
                    if i != verb_idx:
                        self.correct_clause.append(word)
                
                # Add the verb at the end
                if verb_idx < len(sentence):
                    self.correct_clause.append(sentence[verb_idx])
            else:
                self.correct_clause = sentence
        
        # Add a subordinating conjunction
        conjunctions = ["at", "fordi", "når", "hvis"]
        for conj in conjunctions:
            conj_word = self.grammar_engine.get_word(conj, self.language)
            if conj_word:
                self.conjunction = conj
                self.correct_clause.insert(0, conj_word)
                break
        
        # Shuffle the words (excluding the conjunction for now)
        self.shuffled_words = self.correct_clause.copy()
        # Don't shuffle the first word (conjunction)
        if self.shuffled_words:
            fixed_first = self.shuffled_words[0]
            remaining = self.shuffled_words[1:]
            random.shuffle(remaining)
            self.shuffled_words = [fixed_first] + remaining
        
        # Create step
        self.steps = [
            ExerciseStep(
                step_number=1,
                question=f"Arrange the words to form a correct subordinate clause starting with '{self.conjunction}'.",
                options=[word.text for word in self.shuffled_words],
                correct_answer=[word.text for word in self.correct_clause],
                explanation=self._generate_explanation(),
                grammar_rule_id="da_subordinate_order"
            )
        ]
        
        self.current_step_index = 0
    
    def _generate_explanation(self) -> str:
        """Generate explanation for subordinate clause order."""
        if not self.correct_clause:
            return "In Danish subordinate clauses, the word order is Subject-Object-Verb."
        
        sentence_text = ' '.join(word.text for word in self.correct_clause)
        
        # Find the verb
        verb_word = next((w for w in self.correct_clause if w.word_type == WordType.VERB and w.is_finite), None)
        if verb_word:
            return (f"In Danish subordinate clauses, the finite verb '{verb_word.text}' comes at the end. "
                    f"The correct order is: '{sentence_text}'.")
        
        return f"The correct subordinate clause is: '{sentence_text}'."
    
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
        correct_texts = [word.text for word in self.correct_clause]
        if answer == correct_texts:
            return True, "Correct! The subordinate clause has the right word order.", []
        
        # Check if verb is at the end
        user_words = []
        for word_text in answer:
            word = self.grammar_engine.get_word(word_text, self.language)
            if word:
                user_words.append(word)
            else:
                user_words.append(Word(text=word_text, word_type=WordType.OTHER))
        
        verb_indices = [i for i, w in enumerate(user_words) if w.word_type == WordType.VERB and w.is_finite]
        
        if verb_indices and verb_indices[-1] == len(user_words) - 1:
            # Verb is at the end, but other words are wrong
            return False, "The verb is in the correct position (at the end), but other words are not in the right order.", ["word_order"]
        elif verb_indices:
            return False, f"In subordinate clauses, the finite verb should be at the end, but it's at position {verb_indices[-1] + 1}.", ["subordinate_order"]
        else:
            return False, "There should be a finite verb in the clause.", ["verbs"]
    
    def get_shuffled_words(self) -> List[str]:
        """Get the shuffled words."""
        return [word.text for word in self.shuffled_words]
    
    def get_correct_clause(self) -> List[str]:
        """Get the correct clause."""
        return [word.text for word in self.correct_clause]
    
    def get_conjunction(self) -> str:
        """Get the subordinating conjunction."""
        return self.conjunction
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        correct_words = [word.text for word in self.correct_clause]
        
        self.hints = [
            Hint(
                level=1,
                content="In Danish subordinate clauses, the finite verb comes at the END.",
                hint_type="text"
            ),
            Hint(
                level=2,
                content="The word order is: Subject -> Object -> Verb",
                hint_type="text"
            ),
            Hint(
                level=3,
                content=f"The clause starts with '{self.conjunction}'.",
                hint_type="text"
            ),
            Hint(
                level=4,
                content=f"The first word is: '{correct_words[0]}'",
                hint_type="reveal_word"
            ),
            Hint(
                level=5,
                content=f"The correct clause is: '{' '.join(correct_words)}'",
                hint_type="reveal_answer"
            ),
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'correct_clause': [word.text for word in self.correct_clause],
            'shuffled_words': [word.text for word in self.shuffled_words],
            'conjunction': self.conjunction,
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
