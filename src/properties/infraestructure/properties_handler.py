import json


def handle_property():
    try:
        return {
            'status': 200,
            'content_type': 'application/json',
            'content': json.dumps({"data": "ok"})
        }
    except Exception as e:
        {
            'status': 500,
            'content_type': 'application/json',
            'content': json.dumps({'error': str(e)})
        }