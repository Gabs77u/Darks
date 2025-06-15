import pytest
from gui.db_manager import DBManager


def test_db_manager_no_logs(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": True})
    df = DBManager.create_and_populate_db()
    assert df.empty


def test_db_manager_add_invalid_user(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    with pytest.raises(ValueError):
        DBManager.add_user("a", "foo", "", 1, "INVALID")


def test_db_manager_remove_nonexistent_user(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    df2 = DBManager.remove_user(999)
    assert df2.shape[0] == df.shape[0]


def test_db_manager_edit_nonexistent_user(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    df2 = DBManager.edit_user(999, usuario="x")
    assert df2.equals(df)


def test_db_manager_save_encrypted(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    from gui.db_manager import save_encrypted_db, load_encrypted_db

    save_encrypted_db(df)
    df2 = load_encrypted_db()
    assert not df2.empty


def test_db_manager_import_export_encrypted(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    from gui.db_manager import (
        save_encrypted_db,
        export_encrypted_db,
        import_encrypted_db,
    )

    save_encrypted_db(df)
    export_path = tmp_path / "db.enc"
    assert export_encrypted_db(str(export_path))
    assert import_encrypted_db(str(export_path))


def test_db_manager_edit_user_all_fields(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    df2 = DBManager.edit_user(
        1, usuario="novo", status="conectado", host="127.0.0.2", port=22222, tipo="HTTP"
    )
    assert "novo" in df2["usuario"].values
    assert 22222 in df2["proxy_port"].values
    assert "HTTP" in df2["tipo_proxy"].values


def test_db_manager_search_users_case_insensitive(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    result = DBManager.search_users("ADMIN")
    assert not result.empty


def test_db_manager_filter_by_status_empty(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    result = DBManager.filter_by_status("inexistente")
    assert result.empty


def test_db_manager_get_user(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    user = DBManager.get_user(1)
    assert user is not None


def test_db_manager_get_user_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path / "vpn_db.csv"))
    from gui.privacy_config import save_config

    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    user = DBManager.get_user(999)
    assert user is None
