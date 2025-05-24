import json

class Response:
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