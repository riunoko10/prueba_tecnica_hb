import pytest
from unittest.mock import patch, MagicMock
from src.properties.infraestructure.mysql_repository import MySQLPropertyRepository
from src.properties.domain.schemas import PropertyResponse, PropertyRequest



mock_data = [
    {
        'direccion': 'Cra 45 #10-23',
        'ciudad': 'Medellín',
        'estado': 'pre_venta',
        'precio_venta': 250000000,
        'descripcion': 'Apartamento en excelente ubicación'
    },
    {
        'direccion': 'Cra 54 #11-22',
        'ciudad': 'Bogota',
        'estado': 'venta',
        'precio_venta': 280000000,
        'descripcion': 'Apartamento en excelente ubicación'
    },
    {
        'direccion': None,
        'ciudad': 'Bogota',
        'estado': 'venta',
        'precio_venta': 280000000,
        'descripcion': 'Apartamento en excelente ubicación'
    },
]


@pytest.fixture
def mock_mysql_connection():
    with patch('src.properties.infraestructure.mysql_repository.MySQLConnectionPool') as mock_pool_class:
        mock_pool = MagicMock()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_pool_class.return_value = mock_pool
        mock_pool.get_connection.return_value = mock_conn
        mock_pool.is_connected.return_value = True
        mock_pool.close_connection.return_value = None
        
        mock_conn.cursor.return_value = mock_cursor

        def mock_execute(query, params=None):
            if params:
                pass
            else:
                mock_cursor.fetchall.return_value = mock_data

        mock_cursor.execute = MagicMock(side_effect=mock_execute)
        yield mock_cursor, mock_conn, mock_pool


def test_get_wihtout_filters(mock_mysql_connection):
    mock_cursor, mock_conn, mock_pool = mock_mysql_connection
    repo = MySQLPropertyRepository()

    resultados = repo.get_all()

    expected_data = repo._parse_data(mock_data)

    print(f"resultados: {resultados}")
    print(f"expected_data: {expected_data}")

    assert len(resultados) == len(expected_data)
    assert resultados[0].ciudad == expected_data[0].ciudad
 
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_pool.close_connection.assert_called_once()
