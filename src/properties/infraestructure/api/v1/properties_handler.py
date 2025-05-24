import json
from urllib.parse import parse_qs
from src.properties.domain.schemas import PropertyRequest, PropertyState
from src.properties.application.value_objects import CreateProperty
from src.properties.infraestructure.mysql_repository import MySQLPropertyRepository
from src.shared.infraestructure.api.v1.response_models import Response
from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)


def handle_property(path, query=None) -> dict:
    try:
        mysql_repository = MySQLPropertyRepository()


        if query:
            filtros = {k: v[0] for k, v in parse_qs(query, separator="?").items()}
            
            filtros['estado'] = PropertyState(filtros['estado'])
            property_request = PropertyRequest(**filtros)
            result_property = CreateProperty(mysql_repository).find_properties(property_request)
        else:
            result_property = CreateProperty(mysql_repository).find_properties()

        dict_property = [prop.model_dump() for prop in result_property]

        return  Response.success({"data": dict_property})

    except Exception as e:
        logger.info(f"Ha ocurrido un error en handle_property: {e}")
        return Response.error(str(e))