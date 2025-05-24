
from src.properties.domain.repositories import PropertyRepository
from src.properties.domain.schemas import PropertyRequest, PropertyResponse
from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)

class CreateProperty:

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





        


        
