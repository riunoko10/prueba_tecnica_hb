import json
from urllib.parse import parse_qs
from src.properties.domain.schemas import PropertyRequest, PropertyState
from src.properties.application.value_objects import CreateProperty
from src.properties.infraestructure.mysql_repository import MySQLPropertyRepository
from src.shared.infraestructure.api.v1.response_models import Response
from src.shared.infraestructure.logger import get_logger
import re

logger = get_logger(__name__)


def handle_property(path, query=None) -> dict:
    """
    Handles property retrieval based on the provided path and optional query parameters.
    Args:
        path (str): The API endpoint path for the property resource.
        query (str, optional): Query string containing filter parameters for property search.
    Returns:
        dict: A response dictionary containing either the list of found properties under the "data" key on success,
              or an error message on failure.
    Raises:
        Exception: Any exception encountered during property retrieval is caught and logged, and an error response is returned.
    """
    try:
        mysql_repository = MySQLPropertyRepository()
        if query:
            property_request = get_filter(query)
            result_property = CreateProperty(mysql_repository).find_properties(property_request)
        else:
            result_property = CreateProperty(mysql_repository).find_properties()

        dict_property = [prop.model_dump() for prop in result_property]

        return  Response.success({"data": dict_property})

    except Exception as e:
        logger.info(f"Ha ocurrido un error en handle_property: {e}")
        return Response.error(str(e))


def get_filter(query):
    """
    Parses a query string and constructs a PropertyRequest object with the extracted filters.
    Args:
        query (str): The query string containing filter parameters.
    Returns:
        PropertyRequest: An instance of PropertyRequest populated with the parsed filters.
    Raises:
        ValueError: If any of the filter values are invalid or cannot be converted to the expected type.
    Notes:
        - The function expects the query string to contain parameters such as 'estado' and 'anio'.
        - The 'estado' parameter is converted to a PropertyState enum.
        - The 'anio' parameter is converted to an integer.
        - Logs information if an error occurs during parsing or conversion.
    """
    try:
        filtros = {k: v[0] for k, v in parse_qs(query, separator="?").items()}
        if filtros.get("estado"):
            logger.info("")
            filtros['estado'] = PropertyState(filtros['estado'])

        if filtros.get("anio"):
            filtros['anio'] = int(filtros['anio'])

        property_request = PropertyRequest(**filtros)
        return property_request
    except ValueError as e:
        logger.info(f"Ha ocurrido un error en get_filter: {e} , valida los valores enviados")
        raise(e)
