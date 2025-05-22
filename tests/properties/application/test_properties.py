import pytest
import httpx


def test_get_property_endpoint(client):
    """Prueba el endpoint de health check"""
    try:
        response = client.get('/api/properties')
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data
        assert data['data'] == 'ok'
    except httpx.ConnectError as e:
        pytest.fail(f"No se pudo conectar al servidor: {str(e)}")