import json
from urllib.parse import parse_qs
from src.properties.domain.schemas import PropertyRequest, PropertyState
from src.properties.application.value_objects import PropertyService
from src.properties.infraestructure.mysql_repository import MySQLPropertyRepository
from src.shared.infraestructure.api.v1.response_models import Response
from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)


def handle_property(path: str, query: str = None) -> dict:
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
        # Dependency injection - could be improved with a DI container
        mysql_repository = MySQLPropertyRepository()
        property_service = PropertyService(mysql_repository)
        
        if query:
            property_request = _parse_query_filters(query)
            result_properties = property_service.find_properties(property_request)
        else:
            result_properties = property_service.find_properties()

        # Convert to dictionaries for JSON serialization
        properties_data = [prop.model_dump() for prop in result_properties]

        return Response.success({"data": properties_data})

    except ValueError as e:
        logger.warning(f"Validation error in handle_property: {e}")
        return Response.error(f"Error de validación: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Unexpected error in handle_property: {e}")
        return Response.error("Error interno del servidor", 500)


def _parse_query_filters(query: str) -> PropertyRequest:
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
    """
    try:
        # Parse query parameters
        filters = {k: v[0] for k, v in parse_qs(query, separator="?").items()}
        
        # Validate and convert estado parameter
        if filters.get("estado"):
            filters['estado'] = PropertyState(filters['estado'])

        # Validate and convert anio parameter
        if filters.get("anio"):
            filters['anio'] = int(filters['anio'])

        return PropertyRequest(**filters)
        
    except ValueError as e:
        logger.warning(f"Invalid filter values: {e}")
        raise ValueError(f"Valores de filtro inválidos: {e}")
    except Exception as e:
        logger.error(f"Error parsing query filters: {e}")
        raise ValueError("Error procesando los parámetros de consulta")
