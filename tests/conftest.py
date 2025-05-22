
import os
import sys
import pytest
import httpx
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import run_server

TEST_PORT = 8000
BASE_URL = f'http://localhost:{TEST_PORT}'


@pytest.fixture(scope="session", autouse=True)
def setup_test_server():
    """Configura el servidor de pruebas"""
    def is_server_running():
        try:
            with httpx.Client() as client:
                response = client.get(f'http://localhost:{TEST_PORT}/api/health')
                return response.status_code == 200
        except:
            return False

    if not is_server_running():
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        max_retries = 5
        while max_retries > 0 and not is_server_running():
            time.sleep(1)
            max_retries -= 1

        if not is_server_running():
            pytest.fail(f"No se pudo iniciar el servidor en el puerto {TEST_PORT}")


@pytest.fixture
def client():
    """Cliente HTTP para las pruebas"""
    try:
        with httpx.Client(
            base_url=BASE_URL,
            timeout=httpx.Timeout(10.0, connect=5.0)
        ) as client:
            yield client
    except Exception as e:
        pytest.fail(f"Error al crear el cliente HTTP: {str(e)}")