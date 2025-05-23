import pytest
import httpx


def test_health_endpoint(client):
    """Prueba el endpoint de health check"""
    try:
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'ok'
    except httpx.ConnectError as e:
        pytest.fail(f"No se pudo conectar al servidor: {str(e)}")


def test_not_found_endpoint(client):
    
    response = client.get('/ruta-no-existente')
    assert response.status_code == 404
    data = response.json()
    assert 'error' in data