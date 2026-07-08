"""
Anki Integration for Grammar Pro.

Sets up hooks and integration points with Anki's addon API.
"""

import os
from typing import Any, Callable, Optional

from anki.hooks import addHook, remHook
from aqt import mw
from aqt.utils import getText, showInfo, showWarning

from .addon_manager import AddonManager


# Global addon manager instance
_addon_manager: Optional[AddonManager] = None


def get_addon_manager() -> AddonManager:
    """Get the global addon manager instance."""
    global _addon_manager
    if _addon_manager is None:
        _addon_manager = AddonManager()
        _addon_manager.initialize()
    return _addon_manager


def setup_anki_hooks() -> None:
    """
    Set up all Anki hooks for Grammar Pro.
    
    This function should be called when the addon is loaded.
    """
    manager = get_addon_manager()
    
    # Add Grammar Pro to Anki's Tools menu
    addHook("AnkiWebView.contextMenuEvent", on_context_menu)
    
    # Add menu item to Anki's main window
    try:
        from aqt.main import AnkiQt
        addHook("AnkiQt.init", on_anki_init)
    except ImportError:
        pass
    
    # Add hook for when Anki is closing
    addHook("unloadProfile", on_unload_profile)
    
    # Add hook for when profile is loaded
    addHook("profileLoaded", on_profile_loaded)


def on_anki_init(main_window: Any) -> None:
    """
    Called when Anki's main window is initialized.
    
    Adds Grammar Pro menu items to Anki's menu bar.
    """
    from aqt import QAction
    from aqt.utils import getText
    
    manager = get_addon_manager()
    
    # Create Grammar Pro menu
    grammar_pro_menu = main_window.menuBar().addMenu("Grammar Pro")
    
    # Add actions to the menu
    
    # Open Grammar Pro
    action_open = QAction("Open Grammar Pro", main_window)
    action_open.triggered.connect(lambda: manager.show_main_window())
    grammar_pro_menu.addAction(action_open)
    
    # Dashboard
    action_dashboard = QAction("Dashboard", main_window)
    action_dashboard.triggered.connect(lambda: manager.show_dashboard())
    grammar_pro_menu.addAction(action_dashboard)
    
    # Exercise Builder
    action_builder = QAction("Exercise Builder", main_window)
    action_builder.triggered.connect(lambda: manager.show_exercise_builder())
    grammar_pro_menu.addAction(action_builder)
    
    # Settings
    grammar_pro_menu.addSeparator()
    action_settings = QAction("Settings", main_window)
    action_settings.triggered.connect(lambda: manager.show_settings_dialog())
    grammar_pro_menu.addAction(action_settings)
    
    # About
    grammar_pro_menu.addSeparator()
    action_about = QAction("About Grammar Pro", main_window)
    action_about.triggered.connect(show_about)
    grammar_pro_menu.addAction(action_about)


def on_profile_loaded() -> None:
    """Called when an Anki profile is loaded."""
    manager = get_addon_manager()
    # Reload settings for the new profile
    manager.settings.load()


def on_unload_profile() -> None:
    """Called when an Anki profile is unloaded."""
    manager = get_addon_manager()
    # Save settings before unloading
    manager.settings.save()


def on_context_menu(web_view: Any, menu: Any) -> None:
    """
    Called when a context menu is shown in Anki's web view.
    
    Adds Grammar Pro options to the context menu.
    """
    # We don't add context menu items for now
    # This hook is here for future expansion
    pass


def show_about() -> None:
    """Show the About dialog for Grammar Pro."""
    from aqt.utils import showInfo
    
    about_text = """
    <h2>Grammar Pro</h2>
    <p>Version 1.0.0</p>
    <p>A comprehensive Anki addon for learning sentence construction and grammar.</p>
    <p>Teaches language learners how to THINK when building sentences through thousands of small grammar decisions.</p>
    <p>&copy; 2024 Grammar Pro Team</p>
    """
    showInfo(about_text, title="About Grammar Pro")


def add_grammar_pro_tools_menu() -> None:
    """
    Add Grammar Pro to Anki's Tools menu.
    
    This is a fallback for older Anki versions.
    """
    try:
        from aqt import mw
        from aqt.utils import getText
        
        if mw is None:
            return
        
        # Check if menu already exists
        for action in mw.form.menuTools.actions():
            if action.text() == "Grammar Pro":
                return
        
        # Add separator if there are existing items
        if mw.form.menuTools.actions():
            mw.form.menuTools.addSeparator()
        
        # Add Grammar Pro action
        action = mw.form.menuTools.addAction("Grammar Pro")
        action.triggered.connect(lambda: get_addon_manager().show_main_window())
        
    except Exception as e:
        print(f"Error adding Grammar Pro to Tools menu: {e}")


# Initialize hooks when this module is imported
setup_anki_hooks()
