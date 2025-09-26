"""
Base repository classes and exceptions.
Infrastructure layer - common repository functionality.
"""


class RepositoryError(Exception):
    """Base exception for repository operations."""
    pass


class BaseRepository:
    """
    Base repository class with common functionality.
    Following Template Method pattern.
    """
    
    def __init__(self):
        pass