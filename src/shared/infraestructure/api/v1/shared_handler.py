import json
import time
import platform
from datetime import datetime, timezone
from src.shared.infraestructure.api.v1.response_models import Response
from src.shared.infraestructure.logger import get_logger
from src.shared.infraestructure.database.mysql_pool import MySQLConnectionPool
from src.shared.infraestructure.config import config
from src.shared.infraestructure.cache import cache

logger = get_logger(__name__)

def handle_health():
    """
    Enhanced health check endpoint with system information and database pool stats.

    Returns:
        Response: A success response with detailed health information including:
                  - Basic status
                  - System information
                  - Database connection pool stats
                  - Cache statistics
                  - Configuration info
    """
    try:
        # Basic health info
        health_data = {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "Properties API",
            "version": "1.0.0"
        }
        
        # System information
        health_data["system"] = {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "architecture": platform.architecture()[0],
        }
        
        # Configuration status
        health_data["config"] = {
            "debug_mode": config.is_debug(),
            "server": {
                "host": config.get('server.host'),
                "port": config.get('server.port')
            }
        }
        
        # Cache statistics
        health_data["cache"] = cache.get_stats()
        
        # Try to get database pool stats
        try:
            pool = MySQLConnectionPool()
            health_data["database"] = {
                "pool_stats": pool.get_pool_stats(),
                "status": "connected"
            }
        except Exception as db_error:
            health_data["database"] = {
                "status": "error",
                "error": str(db_error)
            }
            # Don't fail the health check just because DB is down
            logger.warning(f"Database health check failed: {db_error}")
        
        return Response.success(health_data)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return Response.error({'error': str(e)})
