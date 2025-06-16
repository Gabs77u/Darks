import pytest
from wireguard.wg_settings import default_wg_settings


def test_default_wg_settings():
    settings = default_wg_settings()
    assert isinstance(settings, dict)
    assert "private_key" in settings
