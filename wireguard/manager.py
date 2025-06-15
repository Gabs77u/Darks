import subprocess
import os
import shutil
from wireguard.wg_settings import load_wg_settings
from crypto.security_protocols import generate_self_signed_cert
import logging
import requests

logging.basicConfig(level=logging.INFO)
LOG_EXTERNAL_URL = os.getenv("LOG_EXTERNAL_URL")


def log_external(msg, level="info"):
    if LOG_EXTERNAL_URL:
        try:
            requests.post(LOG_EXTERNAL_URL, json={"log": msg, "level": level})
        except Exception as e:
            logging.error(f"Falha ao enviar log externo: {e}")


class WireGuardManager:
    @staticmethod
    def start_tunnel(config_path=None):
        # Gera arquivo temporário a partir das configurações do menu
        settings = load_wg_settings()
        conf = f"""[Interface]
PrivateKey = {settings['private_key']}
Address = {settings['address']}
DNS = {settings['dns']}

[Peer]
PublicKey = {settings['peer_public_key']}
Endpoint = {settings['endpoint']}
AllowedIPs = {settings['allowed_ips']}
PersistentKeepalive = {settings['persistent_keepalive']}
"""
        temp_conf = os.path.join(os.path.dirname(__file__), "temp_wg.conf")
        try:
            with open(temp_conf, "w") as f:
                f.write(conf)
        except Exception as e:
            logging.error(f"Erro ao criar arquivo temporário: {e}")
            log_external(f"Erro ao criar arquivo temporário: {e}", level="error")
            return False, f"Erro ao criar arquivo temporário: {e}"
        if not shutil.which("wg-quick"):
            return False, "WireGuard (wg-quick) não está instalado."
        try:
            subprocess.run(["wg-quick", "up", temp_conf], check=True)
            return True, "Conectado com sucesso."
        except subprocess.CalledProcessError as e:
            logging.error(f"Erro ao conectar: {e}")
            log_external(f"Erro ao conectar: {e}", level="error")
            return False, f"Erro ao conectar: {e}"
        except Exception as e:
            logging.error(f"Erro inesperado ao conectar: {e}")
            log_external(f"Erro inesperado ao conectar: {e}", level="error")
            return False, f"Erro inesperado ao conectar: {e}"
        finally:
            try:
                if os.path.exists(temp_conf):
                    os.remove(temp_conf)
            except Exception:
                pass  # Log do erro pode ser adicionado aqui

    @staticmethod
    def stop_tunnel(config_path=None):
        temp_conf = os.path.join(os.path.dirname(__file__), "temp_wg.conf")
        if not shutil.which("wg-quick"):
            return False, "WireGuard (wg-quick) não está instalado."
        try:
            subprocess.run(["wg-quick", "down", temp_conf], check=True)
            return True, "Desconectado com sucesso."
        except subprocess.CalledProcessError as e:
            logging.error(f"Erro ao desconectar: {e}")
            log_external(f"Erro ao desconectar: {e}", level="error")
            return False, f"Erro ao desconectar: {e}"
        except Exception as e:
            logging.error(f"Erro inesperado ao desconectar: {e}")
            log_external(f"Erro inesperado ao desconectar: {e}", level="error")
            return False, f"Erro inesperado ao desconectar: {e}"
        finally:
            try:
                if os.path.exists(temp_conf):
                    os.remove(temp_conf)
            except Exception:
                pass  # Log do erro pode ser adicionado aqui

    @staticmethod
    def is_active(interface_name):
        try:
            result = subprocess.check_output(["wg", "show", interface_name])
            return True if result else False
        except Exception:
            return False

    @staticmethod
    def ensure_tls_cert(cert_path, key_path):
        """Gera certificado TLS/SSL autoassinado se não existir."""
        if not (os.path.exists(cert_path) and os.path.exists(key_path)):
            generate_self_signed_cert(cert_path, key_path)
