import pytest
from unittest.mock import patch, MagicMock
from src.properties.infraestructure.mysql_repository import MySQLPropertyRepository
from src.properties.domain.schemas import PropertyResponse, PropertyRequest



@pytest.fixture
def mock_mysql_connection():
    with patch('mysql.connector.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_connect.return_value = mock_conn
        mock_conn.is_connected.return_value = True
        mock_conn.cursor.return_value = mock_cursor

        # Datos que simula la base de datos
        mock_cursor.fetchall.return_value = [
            {
                'direccion': 'Cra 45 #10-23',
                'ciudad': 'Medellín',
                'estado': 'pre_venta',
                'precio_venta': 250000000,
                'descripcion': 'Apartamento en excelente ubicación'
            }
        ]

        yield mock_cursor, mock_conn


def test_get_wihtout_filters(mock_mysql_connection):
    mock_cursor, mock_conn = mock_mysql_connection
    repo = MySQLPropertyRepository()

    resultados = repo.get_all()

    assert len(resultados) == 1
    assert resultados[0]['ciudad'] == 'Medellín'
    assert resultados[0]['estado'] == 'pre_venta'
    assert resultados[0]['precio_venta'] == 250000000

    # Validamos que se llamó la consulta
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
