"""
Sentence Builder Exercise for Grammar Pro.

Mode 1: Drag words into the correct order.
"""

import random
from typing import Any, Dict, List, Optional, Tuple

from .base_exercise import BaseExercise, ExerciseDifficulty, ExerciseStep, ExerciseType
from ..grammar.base_grammar import Word, WordType


class SentenceBuilderExercise(BaseExercise):
    """
    Sentence Builder Exercise.
    
    The learner drags words into the correct order to form a valid sentence.
    """
    
    exercise_type = ExerciseType.SENTENCE_BUILDER
    name = "Sentence Builder"
    description = "Drag words into the correct order to form a valid sentence."
    difficulty = ExerciseDifficulty.LEVEL_2
    grammar_categories = ["word_order"]
    
    def __init__(self, grammar_engine, settings, exercise_id=None, language=None, difficulty=None):
        """Initialize the Sentence Builder exercise."""
        self.correct_sentence: List[Word] = []
        self.shuffled_words: List[Word] = []
        self.user_sentence: List[Word] = []
        self.template_id: Optional[str] = None
        
        super().__init__(grammar_engine, settings, exercise_id, language, difficulty)
    
    def _initialize(self) -> None:
        """Initialize exercise-specific data."""
        self.correct_sentence = []
        self.shuffled_words = []
        self.user_sentence = []
        self.template_id = None
    
    def generate(self) -> None:
        """Generate a new Sentence Builder exercise."""
        # Get a random template based on difficulty
        level = self.difficulty.value if isinstance(self.difficulty, ExerciseDifficulty) else 1
        
        templates = self.grammar_engine.get_templates_by_level(level, self.language)
        if not templates:
            # Fallback to any template
            templates = list(self.grammar_engine.get_templates(self.language).values())
        
        if templates:
            template = random.choice(templates)
            self.template_id = template.template_id
            self.correct_sentence = self.grammar_engine.generate_sentence(
                template_id=template.template_id,
                language_code=self.language
            )
        else:
            # Fallback: generate a simple sentence
            self.correct_sentence = self.grammar_engine.generate_sentence(
                language_code=self.language
            )
        
        # Create shuffled words (remove duplicates for shuffling)
        self.shuffled_words = self.correct_sentence.copy()
        random.shuffle(self.shuffled_words)
        
        # Create a single step for this exercise
        self.steps = [
            ExerciseStep(
                step_number=1,
                question="Arrange the words to form a correct sentence.",
                options=[word.text for word in self.shuffled_words],
                correct_answer=[word.text for word in self.correct_sentence],
                explanation=self._generate_explanation(),
                grammar_rule_id=self._get_relevant_rule_id()
            )
        ]
        
        self.current_step_index = 0
        self.user_sentence = []
    
    def _generate_explanation(self) -> str:
        """Generate an explanation for the correct sentence."""
        if not self.correct_sentence:
            return ""
        
        # Get the grammar rules that apply
        grammar = self.grammar_engine.get_grammar(self.language)
        if not grammar:
            return ""
        
        # Generate explanation based on the sentence structure
        sentence_text = ' '.join(word.text for word in self.correct_sentence)
        
        # Check for specific patterns
        if len(self.correct_sentence) >= 2:
            subject = next((w for w in self.correct_sentence if w.word_type == WordType.SUBJECT), None)
            verb = next((w for w in self.correct_sentence if w.word_type == WordType.VERB and w.is_finite), None)
            
            if subject and verb:
                return (f"In Danish, the subject '{subject.text}' comes before the verb '{verb.text}'. "
                        f"This forms a valid statement: '{sentence_text}'.")
        
        return f"The correct sentence is: '{sentence_text}'."
    
    def _get_relevant_rule_id(self) -> str:
        """Get the most relevant grammar rule ID for this sentence."""
        # Check for V2 rule
        if len(self.correct_sentence) >= 2:
            verb_indices = [i for i, w in enumerate(self.correct_sentence) 
                          if w.word_type == WordType.VERB and w.is_finite]
            if verb_indices and verb_indices[0] == 1:  # Verb in second position
                return "da_v2_rule"
        
        # Check for SVO
        subject_indices = [i for i, w in enumerate(self.correct_sentence) if w.word_type == WordType.SUBJECT]
        verb_indices = [i for i, w in enumerate(self.correct_sentence) if w.word_type == WordType.VERB and w.is_finite]
        object_indices = [i for i, w in enumerate(self.correct_sentence) if w.word_type == WordType.OBJECT]
        
        if subject_indices and verb_indices and object_indices:
            if subject_indices[0] < verb_indices[0] < object_indices[0]:
                return "da_svo_order"
        
        return "da_subject_verb"
    
    def validate_answer(self, answer: Any) -> Tuple[bool, str, List[str]]:
        """
        Validate the user's answer.
        
        Args:
            answer: List of word texts in the user's order
            
        Returns:
            Tuple of (is_correct, explanation, list_of_mistake_categories)
        """
        if not isinstance(answer, list):
            return False, "Please provide a list of words.", ["invalid_answer"]
        
        # Convert answer to Word objects for validation
        user_words = []
        for word_text in answer:
            word = self.grammar_engine.get_word(word_text, self.language)
            if word:
                user_words.append(word)
            else:
                # Create a temporary word
                user_words.append(Word(text=word_text, word_type=WordType.OTHER))
        
        # Check if the order matches
        correct_texts = [word.text for word in self.correct_sentence]
        user_texts = [word.text for word in user_words]
        
        if user_texts == correct_texts:
            return True, "Correct! The sentence is grammatically valid.", []
        
        # Validate against grammar rules
        is_valid, errors = self.grammar_engine.validate_sentence(user_words, self.language)
        
        if not is_valid:
            mistake_categories = []
            for error in errors:
                # Extract category from error message
                if "V2" in error or "second position" in error:
                    mistake_categories.append("word_order")
                elif "negation" in error or "ikke" in error:
                    mistake_categories.append("negation")
                elif "subject" in error and "verb" in error:
                    mistake_categories.append("word_order")
                else:
                    mistake_categories.append("grammar")
            
            return False, errors[0] if errors else "The sentence is not correct.", mistake_categories
        
        # If grammar is valid but order is different, check if it's an acceptable alternative
        # For now, we'll consider it incorrect if it doesn't match exactly
        return False, "The word order is not correct.", ["word_order"]
    
    def get_shuffled_words(self) -> List[str]:
        """Get the shuffled words for the user to arrange."""
        return [word.text for word in self.shuffled_words]
    
    def get_correct_sentence(self) -> List[str]:
        """Get the correct sentence as a list of word texts."""
        return [word.text for word in self.correct_sentence]
    
    def get_correct_sentence_text(self) -> str:
        """Get the correct sentence as a single string."""
        return ' '.join(word.text for word in self.correct_sentence)
    
    def set_user_sentence(self, words: List[str]) -> None:
        """Set the user's current sentence."""
        self.user_sentence = []
        for word_text in words:
            word = self.grammar_engine.get_word(word_text, self.language)
            if word:
                self.user_sentence.append(word)
            else:
                self.user_sentence.append(Word(text=word_text, word_type=WordType.OTHER))
    
    def get_user_sentence(self) -> List[str]:
        """Get the user's current sentence as a list of word texts."""
        return [word.text for word in self.user_sentence]
    
    def _generate_hints(self) -> None:
        """Generate hints for this exercise."""
        current_step = self.current_step
        if not current_step:
            return
        
        correct_words = [word.text for word in self.correct_sentence]
        
        self.hints = [
            # Hint 1: Identify the subject and verb
            {
                'level': 1,
                'content': self._get_subject_verb_hint(),
                'hint_type': 'text'
            },
            # Hint 2: Explain the rule
            {
                'level': 2,
                'content': current_step.explanation,
                'hint_type': 'text'
            },
            # Hint 3: Show the template
            {
                'level': 3,
                'content': self._get_template_hint(),
                'hint_type': 'template'
            },
            # Hint 4: Reveal first word
            {
                'level': 4,
                'content': f"The first word is: '{correct_words[0]}'",
                'hint_type': 'reveal_word'
            },
            # Hint 5: Reveal the answer
            {
                'level': 5,
                'content': f"The correct sentence is: '{' '.join(correct_words)}'",
                'hint_type': 'reveal_answer'
            },
        ]
    
    def _get_subject_verb_hint(self) -> str:
        """Generate a hint about subject and verb."""
        subject = next((w for w in self.correct_sentence if w.word_type == WordType.SUBJECT), None)
        verb = next((w for w in self.correct_sentence if w.word_type == WordType.VERB and w.is_finite), None)
        
        if subject and verb:
            return (f"Find the subject ('{subject.text}') and the finite verb ('{verb.text}'). "
                    f"In Danish main clauses, the subject comes before the verb.")
        return "Identify the subject and the finite verb in the sentence."
    
    def _get_template_hint(self) -> str:
        """Generate a hint showing the template."""
        if self.template_id:
            template = self.grammar_engine.get_template(self.template_id, self.language)
            if template:
                structure = ' -> '.join(wt.value for wt in template.structure)
                return f"Template: {structure}"
        return "Arrange the words following Danish word order rules."
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = super().to_dict()
        result.update({
            'correct_sentence': [word.text for word in self.correct_sentence],
            'shuffled_words': [word.text for word in self.shuffled_words],
            'user_sentence': [word.text for word in self.user_sentence],
            'template_id': self.template_id,
        })
        return result
