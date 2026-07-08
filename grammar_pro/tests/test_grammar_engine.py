"""
Tests for the Grammar Engine.
"""

import unittest
from grammar_pro.grammar.grammar_engine import GrammarEngine
from grammar_pro.grammar.danish_grammar import DanishGrammar
from grammar_pro.config.settings import Settings


class TestGrammarEngine(unittest.TestCase):
    """Test cases for GrammarEngine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.settings = Settings()
        self.engine = GrammarEngine(self.settings)
    
    def test_initialization(self):
        """Test that GrammarEngine initializes correctly."""
        self.assertIsNotNone(self.engine)
        self.assertTrue(self.engine._initialized)
    
    def test_get_available_languages(self):
        """Test getting available languages."""
        languages = self.engine.get_available_languages()
        self.assertIsInstance(languages, list)
        self.assertGreater(len(languages), 0)
        
        # Check that Danish is available
        language_codes = [lang['code'] for lang in languages]
        self.assertIn('da', language_codes)
    
    def test_get_grammar(self):
        """Test getting a grammar by language code."""
        # Get Danish grammar
        grammar = self.engine.get_grammar('da')
        self.assertIsNotNone(grammar)
        self.assertIsInstance(grammar, DanishGrammar)
        
        # Get non-existent grammar
        grammar = self.engine.get_grammar('xx')
        self.assertIsNone(grammar)
    
    def test_has_language(self):
        """Test checking if a language is available."""
        self.assertTrue(self.engine.has_language('da'))
        self.assertFalse(self.engine.has_language('xx'))
    
    def test_generate_sentence(self):
        """Test generating a sentence."""
        sentence = self.engine.generate_sentence(language_code='da')
        self.assertIsInstance(sentence, list)
        self.assertGreater(len(sentence), 0)
    
    def test_get_word_order(self):
        """Test getting word order."""
        from grammar_pro.grammar.base_grammar import SentenceType
        
        word_order = self.engine.get_word_order(
            sentence_type=SentenceType.STATEMENT,
            language_code='da'
        )
        self.assertIsInstance(word_order, list)
        self.assertGreater(len(word_order), 0)
    
    def test_get_rules(self):
        """Test getting grammar rules."""
        rules = self.engine.get_rules('da')
        self.assertIsInstance(rules, dict)
        self.assertGreater(len(rules), 0)
    
    def test_get_rule(self):
        """Test getting a specific rule."""
        rule = self.engine.get_rule('da_subject_verb', 'da')
        self.assertIsNotNone(rule)
        
        rule = self.engine.get_rule('nonexistent_rule', 'da')
        self.assertIsNone(rule)
    
    def test_get_rules_by_category(self):
        """Test getting rules by category."""
        rules = self.engine.get_rules_by_category('word_order', 'da')
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
    
    def test_get_rules_by_level(self):
        """Test getting rules by level."""
        rules = self.engine.get_rules_by_level(1, 'da')
        self.assertIsInstance(rules, list)
    
    def test_get_templates(self):
        """Test getting templates."""
        templates = self.engine.get_templates('da')
        self.assertIsInstance(templates, dict)
        self.assertGreater(len(templates), 0)
    
    def test_get_template(self):
        """Test getting a specific template."""
        template = self.engine.get_template('da_sv', 'da')
        self.assertIsNotNone(template)
        
        template = self.engine.get_template('nonexistent_template', 'da')
        self.assertIsNone(template)
    
    def test_get_words(self):
        """Test getting words."""
        words = self.engine.get_words('da')
        self.assertIsInstance(words, dict)
        self.assertGreater(len(words), 0)
    
    def test_get_word(self):
        """Test getting a specific word."""
        word = self.engine.get_word('jeg', 'da')
        self.assertIsNotNone(word)
        
        word = self.engine.get_word('nonexistent', 'da')
        self.assertIsNone(word)


if __name__ == '__main__':
    unittest.main()
