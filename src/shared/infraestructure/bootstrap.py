"""
Bootstrap script to configure dependency injection and initialize the application.
"""
from src.shared.infraestructure.container import container
from src.shared.infraestructure.database.connection import DatabaseConnection
from src.shared.infraestructure.database.mysql_pool import MySQLConnectionPool
from src.properties.domain.repositories import PropertyRepository
from src.properties.infraestructure.mysql_repository import MySQLPropertyRepository
from src.properties.application.value_objects import PropertyService
from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)

def setup_dependencies():
    """
    Configure the dependency injection container with all required services.
    """
    logger.info("Setting up dependency injection container...")
    
    # Register database connections as singletons
    container.register_singleton(
        DatabaseConnection,
        MySQLConnectionPool
    )
    
    # Register repositories as singletons (they can be shared)
    container.register_singleton(
        PropertyRepository,
        MySQLPropertyRepository
    )
    
    # Register application services as transient (new instance per request)
    container.register_transient(
        PropertyService,
        lambda: PropertyService(container.get(PropertyRepository))
    )
    
    logger.info("Dependency injection container configured successfully")

def get_property_service() -> PropertyService:
    """
    Get a PropertyService instance from the DI container.
    
    Returns:
        PropertyService instance
    """
    return container.get(PropertyService)

# Initialize dependencies when module is imported
setup_dependencies()