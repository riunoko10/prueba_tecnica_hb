from abc import ABC, abstractmethod
from src.properties.domain.schemas import PropertyResponse, PropertyRequest


class PropertyRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[PropertyResponse]: ...

    @abstractmethod
    def get_all_filters(self, property) -> list[PropertyResponse]: ...
