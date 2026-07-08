"""
Core module for Grammar Pro addon.

Contains the main addon manager, Anki integration, and core functionality.
"""

from .addon_manager import AddonManager
from .anki_integration import setup_anki_hooks

__all__ = ["AddonManager", "setup_anki_hooks"]
