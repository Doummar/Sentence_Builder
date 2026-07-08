"""
Base Grammar class for Grammar Pro.

Defines the interface that all language-specific grammar classes must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..config.settings import Settings


class WordType(Enum):
    """Types of words in a sentence."""
    SUBJECT = "subject"
    VERB = "verb"
    OBJECT = "object"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    ARTICLE = "article"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    NOUN = "noun"
    PROPER_NOUN = "proper_noun"
    AUXILIARY = "auxiliary"
    MODAL = "modal"
    NEGATION = "negation"
    TIME_EXPRESSION = "time_expression"
    PLACE_EXPRESSION = "place_expression"
    RELATIVE_PRONOUN = "relative_pronoun"
    SUBORDINATING_CONJUNCTION = "subordinating_conjunction"
    OTHER = "other"


class ClauseType(Enum):
    """Types of clauses."""
    MAIN = "main"
    SUBORDINATE = "subordinate"
    RELATIVE = "relative"
    QUESTION = "question"
    IMPERATIVE = "imperative"


class SentenceType(Enum):
    """Types of sentences."""
    STATEMENT = "statement"
    QUESTION = "question"
    COMMAND = "command"
    EXCLAMATION = "exclamation"


class GrammarRule:
    """
    Represents a grammar rule.
    
    Contains the rule definition, validation logic, and explanation.
    """
    
    def __init__(
        self,
        rule_id: str,
        name: str,
        description: str,
        category: str,
        level: int,
        validation_func: Optional[callable] = None,
        explanation: str = "",
        examples: List[str] = None,
        counter_examples: List[str] = None
    ):
        """
        Initialize a grammar rule.
        
        Args:
            rule_id: Unique identifier for the rule
            name: Human-readable name
            description: Description of the rule
            category: Category (e.g., 'word_order', 'negation', 'questions')
            level: Difficulty level (1-14)
            validation_func: Function to validate if a sentence follows the rule
            explanation: Explanation of the rule
            examples: Example sentences that follow the rule
            counter_examples: Example sentences that violate the rule
        """
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.category = category
        self.level = level
        self.validation_func = validation_func
        self.explanation = explanation
        self.examples = examples or []
        self.counter_examples = counter_examples or []
    
    def validate(self, sentence: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Validate if a sentence follows this rule.
        
        Args:
            sentence: List of word dictionaries with type information
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.validation_func:
            return self.validation_func(sentence)
        return True, ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary for serialization."""
        return {
            'rule_id': self.rule_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'level': self.level,
            'explanation': self.explanation,
            'examples': self.examples,
            'counter_examples': self.counter_examples,
        }


@dataclass
class Word:
    """Represents a word with its grammatical properties."""
    text: str
    word_type: WordType
    base_form: str = ""
    plural_form: str = ""
    past_tense: str = ""
    present_participle: str = ""
    past_participle: str = ""
    gender: str = ""  # For languages with grammatical gender
    case: str = ""  # For languages with cases
    number: str = "singular"  # singular or plural
    person: int = 0  # 1, 2, 3 for pronouns
    is_finite: bool = False  # For verbs
    is_modal: bool = False
    is_auxiliary: bool = False
    is_negation: bool = False
    position: int = -1  # Position in sentence
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert word to dictionary."""
        return {
            'text': self.text,
            'type': self.word_type.value,
            'base_form': self.base_form,
            'plural_form': self.plural_form,
            'past_tense': self.past_tense,
            'present_participle': self.present_participle,
            'past_participle': self.past_participle,
            'gender': self.gender,
            'case': self.case,
            'number': self.number,
            'person': self.person,
            'is_finite': self.is_finite,
            'is_modal': self.is_modal,
            'is_auxiliary': self.is_auxiliary,
            'is_negation': self.is_negation,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Word':
        """Create Word from dictionary."""
        return cls(
            text=data.get('text', ''),
            word_type=WordType(data.get('type', 'other')),
            base_form=data.get('base_form', ''),
            plural_form=data.get('plural_form', ''),
            past_tense=data.get('past_tense', ''),
            present_participle=data.get('present_participle', ''),
            past_participle=data.get('past_participle', ''),
            gender=data.get('gender', ''),
            case=data.get('case', ''),
            number=data.get('number', 'singular'),
            person=data.get('person', 0),
            is_finite=data.get('is_finite', False),
            is_modal=data.get('is_modal', False),
            is_auxiliary=data.get('is_auxiliary', False),
            is_negation=data.get('is_negation', False),
        )


@dataclass
class SentenceTemplate:
    """
    Template for generating sentences.
    
    Defines the structure and constraints for sentence generation.
    """
    template_id: str
    name: str
    structure: List[WordType]  # Expected word types in order
    required_rules: List[str]  # Rule IDs that must be satisfied
    level: int
    category: str
    description: str = ""
    examples: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary."""
        return {
            'template_id': self.template_id,
            'name': self.name,
            'structure': [wt.value for wt in self.structure],
            'required_rules': self.required_rules,
            'level': self.level,
            'category': self.category,
            'description': self.description,
            'examples': self.examples,
        }


class BaseGrammar(ABC):
    """
    Abstract base class for language-specific grammar implementations.
    
    All language grammars must inherit from this class and implement
    the required methods.
    """
    
    # Language metadata
    language_code: str = "en"
    language_name: str = "English"
    
    # Word order patterns
    default_word_order: List[WordType] = []
    question_word_order: List[WordType] = []
    subordinate_clause_order: List[WordType] = []
    
    # Grammar rules
    rules: Dict[str, GrammarRule] = {}
    
    # Sentence templates
    templates: Dict[str, SentenceTemplate] = {}
    
    # Word database
    words: Dict[str, Word] = {}
    
    def __init__(self, settings: Optional['Settings'] = None):
        """
        Initialize the grammar.
        
        Args:
            settings: Optional settings instance
        """
        self.settings = settings
        self._initialize_rules()
        self._initialize_templates()
        self._initialize_words()
    
    @abstractmethod
    def _initialize_rules(self) -> None:
        """Initialize grammar rules for this language."""
        pass
    
    @abstractmethod
    def _initialize_templates(self) -> None:
        """Initialize sentence templates for this language."""
        pass
    
    @abstractmethod
    def _initialize_words(self) -> None:
        """Initialize word database for this language."""
        pass
    
    def get_language_info(self) -> Dict[str, Any]:
        """Get language metadata."""
        return {
            'code': self.language_code,
            'name': self.language_name,
            'native_name': self.language_name,  # Can be overridden
        }
    
    def get_rules(self) -> Dict[str, GrammarRule]:
        """Get all grammar rules."""
        return self.rules
    
    def get_rule(self, rule_id: str) -> Optional[GrammarRule]:
        """Get a specific grammar rule by ID."""
        return self.rules.get(rule_id)
    
    def get_rules_by_category(self, category: str) -> List[GrammarRule]:
        """Get rules by category."""
        return [rule for rule in self.rules.values() if rule.category == category]
    
    def get_rules_by_level(self, level: int) -> List[GrammarRule]:
        """Get rules by difficulty level."""
        return [rule for rule in self.rules.values() if rule.level == level]
    
    def get_templates(self) -> Dict[str, SentenceTemplate]:
        """Get all sentence templates."""
        return self.templates
    
    def get_template(self, template_id: str) -> Optional[SentenceTemplate]:
        """Get a specific template by ID."""
        return self.templates.get(template_id)
    
    def get_templates_by_level(self, level: int) -> List[SentenceTemplate]:
        """Get templates by difficulty level."""
        return [tmpl for tmpl in self.templates.values() if tmpl.level == level]
    
    def get_templates_by_category(self, category: str) -> List[SentenceTemplate]:
        """Get templates by category."""
        return [tmpl for tmpl in self.templates.values() if tmpl.category == category]
    
    def get_words(self) -> Dict[str, Word]:
        """Get all words in the database."""
        return self.words
    
    def get_word(self, word_text: str) -> Optional[Word]:
        """Get a word by its text."""
        return self.words.get(word_text.lower())
    
    def get_words_by_type(self, word_type: WordType) -> List[Word]:
        """Get words by type."""
        return [word for word in self.words.values() if word.word_type == word_type]
    
    @abstractmethod
    def validate_sentence(self, sentence: List[Word]) -> Tuple[bool, List[str]]:
        """
        Validate a sentence against grammar rules.
        
        Args:
            sentence: List of Word objects
            
        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        pass
    
    @abstractmethod
    def generate_sentence(self, template_id: str = None, level: int = None) -> List[Word]:
        """
        Generate a random sentence.
        
        Args:
            template_id: Optional template ID to use
            level: Optional difficulty level
            
        Returns:
            List of Word objects forming a valid sentence
        """
        pass
    
    @abstractmethod
    def get_word_order(self, sentence_type: SentenceType = SentenceType.STATEMENT) -> List[WordType]:
        """
        Get the expected word order for a sentence type.
        
        Args:
            sentence_type: Type of sentence
            
        Returns:
            List of WordType in expected order
        """
        pass
    
    def get_verb_conjugation(self, verb: Word, person: int = 3, number: str = "singular", tense: str = "present") -> str:
        """
        Get the conjugated form of a verb.
        
        Args:
            verb: The verb to conjugate
            person: 1, 2, or 3
            number: 'singular' or 'plural'
            tense: 'present', 'past', 'future', etc.
            
        Returns:
            The conjugated verb form
        """
        # Default implementation - override for specific languages
        if tense == "past" and verb.past_tense:
            return verb.past_tense
        return verb.text
    
    def get_article(self, noun: Word) -> str:
        """
        Get the appropriate article for a noun.
        
        Args:
            noun: The noun
            
        Returns:
            The article (e.g., 'a', 'an', 'the', or empty string)
        """
        # Default implementation - override for specific languages
        return ""
    
    def get_negation_word(self) -> str:
        """
        Get the negation word for this language.
        
        Returns:
            The negation word (e.g., 'not', 'ikke', 'ne')
        """
        return "not"
    
    def get_question_word(self, question_type: str = "yes_no") -> str:
        """
        Get the question word for a question type.
        
        Args:
            question_type: Type of question ('yes_no', 'who', 'what', 'where', etc.)
            
        Returns:
            The question word
        """
        return ""
    
    def shutdown(self) -> None:
        """Clean up resources."""
        pass
