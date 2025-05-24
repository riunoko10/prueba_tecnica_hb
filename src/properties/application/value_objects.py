
from src.properties.domain.repositories import PropertyRepository
from src.properties.domain.schemas import PropertyRequest, PropertyResponse
from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)

class CreateProperty:
    """
    CreateProperty is an application service class responsible for managing property-related operations.
    Attributes:
        _property_repository (PropertyRepository): Repository instance for accessing property data.
    Methods:
        __init__(property_repository: PropertyRepository):
            Initializes the CreateProperty service with a property repository.
        find_properties(property_filters: PropertyRequest = None) -> list[PropertyResponse]:
            Retrieves a list of properties based on the provided filters.
            If no filters are provided, returns all properties.
            Handles exceptions and logs errors during the retrieval process.
    Raises:
        Exception: Propagates any exceptions encountered during property retrieval.
    """

    def __init__(self, property_repository: PropertyRepository):
        self._property_repository = property_repository

    def find_properties(self, property_filters: PropertyRequest = None) -> list[PropertyResponse]:
        try:
            if property_filters:
                all_properties = self._property_repository.get_all_filters(property_filters)
            else:
                all_properties = self._property_repository.get_all()
            
            return all_properties
        except Exception as e:
            logger.error(f"Error al ejecutar la consulta con parametros: {e}")
            raise(e)





        


        
