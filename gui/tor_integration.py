import subprocess
from gui.privacy_config import load_config
from crypto.security_protocols import generate_secure_random_bytes
import logging
import os
import requests
import traceback
from datetime import datetime

# Configuração avançada de logging
LOG_EXTERNAL_URL = os.getenv("LOG_EXTERNAL_URL")
LOG_USER = os.getenv("LOG_USER", "sistema")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def log_external(msg, level="info", context=None):
    if LOG_EXTERNAL_URL:
        payload = {
            "log": msg,
            "level": level,
            "user": LOG_USER,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        try:
            requests.post(LOG_EXTERNAL_URL, json=payload, timeout=2)
        except Exception as e:
            logging.error(f"Falha ao enviar log externo: {e}")


def handle_exception(e, context=None):
    tb = traceback.format_exc()
    msg = f"Erro: {e}\nTraceback: {tb}"
    logging.error(msg)
    log_external(msg, level="error", context=context)
    # Mensagem amigável para o usuário final
    print("Ocorreu um erro inesperado. Tente novamente ou contate o suporte.")


def start_tor():
    import platform
    import shutil
    import os

    config = load_config()
    if not config.get("tor_enabled", False):
        return
    session_token = generate_secure_random_bytes(16).hex()
    # O token pode ser usado para logs ou auditoria segura
    try:
        tor_cmd = "tor"
        if platform.system() == "Windows":
            possible_paths = [
                shutil.which("tor"),
                r"C:\Users\gabri\Downloads\tor-expert-bundle-windows-x86_64-14.5.3\tor\tor.exe",
                r"C:\Program Files\Tor\tor.exe",
            ]
            for path in possible_paths:
                if path and os.path.isfile(path):
                    tor_cmd = path
                    break
        subprocess.Popen([tor_cmd])
    except Exception as e:
        print("Erro ao iniciar Tor:", e)

    # (Opcional) criptografar configs sensíveis do Tor
    # Exemplo: aes = AESCipher(key); dados = aes.encrypt(b'config')
