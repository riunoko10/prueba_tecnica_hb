from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from src.shared.infraestructure.shared_handler import handle_healh
from src.properties.infraestructure.properties_handler import handle_property


class APIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_string = parsed_path.query


            if path == '/api/health':
                response = handle_healh()
            
            elif path == '/api/properties':
                response = handle_property(path=path, query=query_string )
            
            else:
                response = {
                    'status': 404,
                    'content_type': 'application/json',
                    'content': json.dumps({'error': 'Ruta no encontrada'})
                }
            
            self.send_response(response['status'])
            self.send_header('Content-type', response['content_type'])
            self.end_headers()
            self.wfile.write(response['content'].encode())
        except Exception as e:
            error_response = {
                'status': 500,
                'content_type': 'application/json',
                'content': json.dumps({'error': str(e)})
            }
            self.send_response(error_response['status'])
            self.send_header('Content-type', error_response['content_type'])
            self.end_headers()
            self.wfile.write(error_response['content'].encode())



def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, APIHandler)
    print(f'Servidor iniciado en http://localhost:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()