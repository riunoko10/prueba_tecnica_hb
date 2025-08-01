from typing import Dict, Callable, TypeVar, Type, Any
from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')

class DependencyContainer:
    """
    Simple dependency injection container for managing service dependencies.
    """
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, bool] = {}
    
    def register_singleton(self, interface: Type[T], implementation: Type[T] | Callable[[], T], name: str = None) -> None:
        """
        Register a singleton service.
        
        Args:
            interface: The interface/abstract class
            implementation: The concrete implementation or factory function
            name: Optional name for the service (defaults to interface name)
        """
        service_name = name or interface.__name__
        
        if callable(implementation) and not isinstance(implementation, type):
            # It's a factory function
            self._factories[service_name] = implementation
        else:
            # It's a class
            self._factories[service_name] = lambda: implementation()
        
        self._singletons[service_name] = True
        logger.debug(f"Registered singleton service: {service_name}")
    
    def register_transient(self, interface: Type[T], implementation: Type[T] | Callable[[], T], name: str = None) -> None:
        """
        Register a transient service (new instance each time).
        
        Args:
            interface: The interface/abstract class
            implementation: The concrete implementation or factory function
            name: Optional name for the service (defaults to interface name)
        """
        service_name = name or interface.__name__
        
        if callable(implementation) and not isinstance(implementation, type):
            # It's a factory function
            self._factories[service_name] = implementation
        else:
            # It's a class
            self._factories[service_name] = lambda: implementation()
        
        self._singletons[service_name] = False
        logger.debug(f"Registered transient service: {service_name}")
    
    def get(self, interface: Type[T], name: str = None) -> T:
        """
        Get a service instance.
        
        Args:
            interface: The interface/abstract class to get
            name: Optional name for the service (defaults to interface name)
            
        Returns:
            Service instance
            
        Raises:
            ValueError: If service not registered
        """
        service_name = name or interface.__name__
        
        if service_name not in self._factories:
            raise ValueError(f"Service {service_name} not registered")
        
        # Check if it's a singleton and already created
        if self._singletons.get(service_name, False):
            if service_name in self._services:
                return self._services[service_name]
            
            # Create singleton instance
            instance = self._factories[service_name]()
            self._services[service_name] = instance
            logger.debug(f"Created singleton instance of {service_name}")
            return instance
        else:
            # Create new instance each time
            instance = self._factories[service_name]()
            logger.debug(f"Created transient instance of {service_name}")
            return instance
    
    def clear(self) -> None:
        """Clear all registered services (useful for testing)"""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()
        logger.debug("Cleared all registered services")


# Global container instance
container = DependencyContainer()