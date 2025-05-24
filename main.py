from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from src.shared.infraestructure.api.v1.shared_handler import handle_health
from src.properties.infraestructure.api.v1.properties_handler import handle_property
from src.shared.infraestructure.logger import get_logger
from src.shared.infraestructure.api.v1.response_models import Response

logger = get_logger(__name__)

class APIHandler(BaseHTTPRequestHandler):

    def _handle_response(self, handler_response):
        self.send_response(handler_response['status'])
        self.send_header('Content-type', handler_response['content_type'])
        self.end_headers()
        self.wfile.write(handler_response['content'].encode())

    def do_GET(self):
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_string = parsed_path.query

            if path == '/api/health':
                response = handle_health()
            elif path == '/api/properties':
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
    print(f'Servidor iniciado en http://localhost:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()