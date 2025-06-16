import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_external_services():
    # Mocka serviços externos críticos para integração
    with patch("proxies.proxy_manager.ProxyManager.connect", return_value=True), patch(
        "wireguard.manager.WireGuardManager.connect", return_value=True
    ), patch("gui.db_manager.DBManager.connect", return_value=True):
        yield


@pytest.fixture
def fake_user():
    return {"username": "testuser", "role": "admin"}


# Adicione outros fixtures/mocks conforme necessário para integração
