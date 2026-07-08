"""
Main entry point for Grammar Pro addon.

This module is loaded by Anki when the addon is enabled.
"""

from . import init_addon

# Initialize the addon when imported
addon_manager = init_addon()

# Export the addon manager for external access
__all__ = ["addon_manager"]
