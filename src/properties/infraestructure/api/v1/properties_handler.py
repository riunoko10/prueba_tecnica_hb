import json
from urllib.parse import parse_qs
from src.properties.domain.schemas import PropertyRequest, PropertyState
from src.shared.infraestructure.api.v1.response_models import Response
from src.shared.infraestructure.logger import get_logger
from src.shared.infraestructure.bootstrap import get_property_service
from src.shared.infraestructure.cache import cache

logger = get_logger(__name__)


def handle_property(path: str, query: str = None) -> dict:
    """
    Handles property retrieval based on the provided path and optional query parameters.
    Uses dependency injection and caching for improved performance.
    
    Args:
        path (str): The API endpoint path for the property resource.
        query (str, optional): Query string containing filter parameters for property search.
    Returns:
        dict: A response dictionary containing either the list of found properties under the "data" key on success,
              or an error message on failure.
    """
    try:
        # Create cache key based on query parameters
        cache_key = f"properties:{query or 'all'}"
        
        # Try to get from cache first
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Returning cached result for: {cache_key}")
            return Response.success({"data": cached_result, "cached": True})
        
        # Get service from DI container
        property_service = get_property_service()
        
        if query:
            property_request = _parse_query_filters(query)
            result_properties = property_service.find_properties(property_request)
        else:
            result_properties = property_service.find_properties()

        # Convert to dictionaries for JSON serialization
        properties_data = [prop.model_dump() for prop in result_properties]
        
        # Cache the result for 5 minutes
        cache.set(cache_key, properties_data, ttl=300)
        
        return Response.success({"data": properties_data, "cached": False})

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
