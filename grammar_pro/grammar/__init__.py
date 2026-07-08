"""
Grammar Engine module for Grammar Pro.

Provides the modular grammar engine that can be extended for any language.
"""

from .grammar_engine import GrammarEngine
from .base_grammar import BaseGrammar
from .danish_grammar import DanishGrammar
from .english_grammar import EnglishGrammar

__all__ = ["GrammarEngine", "BaseGrammar", "DanishGrammar", "EnglishGrammar"]
