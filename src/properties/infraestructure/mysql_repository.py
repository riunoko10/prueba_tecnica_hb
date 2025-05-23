from src.properties.domain.repositories import PropertyRepository
from src.properties.domain.schemas import PropertyResponse, PropertyRequest


class MySQLPropertyRepository(PropertyRepository):

    def get_all_filter(self, property:PropertyRequest)-> list[PropertyResponse]:
        pass

    def get_all()-> list[PropertyResponse]:
        pass


    def _extract_filters(self, property: PropertyRequest) -> str:
        pass