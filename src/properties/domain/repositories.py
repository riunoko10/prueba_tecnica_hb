from abc import ABC, abstractmethod
from src.properties.domain.value_objects import PropertyResponse, PropertyRequest


class PropertyRepository(ABC):
    @abstractmethod
    def get_all(self, params) -> list[PropertyResponse]: ...



class MySQLPropertyRepository(PropertyRepository):

    def get_all(self, property:PropertyRequest)-> list[PropertyResponse]:
        pass


    def _extract_filters(self, property: PropertyRequest) -> str:
        pass