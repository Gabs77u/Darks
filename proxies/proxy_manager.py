import random
import socket
import threading
import logging
import os
import requests
from gui.privacy_config import load_config
from .proxychains import ProxyChain
from crypto.security_protocols import SSHManager, ftps_upload

logging.basicConfig(level=logging.INFO)
LOG_EXTERNAL_URL = os.getenv("LOG_EXTERNAL_URL")


def log_external(msg, level="info"):
    if LOG_EXTERNAL_URL:
        try:
            requests.post(LOG_EXTERNAL_URL, json={"log": msg, "level": level})
        except Exception as e:
            logging.error(f"Falha ao enviar log externo: {e}")


class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.countries = ["BR", "US", "DE", "FR", "NL", "JP"]
        self.last_country = None

    def generate_random_proxy(self):
        config = load_config()
        country = None
        if config.get("proxy_rotation", True):
            # Rotaciona entre países simulados
            available = [c for c in self.countries if c != self.last_country]
            country = random.choice(available)
            self.last_country = country
        port = random.randint(20000, 60000)
        proxy = {
            "host": "127.0.0.1",
            "port": port,
            "type": "SOCKS5",
            "country": country,
        }
        self.proxies.append(proxy)
        return proxy

    def start_proxy_server(self, proxy):
        def handle_client(client_socket):
            try:
                client_socket.close()
            except Exception:
                pass

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((proxy["host"], proxy["port"]))
            server.listen(5)
            print(
                f"Proxy SOCKS5 rodando em {proxy['host']}:{proxy['port']} ({proxy.get('country','')})"
            )
            while True:
                client, addr = server.accept()
                client_handler = threading.Thread(target=handle_client, args=(client,))
                client_handler.start()
        except Exception as e:
            logging.error(f"Erro ao iniciar proxy: {e}")
            log_external(f"Erro ao iniciar proxy: {e}", level="error")
        finally:
            try:
                server.close()
            except Exception:
                pass

    def start_random_proxy(self):
        proxy = self.generate_random_proxy()
        thread = threading.Thread(
            target=self.start_proxy_server, args=(proxy,), daemon=True
        )
        thread.start()
        return proxy

    def start_multi_hop(self, hops=2):
        # Simula multi-hop: inicia proxies em sequência
        proxies = []
        for _ in range(hops):
            proxy = self.generate_random_proxy()
            thread = threading.Thread(
                target=self.start_proxy_server, args=(proxy,), daemon=True
            )
            thread.start()
            proxies.append(proxy)
        return proxies

    def start_proxy_chain(self, chain, dest_host, dest_port):
        pc = ProxyChain(chain)
        try:
            sock = pc.chain_connect(dest_host, dest_port)
            return sock
        except Exception as e:
            logging.error(f"Erro ao encadear proxies: {e}")
            log_external(f"Erro ao encadear proxies: {e}", level="error")
            return None

    def upload_proxy_list_sftp(
        self, hostname, username, password, local_path, remote_path
    ):
        try:
            ssh = SSHManager(hostname, username, password)
            ssh.connect()
            sftp = ssh.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            ssh.close()
        except Exception as e:
            logging.error(f"Erro ao enviar lista via SFTP: {e}")
            log_external(f"Erro ao enviar lista via SFTP: {e}", level="error")

    def upload_proxy_list_ftps(self, host, username, password, local_path, dest_path):
        try:
            ftps_upload(host, username, password, local_path, dest_path)
        except Exception as e:
            logging.error(f"Erro ao enviar lista via FTPS: {e}")
            log_external(f"Erro ao enviar lista via FTPS: {e}", level="error")


def validate_proxy_config(proxy):
    errors = []
    if not proxy.get("host") or not isinstance(proxy["host"], str):
        errors.append("Host do proxy inválido.")
    if not proxy.get("port") or not (20000 <= int(proxy["port"]) <= 60000):
        errors.append("Porta do proxy fora do intervalo permitido (20000-60000).")
    if proxy.get("type") not in ["SOCKS5", "HTTP"]:
        errors.append("Tipo de proxy inválido (apenas SOCKS5 ou HTTP suportados).")
    return errors
