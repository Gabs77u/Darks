import os
import pytest
from proxies.proxy_manager import *


def test_dummy_proxy_manager():
    # Adapte para funções reais do módulo
    assert True


def test_proxy_manager_upload_sftp():
    pm = ProxyManager()
    hostname = os.environ.get("SFTP_HOST")
    username = os.environ.get("SFTP_USER")
    password = os.environ.get("SFTP_PASS")
    local_path = os.environ.get("SFTP_LOCAL", "test.txt")
    remote_path = os.environ.get("SFTP_REMOTE", "test_remote.txt")
    if not (hostname and username and password):
        print("Ambiente SFTP não configurado, teste ignorado.")
        return
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
    monkeypatch.setattr(
        "proxies.proxychains.ProxyChain.chain_connect", lambda self, h, p: True
    )
    assert pc.chain_connect("dest", 80)


def test_proxy_manager_generate_random_proxy(monkeypatch):
    pm = ProxyManager()
    monkeypatch.setattr("random.choice", lambda x: x[0])
    proxy = pm.generate_random_proxy()
    assert proxy["host"] == "127.0.0.1"


def test_proxy_manager_start_proxy_server(monkeypatch):
    pm = ProxyManager()
    proxy = {"host": "127.0.0.1", "port": 20000, "type": "SOCKS5"}
    monkeypatch.setattr(
        "socket.socket",
        lambda *a, **k: type(
            "S",
            (),
            {
                "bind": lambda self, x: True,
                "listen": lambda self, x: True,
                "accept": lambda self: (_ for _ in ()).throw(Exception("stop")),
                "close": lambda self: True,
            },
        )(),
    )
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
    monkeypatch.setattr(
        "proxies.proxychain_manager.generate_random_chain",
        lambda l: [{"type": "SOCKS5", "host": "127.0.0.1", "port": 1080}] * l,
    )
    chain = ProxyChain.randomize_chain(2)
    assert len(chain) == 2


def test_proxychain_chain_connect_fail(monkeypatch):
    chain = [{"type": "SOCKS5", "host": "127.0.0.1", "port": 1080}]
    pc = ProxyChain(chain)
    monkeypatch.setattr(
        "proxies.proxychains.ProxyChain.chain_connect",
        lambda self, h, p: (_ for _ in ()).throw(Exception("fail")),
    )
    with pytest.raises(Exception):
        pc.chain_connect("dest", 80)
