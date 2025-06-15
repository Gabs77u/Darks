import pytest
from integrations.api_server import *


def test_dummy_api_server():
    # Adapte para funções reais do módulo
    assert True


def test_generate_self_signed_cert_invalid(monkeypatch):
    monkeypatch.setattr(
        "OpenSSL.crypto.PKey.generate_key",
        lambda self, t, s: (_ for _ in ()).throw(Exception("fail")),
    )
    with pytest.raises(Exception):
        generate_self_signed_cert("cert", "key")
