"""
Clause Trainer Exercise for Grammar Pro.

Mode 5: The learner first builds the main clause, then the subordinate clause, then combines them.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class ClauseTrainerExercise(BaseExercise):
    """
    Clause Trainer Exercise.
    
    The learner builds the main clause, then the subordinate clause, then combines them.
    """
    
    exercise_type = ExerciseType.CLAUSE_TRAINER
    name = "Clause Trainer"
    description = "Build the main clause, then the subordinate clause, then combine them."
    difficulty = ExerciseDifficulty.LEVEL_12
    grammar_categories = ["clauses", "word_order"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Clause Trainer exercise."""
        self.main_clause: List[Word] = []
        self.subordinate_clause: List[Word] = []
        self.combined_sentence: List[Word] = []
        self.current_phase: str = "main"  # 'main', 'subordinate', 'combine'
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.main_clause = []
        self.subordinate_clause = []
        self.combined_sentence = []
        self.current_phase = "main"
    
    def generate(self) -> None:
        """Generate a new Clause Trainer exercise."""
        # Generate a main clause
        self.main_clause = self.grammar_engine.generate_sentence(
            level=8,  # Main clauses are simpler
            language_code=self.language
        )
        
        # Generate a subordinate clause
        # For now, we'll generate a simple clause and add a subordinating conjunction
        self.subordinate_clause = self.grammar_engine.generate_sentence(
            level=12,
            language_code=self.language
        )
        
        # Add a subordinating conjunction at the beginning
        conjunction = self.grammar_engine.get_word("at", self.language)
        if conjunction:
            self.subordinate_clause.insert(0, conjunction)
        
        # Create steps for each phase
        self.steps = [
            # Phase 1: Build main clause
            ExerciseStep(
                step_number=1,
                question="Build the main clause. Arrange these words in the correct order.",
                options=[word.text for word in self.main_clause],
                correct_answer=[word.text for word in self.main_clause],
                explanation="In Danish main clauses, follow the V2 rule: the finite verb is in the second position.",
                grammar_rule_id="da_v2_rule"
            ),
            # Phase 2: Build subordinate clause
            ExerciseStep(
                step_number=2,
                question="Build the subordinate clause. Arrange these words in the correct order.",
                options=[word.text for word in self.subordinate_clause],
                correct_answer=[word.text for word in self.subordinate_clause],
                explanation="In Danish subordinate clauses, the finite verb comes at the end (after subject and object).",
                grammar_rule_id="da_subordinate_order"
            ),
            # Phase 3: Combine them
            ExerciseStep(
                step_number=3,
                question="Combine the main and subordinate clauses. Where should the subordinate clause go?",
                options=["Before the main clause", "After the main clause"],
                correct_answer="After the main clause",
                explanation="Subordinate clauses typically come after the main clause in Danish.",
                grammar_rule_id="da_subordinate_order"
            )
        ]
        
        self.current_step_index = 0
    
    def validate_answer(self, answer: Any) -> Tuple[bool, str, List[str]]:
        """
        Validate the user's answer.
        
        Args:
            answer: The user's answer
            
        Returns:
            Tuple of (is_correct, explanation, list_of_mistake_categories)
        """
        current_step = self.current_step
        if not current_step:
            return False, "No current step.", ["internal_error"]
        
        # Step 1: Main clause
        if current_step.step_number == 1:
            if isinstance(answer, list):
                correct_texts = [word.text for word in self.main_clause]
                if answer == correct_texts:
                    self.current_phase = "subordinate"
                    return True, current_step.explanation, []
            return False, "The main clause order is not correct.", ["word_order"]
        
        # Step 2: Subordinate clause
        if current_step.step_number == 2:
            if isinstance(answer, list):
                correct_texts = [word.text for word in self.subordinate_clause]
                if answer == correct_texts:
                    self.current_phase = "combine"
                    return True, current_step.explanation, []
            return False, "The subordinate clause order is not correct.", ["clauses"]
        
        # Step 3: Combine
        if current_step.step_number == 3:
            if answer == "After the main clause":
                # Build the combined sentence
                self.combined_sentence = self.main_clause + [self.grammar_engine.get_word(",", self.language) or Word(text=",", word_type=WordType.OTHER)] + self.subordinate_clause
                return True, current_step.explanation, []
            return False, "Subordinate clauses typically come after the main clause.", ["clauses"]
        
        return False, "Invalid answer.", ["internal_error"]
    
    def get_main_clause(self) -> List[str]:
        """Get the main clause words."""
        return [word.text for word in self.main_clause]
    
    def get_subordinate_clause(self) -> List[str]:
        """Get the subordinate clause words."""
        return [word.text for word in self.subordinate_clause]
    
    def get_combined_sentence(self) -> List[str]:
        """Get the combined sentence."""
        if self.combined_sentence:
            return [word.text for word in self.combined_sentence]
        return []
    
    def get_current_phase(self) -> str:
        """Get the current phase."""
        return self.current_phase
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        if current_step.step_number == 1:
            self.hints = [
                Hint(
                    level=1,
                    content="Remember the V2 rule: the finite verb must be in the second position.",
                    hint_type="text"
                ),
                Hint(
                    level=2,
                    content=current_step.explanation,
                    hint_type="text"
                ),
            ]
        elif current_step.step_number == 2:
            self.hints = [
                Hint(
                    level=1,
                    content="In subordinate clauses, the finite verb comes at the end.",
                    hint_type="text"
                ),
                Hint(
                    level=2,
                    content=current_step.explanation,
                    hint_type="text"
                ),
            ]
        else:
            self.hints = [
                Hint(
                    level=1,
                    content="Subordinate clauses typically follow the main clause.",
                    hint_type="text"
                ),
            ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'main_clause': [word.text for word in self.main_clause],
            'subordinate_clause': [word.text for word in self.subordinate_clause],
            'combined_sentence': [word.text for word in self.combined_sentence],
            'current_phase': self.current_phase,
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
