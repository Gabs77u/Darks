import pytest
from wireguard.manager import *
from wireguard.wg_settings import save_wg_settings


def test_dummy_wireguard():
    # Adapte para funções reais do módulo
    assert True


def test_wg_settings_save_invalid(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "wireguard.wg_settings.WG_CONFIG_PATH", str(tmp_path / "wg_settings.json")
    )
    with pytest.raises(Exception):
        save_wg_settings({"invalid": True})
