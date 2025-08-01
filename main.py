import signal
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from src.shared.infraestructure.api.v1.shared_handler import handle_health
from src.properties.infraestructure.api.v1.properties_handler import handle_property
from src.shared.infraestructure.logger import get_logger
from src.shared.infraestructure.api.v1.response_models import Response
from src.shared.infraestructure.config import config

logger = get_logger(__name__)

class APIHandler(BaseHTTPRequestHandler):
    """
    Enhanced APIHandler with improved error handling and CORS support.
    """

    def _set_cors_headers(self):
        """Set CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def _handle_response(self, handler_response):
        """
        Handles the HTTP response by sending the status code, headers, and content to the client.

        Args:
            handler_response (dict): A dictionary containing the response details with the following keys:
                - 'status' (int): The HTTP status code to send.
                - 'content_type' (str): The value for the 'Content-type' header.
                - 'content' (str): The response body content to send to the client.

        Returns:
            None
        """
        self.send_response(handler_response['status'])
        self.send_header('Content-type', handler_response['content_type'])
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(handler_response['content'].encode())

    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_string = parsed_path.query

            # Route handling
            if path == '/api/v1/health':
                response = handle_health()
            elif path == '/api/v1/properties':
                response = handle_property(path=path, query=query_string)
            else:
                response = Response.error('Ruta no encontrada', 404)
            
            self._handle_response(response)
            
        except Exception as e:
            logger.error(f"Unexpected error in GET handler: {e}")
            response = Response.error("Error interno del servidor", 500)
            self._handle_response(response)

    def log_message(self, format, *args):
        """Override to use our logger instead of default logging"""
        logger.info(f"{self.address_string()} - {format % args}")


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Recibida señal {signum}, cerrando servidor...")
    sys.exit(0)


def run_server(host: str = None, port: int = None, test_mode: bool = False):
    """
    Run the HTTP server with improved configuration and error handling.
    
    Args:
        host (str): Host to bind the server to (uses config if None)
        port (int): Port to bind the server to (uses config if None)
        test_mode (bool): If True, skip signal handlers (for testing)
    """
    # Use configuration if not provided
    server_config = config.get_server_config()
    host = host or server_config['host']
    port = port or server_config['port']
    
    server_address = (host, port)
    
    # Register signal handlers for graceful shutdown (only in main thread)
    if not test_mode:
        try:
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        except ValueError:
            # Signal handlers only work in main thread
            pass
    
    try:
        httpd = HTTPServer(server_address, APIHandler)
        logger.info(f'Servidor iniciado en http://{host}:{port}')
        if config.is_debug():
            logger.info('Modo debug activado')
        if not test_mode:
            logger.info('Presiona Ctrl+C para detener el servidor')
        httpd.serve_forever()
    except OSError as e:
        logger.error(f"Error al iniciar el servidor: {e}")
        if not test_mode:
            sys.exit(1)
        raise
    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"Error inesperado del servidor: {e}")
        if not test_mode:
            sys.exit(1)
        raise
    finally:
        logger.info("Servidor cerrado")


if __name__ == '__main__':
    run_server()