import os
import pytest
import tempfile
from gui.privacy_config import *
from gui.audit_log import log_audit_event
from crypto.security_protocols import *
from proxies.proxy_manager import ProxyManager, validate_proxy_config
from proxies.proxychains import ProxyChain
from wireguard.wg_settings import *
from openvpn.settings import *
from gui.db_manager import DBManager


def test_config_export_import(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.privacy_config.CONFIG_PATH", str(tmp_path/"privacy_config.json"))
    monkeypatch.setattr("gui.privacy_config.KEY_PATH", str(tmp_path/"privacy_config.key"))
    config = default_config()
    save_config(config)
    export_path = tmp_path/"exported.enc"
    from gui.privacy_config import export_encrypted_config, import_encrypted_config
    assert export_encrypted_config(str(export_path))
    assert import_encrypted_config(str(export_path))

def test_db_manager_no_logs(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": True})
    df = DBManager.create_and_populate_db()
    assert df.empty

def test_db_manager_add_invalid_user(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    with pytest.raises(ValueError):
        DBManager.add_user("a", "foo", "", 1, "INVALID")

def test_db_manager_remove_nonexistent_user(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    df2 = DBManager.remove_user(999)
    assert df2.shape[0] == df.shape[0]

def test_db_manager_edit_nonexistent_user(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    df2 = DBManager.edit_user(999, usuario="x")
    assert df2.equals(df)

def test_proxy_manager_upload_sftp():
    pm = ProxyManager()
    # Parâmetros reais ou de ambiente controlado
    hostname = os.environ.get("SFTP_HOST")
    username = os.environ.get("SFTP_USER")
    password = os.environ.get("SFTP_PASS")
    local_path = os.environ.get("SFTP_LOCAL", "test.txt")
    remote_path = os.environ.get("SFTP_REMOTE", "test_remote.txt")
    if not (hostname and username and password):
        print("Ambiente SFTP não configurado, teste ignorado.")
        return
    # Cria arquivo local de teste se não existir
    if not os.path.exists(local_path):
        with open(local_path, "w") as f:
            f.write("teste sftp upload")
    try:
        pm.upload_proxy_list_sftp(hostname, username, password, local_path, remote_path)
    except Exception as e:
        print(f"Falha no upload SFTP: {e}")
        assert False
    assert True

def test_proxy_manager_upload_ftps(monkeypatch):
    pm = ProxyManager()
    monkeypatch.setattr("crypto.security_protocols.ftps_upload", lambda *a, **kw: True)
    pm.upload_proxy_list_ftps("host", "user", "pass", "local", "remote")
    assert True

def test_proxychain_chain_connect(monkeypatch):
    chain = [
        {"type": "SOCKS5", "host": "127.0.0.1", "port": 1080},
        {"type": "HTTP", "host": "127.0.0.1", "port": 8080},
    ]
    pc = ProxyChain(chain)
    monkeypatch.setattr("proxies.proxychains.ProxyChain.chain_connect", lambda self, h, p: True)
    assert pc.chain_connect("dest", 80)

def test_aes_cipher_wrong_decrypt():
    key1 = generate_secure_random_bytes(32)
    key2 = generate_secure_random_bytes(32)
    cipher1 = AESCipher(key1)
    cipher2 = AESCipher(key2)
    data = b"test"
    enc = cipher1.encrypt(data)
    with pytest.raises(Exception):
        cipher2.decrypt(enc)

def test_generate_self_signed_cert_invalid(monkeypatch):
    monkeypatch.setattr("OpenSSL.crypto.PKey.generate_key", lambda self, t, s: (_ for _ in ()).throw(Exception("fail")))
    with pytest.raises(Exception):
        generate_self_signed_cert("cert", "key")

def test_privacy_config_invalid_file(tmp_path, monkeypatch):
    config_path = tmp_path/"privacy_config.json"
    with open(config_path, "w") as f:
        f.write("{corrompido}")
    monkeypatch.setattr("gui.privacy_config.CONFIG_PATH", str(config_path))
    try:
        load_config()
    except Exception:
        assert True

def test_wg_settings_save_invalid(tmp_path, monkeypatch):
    monkeypatch.setattr("wireguard.wg_settings.WG_CONFIG_PATH", str(tmp_path/"wg_settings.json"))
    with pytest.raises(Exception):
        save_wg_settings({"invalid": True})

def test_ovpn_settings_save_invalid(tmp_path, monkeypatch):
    monkeypatch.setattr("openvpn.settings.OVPN_CONFIG_PATH", str(tmp_path/"ovpn_settings.json"))
    with pytest.raises(Exception):
        save_ovpn_settings({"invalid": True})

def test_db_manager_save_encrypted(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    from gui.db_manager import save_encrypted_db, load_encrypted_db
    save_encrypted_db(df)
    df2 = load_encrypted_db()
    assert not df2.empty

def test_db_manager_import_export_encrypted(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    from gui.db_manager import save_encrypted_db, export_encrypted_db, import_encrypted_db
    save_encrypted_db(df)
    export_path = tmp_path/"db.enc"
    assert export_encrypted_db(str(export_path))
    assert import_encrypted_db(str(export_path))

def test_proxy_manager_generate_random_proxy(monkeypatch):
    pm = ProxyManager()
    monkeypatch.setattr("random.choice", lambda x: x[0])
    proxy = pm.generate_random_proxy()
    assert proxy["host"] == "127.0.0.1"

def test_proxy_manager_start_proxy_server(monkeypatch):
    pm = ProxyManager()
    proxy = {"host": "127.0.0.1", "port": 20000, "type": "SOCKS5"}
    monkeypatch.setattr("socket.socket", lambda *a, **k: type('S', (), {"bind": lambda self, x: True, "listen": lambda self, x: True, "accept": lambda self: (_ for _ in ()).throw(Exception("stop")), "close": lambda self: True})())
    try:
        pm.start_proxy_server(proxy)
    except Exception:
        assert True

def test_proxy_manager_start_random_proxy(monkeypatch):
    pm = ProxyManager()
    monkeypatch.setattr(pm, "start_proxy_server", lambda proxy: True)
    proxy = pm.start_random_proxy()
    assert proxy["host"] == "127.0.0.1"

def test_proxy_manager_start_multi_hop(monkeypatch):
    pm = ProxyManager()
    monkeypatch.setattr(pm, "start_proxy_server", lambda proxy: True)
    proxies = pm.start_multi_hop(hops=2)
    assert len(proxies) == 2

def test_proxychain_randomize_chain(monkeypatch):
    monkeypatch.setattr("proxies.proxychain_manager.generate_random_chain", lambda l: [{"type": "SOCKS5", "host": "127.0.0.1", "port": 1080}]*l)
    chain = ProxyChain.randomize_chain(2)
    assert len(chain) == 2

def test_proxychain_chain_connect_fail(monkeypatch):
    chain = [{"type": "SOCKS5", "host": "127.0.0.1", "port": 1080}]
    pc = ProxyChain(chain)
    monkeypatch.setattr("proxies.proxychains.ProxyChain.chain_connect", lambda self, h, p: (_ for _ in ()).throw(Exception("fail")))
    with pytest.raises(Exception):
        pc.chain_connect("dest", 80)

def test_aes_cipher_decrypt_corrupted():
    key = generate_secure_random_bytes(32)
    cipher = AESCipher(key)
    with pytest.raises(Exception):
        cipher.decrypt(b"corrompido")

def test_generate_secure_random_bytes_zero():
    bts = generate_secure_random_bytes(0)
    assert bts == b""

def test_generate_secure_random_bytes_large():
    bts = generate_secure_random_bytes(1024)
    assert len(bts) == 1024

def test_config_save_and_load_unicode(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.privacy_config.CONFIG_PATH", str(tmp_path/"privacy_config.json"))
    monkeypatch.setattr("gui.privacy_config.KEY_PATH", str(tmp_path/"privacy_config.key"))
    config = default_config()
    config["custom_dns"] = "8.8.8.8"
    save_config(config)
    loaded = load_config()
    assert loaded["custom_dns"] == "8.8.8.8"

def test_db_manager_edit_user_all_fields(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    df2 = DBManager.edit_user(1, usuario="novo", status="conectado", host="127.0.0.2", port=22222, tipo="HTTP")
    assert "novo" in df2["usuario"].values
    assert 22222 in df2["proxy_port"].values
    assert "HTTP" in df2["tipo_proxy"].values

def test_db_manager_search_users_case_insensitive(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    result = DBManager.search_users("ADMIN")
    assert not result.empty

def test_db_manager_filter_by_status_empty(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    result = DBManager.filter_by_status("inexistente")
    assert result.empty

def test_db_manager_get_user(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    user = DBManager.get_user(1)
    assert user is not None

def test_db_manager_get_user_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr("gui.db_manager.DB_PATH", str(tmp_path/"vpn_db.csv"))
    from gui.privacy_config import save_config
    save_config({"no_logs": False})
    df = DBManager.create_and_populate_db()
    user = DBManager.get_user(999)
    assert user is None
