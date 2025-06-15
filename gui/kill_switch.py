import logging
import os
import platform
import requests
import subprocess
import traceback
from datetime import datetime
from gui.privacy_config import load_config
from crypto.security_protocols import generate_secure_random_bytes

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


def enable_kill_switch():
    config = load_config()
    if not config.get("kill_switch", True):
        return
    kill_token = generate_secure_random_bytes(8).hex()
    # O token pode ser usado para logs ou auditoria segura
    if platform.system() == "Windows":
        subprocess.call("netsh advfirewall set allprofiles state on", shell=True)
        subprocess.call(
            'netsh advfirewall firewall add rule name="KillSwitch" dir=out action=block remoteip=0.0.0.0/0',
            shell=True,
        )
    else:
        subprocess.call("iptables -I OUTPUT ! -o wg0 -j DROP", shell=True)


def disable_kill_switch():
    if platform.system() == "Windows":
        subprocess.call(
            'netsh advfirewall firewall delete rule name="KillSwitch"', shell=True
        )
    else:
        subprocess.call("iptables -D OUTPUT ! -o wg0 -j DROP", shell=True)
