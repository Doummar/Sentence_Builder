"""
Grammar Decision Exercise for Grammar Pro.

Mode 2: Answer grammar questions one step at a time.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class GrammarDecisionExercise(BaseExercise):
    """
    Grammar Decision Exercise.
    
    The learner answers grammar questions one step at a time,
    guiding them through the sentence construction process.
    """
    
    exercise_type = ExerciseType.GRAMMAR_DECISION
    name = "Grammar Decision Trainer"
    description = "Answer grammar questions one step at a time to build a sentence."
    difficulty = ExerciseDifficulty.LEVEL_3
    grammar_categories = ["word_order", "grammar_rules"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Grammar Decision exercise."""
        self.correct_sentence: List[Word] = []
        self.built_sentence: List[Word] = []
        self.remaining_words: List[Word] = []
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.correct_sentence = []
        self.built_sentence = []
        self.remaining_words = []
    
    def generate(self) -> None:
        """Generate a new Grammar Decision exercise."""
        # Generate a sentence
        level = self.difficulty.value if isinstance(self.difficulty, ExerciseDifficulty) else 1
        self.correct_sentence = self.grammar_engine.generate_sentence(
            level=level,
            language_code=self.language
        )
        
        # Shuffle the words for the exercise
        self.remaining_words = self.correct_sentence.copy()
        random.shuffle(self.remaining_words)
        
        # Create steps for each decision point
        self.steps = self._create_steps()
        self.current_step_index = 0
    
    def _create_steps(self) -> List[ExerciseStep]:
        """Create the decision steps for building the sentence."""
        steps = []
        grammar = self.grammar_engine.get_grammar(self.language)
        
        if not grammar or not self.correct_sentence:
            return steps
        
        # Step 1: Is this a main clause or subordinate clause?
        steps.append(ExerciseStep(
            step_number=1,
            question="Is this a main clause or a subordinate clause?",
            options=["Main clause", "Subordinate clause"],
            correct_answer="Main clause",
            explanation="This is a main clause (independent clause) that can stand alone as a sentence.",
            grammar_rule_id="da_v2_rule"
        ))
        
        # Step 2: What comes first?
        first_word = self.correct_sentence[0]
        steps.append(ExerciseStep(
            step_number=2,
            question=f"What word should come first?",
            options=[word.text for word in self.remaining_words[:4]],  # Show first 4 options
            correct_answer=first_word.text,
            explanation=self._get_first_word_explanation(first_word),
            grammar_rule_id="da_v2_rule"
        ))
        
        # Step 3: Place the finite verb
        verb_word = next((w for w in self.correct_sentence if w.word_type == WordType.VERB and w.is_finite), None)
        if verb_word:
            steps.append(ExerciseStep(
                step_number=3,
                question="Where should the finite verb go?",
                options=["First position", "Second position", "Third position", "Last position"],
                correct_answer="Second position",
                explanation=f"In Danish main clauses, the finite verb '{verb_word.text}' must be in the second position (V2 rule).",
                grammar_rule_id="da_v2_rule"
            ))
        
        # Step 4: Place the subject
        subject_word = next((w for w in self.correct_sentence if w.word_type == WordType.SUBJECT), None)
        if subject_word:
            steps.append(ExerciseStep(
                step_number=4,
                question=f"Where should the subject '{subject_word.text}' go?",
                options=["Before the verb", "After the verb", "At the end"],
                correct_answer="Before the verb",
                explanation=f"In Danish main clauses, the subject '{subject_word.text}' comes before the finite verb.",
                grammar_rule_id="da_subject_verb"
            ))
        
        # Step 5: Continue with remaining words
        # For simplicity, we'll just have a few key decision points
        # In a full implementation, we'd guide through each word placement
        
        return steps
    
    def _get_first_word_explanation(self, first_word: Word) -> str:
        """Generate explanation for the first word."""
        if first_word.word_type == WordType.SUBJECT:
            return f"' {first_word.text}' is the subject. In Danish main clauses, the subject often comes first."
        elif first_word.word_type == WordType.ADVERB:
            return f"' {first_word.text}' is an adverb. When an adverb comes first, it triggers V2 inversion."
        elif first_word.word_type == WordType.TIME_EXPRESSION:
            return f"' {first_word.text}' is a time expression. Time expressions can come first, triggering V2 inversion."
        else:
            return f"The sentence starts with '{first_word.text}'."
    
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
        
        # Check if answer matches
        if answer == current_step.correct_answer:
            # Move the correct word to the built sentence if applicable
            if isinstance(answer, str) and answer in [w.text for w in self.remaining_words]:
                for i, word in enumerate(self.remaining_words):
                    if word.text == answer:
                        self.built_sentence.append(self.remaining_words.pop(i))
                        break
            
            return True, current_step.explanation, []
        
        # Determine mistake category
        mistake_categories = []
        if "clause" in current_step.question.lower():
            mistake_categories.append("clauses")
        elif "verb" in current_step.question.lower():
            mistake_categories.append("verbs")
        elif "subject" in current_step.question.lower():
            mistake_categories.append("word_order")
        else:
            mistake_categories.append("grammar")
        
        return False, current_step.explanation, mistake_categories
    
    def get_built_sentence(self) -> List[str]:
        """Get the currently built sentence."""
        return [word.text for word in self.built_sentence]
    
    def get_remaining_words(self) -> List[str]:
        """Get the remaining words to place."""
        return [word.text for word in self.remaining_words]
    
    def get_correct_sentence_text(self) -> str:
        """Get the correct sentence as a single string."""
        return ' '.join(word.text for word in self.correct_sentence)
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        self.hints = [
            Hint(
                level=1,
                content=f"Think about: {current_step.question}",
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'correct_sentence': [word.text for word in self.correct_sentence],
            'built_sentence': [word.text for word in self.built_sentence],
            'remaining_words': [word.text for word in self.remaining_words],
        })
        return result


# Import Hint for type checking
from .base_exercise import Hint
