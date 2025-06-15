import socket
import threading
import random
import requests
import json
import os
from .proxychain_manager import generate_random_chain, set_active_proxychain


class ProxyChain:
    def __init__(self, chain):
        """
        chain: lista de proxies, cada proxy é um dict:
        {'type': 'SOCKS5'|'SOCKS4'|'HTTP'|'HTTPS', 'host': 'ip', 'port': int}
        """
        self.chain = chain

    def request(self, url, method="GET", **kwargs):
        try:
            session = requests.Session()
            proxy_url = self._build_chain_url()
            session.proxies = {"http": proxy_url, "https": proxy_url}
            return session.request(method, url, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Erro ao fazer requisição via proxychain: {e}")

    def _build_chain_url(self):
        """
        Constrói a URL do proxy inicial da cadeia (apenas para requests).
        """
        # Para requests, só o primeiro proxy é usado, mas para encadeamento real seria necessário um proxy local customizado
        first = self.chain[0]
        proto = first["type"].lower()
        if proto == "socks5":
            proto = "socks5h"
        return f"{proto}://{first['host']}:{first['port']}"

    def chain_connect(self, dest_host, dest_port):
        try:
            sock = None
            for proxy in self.chain:
                if proxy["type"].startswith("SOCKS"):
                    import socks

                    s = socks.socksocket()
                    s.set_proxy(
                        socks.SOCKS5 if proxy["type"] == "SOCKS5" else socks.SOCKS4,
                        proxy["host"],
                        proxy["port"],
                    )
                    if sock:
                        s.connect((proxy["host"], proxy["port"]))
                    sock = s
                elif proxy["type"] in ["HTTP", "HTTPS"]:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((proxy["host"], proxy["port"]))
                    connect_str = f"CONNECT {dest_host}:{dest_port} HTTP/1.1\r\n\r\n"
                    s.sendall(connect_str.encode())
                    resp = s.recv(4096)
                    if b"200 Connection established" not in resp:
                        raise Exception("Proxy HTTP CONNECT falhou")
                    sock = s
            if sock:
                sock.connect((dest_host, dest_port))
            return sock
        except Exception as e:
            raise RuntimeError(f"Erro ao encadear proxies: {e}")

    @staticmethod
    def randomize_chain(length=3):
        chain = generate_random_chain(length)
        set_active_proxychain(chain)
        return chain


# Exemplo de uso:
# chain = [
#     {'type': 'SOCKS5', 'host': '127.0.0.1', 'port': 1080},
#     {'type': 'HTTP', 'host': '127.0.0.1', 'port': 8080}
# ]
# pc = ProxyChain(chain)
# resp = pc.request('http://ifconfig.me')
# print(resp.text)
