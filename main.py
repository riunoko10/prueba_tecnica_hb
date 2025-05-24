from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from src.shared.infraestructure.api.v1.shared_handler import handle_health
from src.properties.infraestructure.api.v1.properties_handler import handle_property
from src.shared.infraestructure.logger import get_logger
from src.shared.infraestructure.api.v1.response_models import Response

logger = get_logger(__name__)

class APIHandler(BaseHTTPRequestHandler):
    """
    APIHandler is a subclass of BaseHTTPRequestHandler that handles HTTP GET requests for a RESTful API.
    Methods
    -------
    _handle_response(handler_response):
        Sends an HTTP response to the client using the provided handler_response dictionary, which should contain
        'status', 'content_type', and 'content' keys.
    do_GET():
        Handles HTTP GET requests. Routes requests based on the URL path:
            - '/api/v1/health': Calls handle_health() to return the health status of the API.
            - '/api/v1/properties': Calls handle_property() with the current path and query string to return property data.
            - Any other path: Returns a 404 error response.
        Catches exceptions, logs the error, and returns an error response.
    """

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
        self.end_headers()
        self.wfile.write(handler_response['content'].encode())

    def do_GET(self):
        try:

            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_string = parsed_path.query

            if path == '/api/v1/health':
                response = handle_health()
            elif path == '/api/v1/properties':
                response = handle_property(path=path, query=query_string)
            else:
                response = Response.error('Ruta no encontrada', 404)
            self._handle_response(response)
        except Exception as e:
            logger.info(f"{e}")
            response = Response.error(str(e))
            self._handle_response(response)


def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, APIHandler)
    logger.info(f'Servidor iniciado en http://localhost:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()