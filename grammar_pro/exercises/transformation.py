"""
Transformation Exercise for Grammar Pro.

Mode 6: Convert a sentence through various transformations.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class TransformationExercise(BaseExercise):
    """
    Transformation Exercise.
    
    Convert a sentence through various transformations:
    Statement -> Question -> Negative -> Past tense -> Future tense -> Subordinate clause -> Passive -> Relative clause
    """
    
    exercise_type = ExerciseType.TRANSFORMATION
    name = "Transformation Trainer"
    description = "Transform the sentence through various forms."
    difficulty = ExerciseDifficulty.LEVEL_8
    grammar_categories = ["verbs", "questions", "negation", "clauses"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Transformation exercise."""
        self.base_sentence: List[Word] = []
        self.current_sentence: List[Word] = []
        self.transformations: List[Dict[str, Any]] = []
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.base_sentence = []
        self.current_sentence = []
        self.transformations = []
    
    def generate(self) -> None:
        """Generate a new Transformation exercise."""
        # Generate a base sentence (statement)
        self.base_sentence = self.grammar_engine.generate_sentence(
            level=5,
            language_code=self.language
        )
        self.current_sentence = self.base_sentence.copy()
        
        # Define transformation steps
        self.transformations = [
            {
                'name': 'Question',
                'description': 'Convert the statement to a yes/no question',
                'rule_id': 'da_question_inversion',
                'explanation': 'In Danish, yes/no questions use subject-verb inversion.'
            },
            {
                'name': 'Negative',
                'description': 'Convert the sentence to negative form',
                'rule_id': 'da_negation_ikke',
                'explanation': 'Add "ikke" after the finite verb to make it negative.'
            },
            {
                'name': 'Past Tense',
                'description': 'Convert the sentence to past tense',
                'rule_id': '',
                'explanation': 'Change the verb to its past tense form.'
            },
        ]
        
        # Create steps
        self.steps = []
        for i, trans in enumerate(self.transformations):
            self.steps.append(ExerciseStep(
                step_number=i + 1,
                question=f"Transform to {trans['name']}: {trans['description']}",
                options=[],
                correct_answer=self._get_transformed_sentence(i),
                explanation=trans['explanation'],
                grammar_rule_id=trans['rule_id']
            ))
        
        self.current_step_index = 0
    
    def _get_transformed_sentence(self, transformation_index: int) -> List[str]:
        """Get the sentence after applying the transformation."""
        # This is a simplified version - in a full implementation, we'd actually transform the sentence
        transformation = self.transformations[transformation_index]
        
        if transformation['name'] == 'Question':
            # Swap subject and verb for question
            sentence = self.base_sentence.copy()
            subject_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.SUBJECT), 0)
            verb_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.VERB and w.is_finite), 1)
            if subject_idx < verb_idx:
                sentence[subject_idx], sentence[verb_idx] = sentence[verb_idx], sentence[subject_idx]
            return [word.text for word in sentence]
        
        elif transformation['name'] == 'Negative':
            # Add "ikke" after the verb
            sentence = self.base_sentence.copy()
            verb_idx = next((i for i, w in enumerate(sentence) if w.word_type == WordType.VERB and w.is_finite), 1)
            ikke = self.grammar_engine.get_word("ikke", self.language)
            if ikke:
                sentence.insert(verb_idx + 1, ikke)
            return [word.text for word in sentence]
        
        elif transformation['name'] == 'Past Tense':
            # Change verb to past tense
            sentence = self.base_sentence.copy()
            for i, word in enumerate(sentence):
                if word.word_type == WordType.VERB and word.is_finite and word.past_tense:
                    sentence[i] = Word(
                        text=word.past_tense,
                        word_type=word.word_type,
                        base_form=word.base_form,
                        is_finite=True,
                        past_tense=word.past_tense
                    )
                    break
            return [word.text for word in sentence]
        
        return [word.text for word in self.base_sentence]
    
    def validate_answer(self, answer: Any) -> Tuple[bool, str, List[str]]:
        """
        Validate the user's answer.
        
        Args:
            answer: The user's answer (list of word texts)
            
        Returns:
            Tuple of (is_correct, explanation, list_of_mistake_categories)
        """
        current_step = self.current_step
        if not current_step:
            return False, "No current step.", ["internal_error"]
        
        if isinstance(answer, list):
            correct = current_step.correct_answer
            if answer == correct:
                self.current_sentence = [self.grammar_engine.get_word(w, self.language) or Word(text=w, word_type=WordType.OTHER) for w in answer]
                return True, current_step.explanation, []
        
        # Determine mistake category
        mistake_categories = []
        if current_step.grammar_rule_id:
            if "question" in current_step.grammar_rule_id:
                mistake_categories.append("questions")
            elif "negation" in current_step.grammar_rule_id:
                mistake_categories.append("negation")
            else:
                mistake_categories.append("verbs")
        
        return False, current_step.explanation, mistake_categories
    
    def get_base_sentence(self) -> List[str]:
        """Get the base sentence."""
        return [word.text for word in self.base_sentence]
    
    def get_current_sentence(self) -> List[str]:
        """Get the current sentence."""
        return [word.text for word in self.current_sentence]
    
    def get_transformation_name(self) -> str:
        """Get the name of the current transformation."""
        if self.current_step_index < len(self.transformations):
            return self.transformations[self.current_step_index]['name']
        return ""
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        transformation = self.transformations[self.current_step_index] if self.current_step_index < len(self.transformations) else None
        
        if transformation:
            self.hints = [
                Hint(
                    level=1,
                    content=transformation['description'],
                    hint_type="text"
                ),
                Hint(
                    level=2,
                    content=transformation['explanation'],
                    hint_type="text"
                ),
                Hint(
                    level=5,
                    content=f"The correct answer is: {' '.join(current_step.correct_answer)}",
                    hint_type="reveal_answer"
                ),
            ]
        else:
            self.hints = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'base_sentence': [word.text for word in self.base_sentence],
            'current_sentence': [word.text for word in self.current_sentence],
            'transformations': [t['name'] for t in self.transformations],
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
