import subprocess
import platform
from gui.privacy_config import load_config
from crypto.security_protocols import generate_secure_random_bytes
import logging
import os
import requests
import traceback
from datetime import datetime

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
    print("Ocorreu um erro inesperado. Tente novamente ou contate o suporte.")


def set_secure_dns():
    config = load_config()
    if not config.get("secure_dns", True):
        return
    dns = config.get("custom_dns") or "1.1.1.1"
    dns_session_id = generate_secure_random_bytes(8).hex()
    # O identificador pode ser usado para logs ou auditoria segura
    try:
        if platform.system() == "Windows":
            subprocess.call(
                f'netsh interface ip set dns name="Ethernet" static {dns}', shell=True
            )
        else:
            subprocess.call(f"resolvectl dns eth0 {dns}", shell=True)
    except Exception as e:
        handle_exception(
            e, context={"funcao": "set_secure_dns", "parametros": {"dns": dns}}
        )
