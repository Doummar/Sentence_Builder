"""
Persistence module for Grammar Pro.

Handles data storage and retrieval for exercises, statistics, and user data.
"""

from .data_manager import DataManager
from .storage_backend import StorageBackend

__all__ = ["DataManager", "StorageBackend"]
