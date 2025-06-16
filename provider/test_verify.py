import os

import pytest
from pact.v3 import Verifier
from fastapi.testclient import TestClient
from api import app

@pytest.fixture
def client():
    return TestClient(app)

broker_url = os.getenv('PACT_BROKER_URL', 'http://localhost:9292')
username = os.getenv('PACT_BROKER_USERNAME', 'username')
password = os.getenv('PACT_BROKER_PASSWORD', 'password')

def test_verify_contract(client):
    verifier = (Verifier("UserServiceProvider")
                .add_transport(url="http://localhost:8000")
                .broker_source(url=broker_url, username=username, password=password))

    # Запускаем сервер FastAPI в фоне (можно через subprocess)
    import subprocess
    proc = subprocess.Popen(["uvicorn", "provider.api:app", "--port", "8000"])

    # Проверяем контракт
    result = verifier.verify()

    proc.terminate()
    assert result, f"Pact verification failed"