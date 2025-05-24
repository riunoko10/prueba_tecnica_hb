import json

class Response:
    """
    Response utility class for formatting API responses in JSON.
    Methods
    -------
    success(data, status=200)
        Returns a successful JSON response with the given data and HTTP status code.
    error(message, status=500)
        Returns an error JSON response with the given error message and HTTP status code.
    """
    @staticmethod
    def success(data, status=200):
        return {
            'status': status,
            'content_type': 'application/json',
            'content': json.dumps(data)
        }

    @staticmethod
    def error(message, status=500):
        return {
            'status': status,
            'content_type': 'application/json',
            'content': json.dumps({'error': message})
        }