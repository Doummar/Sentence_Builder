"""
Main entry point for Grammar Pro Anki Addon.

This module is loaded by Anki when the addon is enabled.
"""

import sys
import os

# Add the addon directory to the path
addon_dir = os.path.dirname(os.path.abspath(__file__))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

# Import the addon
from grammar_pro import init_addon

# Initialize the addon
addon_manager = init_addon()

# Export for Anki
__all__ = ["addon_manager"]
