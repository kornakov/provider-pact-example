import os

import pytest
from pact import Verifier
from fastapi.testclient import TestClient
from api import app
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def client():
    return TestClient(app)


broker_url = os.getenv('PACT_BROKER_URL', 'http://localhost:9292')
username = os.getenv('PACT_BROKER_USERNAME', 'username')
password = os.getenv('PACT_BROKER_PASSWORD', 'password')
provider_version = os.getenv('GITHUB_SHA', '1.0.10')
branch = os.getenv('GITHUB_REF_NAME', 'main')

def test_verify_contract(client):
    verifier = Verifier(provider="UserServiceProvider", provider_base_url="http://localhost:8011")
    # Запускаем сервер FastAPI в фоне (можно через subprocess)
    import subprocess
    proc = subprocess.Popen(["uvicorn", "provider.api:app", "--port", "8011"])

    # Верификация с публикацией результатов
    result, _= verifier.verify_with_broker(
        broker_url=broker_url,
        broker_username=username,
        broker_password=password,
        publish_version=provider_version,
        publish_verification_results=True,
        provider_version_branch=branch,
        enable_pending=False,
        verbose=True
    )

    proc.terminate()
    assert result == 0, f"Pact verification failed"