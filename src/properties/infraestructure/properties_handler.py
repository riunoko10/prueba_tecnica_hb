import json
from urllib.parse import parse_qs
from src.properties.domain.schemas import PropertyRequest
from src.properties.application.value_objects import CreateProperty
from src.properties.infraestructure.mysql_repository import MySQLPropertyRepository


def handle_property(path, query):
    try:
        filtros = {k: v[0] for k, v in parse_qs(query).items()}


        property_request = PropertyRequest(**filtros)
        mysql_repository = MySQLPropertyRepository()
        result_property = CreateProperty(mysql_repository).find_properties(property_request)
        return result_property

        # return {
        #     'status': 200,
        #     'content_type': 'application/json',
        #     'content': json.dumps({"data": "ok"})
        # }
    except Exception as e:
        {
            'status': 500,
            'content_type': 'application/json',
            'content': json.dumps({'error': str(e)})
        }