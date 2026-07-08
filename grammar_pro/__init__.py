"""
Grammar Pro - Anki Addon for Learning Sentence Construction and Grammar

A comprehensive addon that teaches language learners how to THINK when building
sentences through thousands of small grammar decisions.

Architecture:
- Core: Main addon integration with Anki
- Grammar: Modular grammar engine per language
- Exercises: Exercise generators and validators
- UI: Qt6-based user interfaces
- Statistics: Learning analytics and adaptive learning
- Persistence: Data storage and retrieval
- Config: Configuration management
- Languages: Language-specific grammar definitions
"""

from .core.addon_manager import AddonManager
from .config.settings import Settings

__version__ = "1.0.0"
__author__ = "Grammar Pro Team"

# Initialize settings
settings = Settings()

# Addon manager instance
addon_manager = AddonManager()


def init_addon():
    """Initialize the Grammar Pro addon."""
    from .core.anki_integration import setup_anki_hooks
    setup_anki_hooks()
    return addon_manager


def get_addon_manager():
    """Get the addon manager instance."""
    return addon_manager
