from abc import ABC, abstractmethod
from typing import Any


class DatabaseConnection(ABC):
    """Abstract database connection interface"""
    
    @abstractmethod
    def get_connection(self) -> Any:
        """Get a database connection"""
        pass
    
    @abstractmethod
    def close_connection(self, connection: Any) -> None:
        """Close a database connection"""
        pass
    
    @abstractmethod
    def is_connected(self, connection: Any) -> bool:
        """Check if connection is active"""
        pass