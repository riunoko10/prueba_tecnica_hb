import json
from src.shared.infraestructure.api.v1.response_models import Response
from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)

def handle_health():
    """
    Handles the health check endpoint.

    Returns:
        Response: A success response with a status message if the service is healthy,
                  or an error response with the exception message if an error occurs.
    """
    try:
        return Response.success({"status": "ok"})
    except Exception as e:
        return Response.error({'error': str(e)})
