"""
Grammar Engine for Grammar Pro.

Central engine that manages all language-specific grammar implementations.
"""

from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from .base_grammar import BaseGrammar, Word, WordType, SentenceType
from .danish_grammar import DanishGrammar
from .english_grammar import EnglishGrammar

if TYPE_CHECKING:
    from ..config.settings import Settings


class GrammarEngine:
    """
    Central grammar engine that manages all language grammars.
    
    Provides a unified interface for:
    - Accessing language-specific grammars
    - Validating sentences
    - Generating sentences
    - Managing grammar rules
    """
    
    def __init__(self, settings: Optional['Settings'] = None):
        """
        Initialize the grammar engine.
        
        Args:
            settings: Optional settings instance
        """
        self.settings = settings
        self._grammars: Dict[str, BaseGrammar] = {}
        self._initialized = False
        
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize all registered grammars."""
        if self._initialized:
            return
        
        # Register built-in grammars
        self.register_grammar(DanishGrammar(self.settings))
        self.register_grammar(EnglishGrammar(self.settings))
        
        self._initialized = True
    
    def shutdown(self) -> None:
        """Shutdown all grammars."""
        for grammar in self._grammars.values():
            grammar.shutdown()
        self._grammars.clear()
        self._initialized = False
    
    def register_grammar(self, grammar: BaseGrammar) -> None:
        """
        Register a grammar implementation.
        
        Args:
            grammar: Grammar instance to register
        """
        self._grammars[grammar.language_code] = grammar
    
    def unregister_grammar(self, language_code: str) -> bool:
        """
        Unregister a grammar implementation.
        
        Args:
            language_code: Language code of the grammar to unregister
            
        Returns:
            True if grammar was unregistered, False if not found
        """
        if language_code in self._grammars:
            self._grammars[language_code].shutdown()
            del self._grammars[language_code]
            return True
        return False
    
    def get_grammar(self, language_code: str) -> Optional[BaseGrammar]:
        """
        Get a grammar by language code.
        
        Args:
            language_code: Language code (e.g., 'da', 'en')
            
        Returns:
            Grammar instance, or None if not found
        """
        return self._grammars.get(language_code)
    
    def get_available_languages(self) -> List[Dict[str, Any]]:
        """
        Get list of available languages.
        
        Returns:
            List of language descriptors with code, name, etc.
        """
        languages = []
        for code, grammar in self._grammars.items():
            languages.append({
                'code': code,
                'name': grammar.language_name,
                'native_name': grammar.language_name,
            })
        return languages
    
    def get_language_codes(self) -> List[str]:
        """
        Get list of available language codes.
        
        Returns:
            List of language codes
        """
        return list(self._grammars.keys())
    
    def has_language(self, language_code: str) -> bool:
        """
        Check if a language is available.
        
        Args:
            language_code: Language code to check
            
        Returns:
            True if language is available
        """
        return language_code in self._grammars
    
    def validate_sentence(self, sentence: List[Word], language_code: str = None) -> Tuple[bool, List[str]]:
        """
        Validate a sentence against grammar rules.
        
        Args:
            sentence: List of Word objects
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'  # Default to Danish
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.validate_sentence(sentence)
        
        return False, [f"Language '{language_code}' not found"]
    
    def generate_sentence(
        self, 
        template_id: str = None, 
        level: int = None, 
        language_code: str = None
    ) -> List[Word]:
        """
        Generate a random sentence.
        
        Args:
            template_id: Optional template ID to use
            level: Optional difficulty level
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            List of Word objects forming a valid sentence
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.generate_sentence(template_id, level)
        
        return []
    
    def get_word_order(
        self, 
        sentence_type: SentenceType = SentenceType.STATEMENT,
        language_code: str = None
    ) -> List[WordType]:
        """
        Get the expected word order for a sentence type.
        
        Args:
            sentence_type: Type of sentence
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            List of WordType in expected order
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_word_order(sentence_type)
        
        return []
    
    def get_rules(self, language_code: str = None) -> Dict[str, Any]:
        """
        Get all grammar rules for a language.
        
        Args:
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            Dictionary of rule_id to GrammarRule
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_rules()
        
        return {}
    
    def get_rule(self, rule_id: str, language_code: str = None) -> Optional[Any]:
        """
        Get a specific grammar rule.
        
        Args:
            rule_id: Rule identifier
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            GrammarRule, or None if not found
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_rule(rule_id)
        
        return None
    
    def get_rules_by_category(self, category: str, language_code: str = None) -> List[Any]:
        """
        Get rules by category.
        
        Args:
            category: Rule category
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            List of GrammarRule objects
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_rules_by_category(category)
        
        return []
    
    def get_rules_by_level(self, level: int, language_code: str = None) -> List[Any]:
        """
        Get rules by difficulty level.
        
        Args:
            level: Difficulty level (1-14)
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            List of GrammarRule objects
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_rules_by_level(level)
        
        return []
    
    def get_templates(self, language_code: str = None) -> Dict[str, Any]:
        """
        Get all sentence templates for a language.
        
        Args:
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            Dictionary of template_id to SentenceTemplate
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_templates()
        
        return {}
    
    def get_template(self, template_id: str, language_code: str = None) -> Optional[Any]:
        """
        Get a specific sentence template.
        
        Args:
            template_id: Template identifier
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            SentenceTemplate, or None if not found
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_template(template_id)
        
        return None
    
    def get_templates_by_level(self, level: int, language_code: str = None) -> List[Any]:
        """
        Get templates by difficulty level.
        
        Args:
            level: Difficulty level (1-14)
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            List of SentenceTemplate objects
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_templates_by_level(level)
        
        return []
    
    def get_templates_by_category(self, category: str, language_code: str = None) -> List[Any]:
        """
        Get templates by category.
        
        Args:
            category: Template category
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            List of SentenceTemplate objects
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_templates_by_category(category)
        
        return []
    
    def get_words(self, language_code: str = None) -> Dict[str, Word]:
        """
        Get all words for a language.
        
        Args:
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            Dictionary of word_text to Word
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_words()
        
        return {}
    
    def get_word(self, word_text: str, language_code: str = None) -> Optional[Word]:
        """
        Get a specific word.
        
        Args:
            word_text: Text of the word
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            Word object, or None if not found
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_word(word_text)
        
        return None
    
    def get_negation_word(self, language_code: str = None) -> str:
        """
        Get the negation word for a language.
        
        Args:
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            The negation word
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_negation_word()
        
        return "not"
    
    def get_question_word(self, question_type: str = "yes_no", language_code: str = None) -> str:
        """
        Get a question word.
        
        Args:
            question_type: Type of question
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            The question word
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_question_word(question_type)
        
        return ""
    
    def get_article(self, noun: Word, language_code: str = None) -> str:
        """
        Get the appropriate article for a noun.
        
        Args:
            noun: The noun
            language_code: Optional language code (uses default if not specified)
            
        Returns:
            The article
        """
        if language_code is None:
            if self.settings:
                language_code = self.settings.grammar.default_language
            else:
                language_code = 'da'
        
        grammar = self.get_grammar(language_code)
        if grammar:
            return grammar.get_article(noun)
        
        return ""
