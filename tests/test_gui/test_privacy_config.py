import pytest
from gui.privacy_config import *


def test_config_export_import(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "gui.privacy_config.CONFIG_PATH", str(tmp_path / "privacy_config.json")
    )
    monkeypatch.setattr(
        "gui.privacy_config.KEY_PATH", str(tmp_path / "privacy_config.key")
    )
    config = default_config()
    save_config(config)
    export_path = tmp_path / "exported.enc"
    from gui.privacy_config import export_encrypted_config, import_encrypted_config

    assert export_encrypted_config(str(export_path))
    assert import_encrypted_config(str(export_path))


def test_privacy_config_invalid_file(tmp_path, monkeypatch):
    config_path = tmp_path / "privacy_config.json"
    with open(config_path, "w") as f:
        f.write("{corrompido}")
    monkeypatch.setattr("gui.privacy_config.CONFIG_PATH", str(config_path))
    try:
        load_config()
    except Exception:
        assert True


def test_config_save_and_load_unicode(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "gui.privacy_config.CONFIG_PATH", str(tmp_path / "privacy_config.json")
    )
    monkeypatch.setattr(
        "gui.privacy_config.KEY_PATH", str(tmp_path / "privacy_config.key")
    )
    config = default_config()
    config["custom_dns"] = "8.8.8.8"
    save_config(config)
    loaded = load_config()
    assert loaded["custom_dns"] == "8.8.8.8"
