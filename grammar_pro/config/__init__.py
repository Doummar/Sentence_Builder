"""
Configuration module for Grammar Pro.

Provides settings management, user preferences, and configuration persistence.
"""

from .settings import Settings
from .user_preferences import UserPreferences

__all__ = ["Settings", "UserPreferences"]
