import logging
import os
import requests
import traceback
from datetime import datetime
from gui.privacy_config import get_or_create_key, AESCipher

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


def log_audit_event(event):
    try:
        key = get_or_create_key()
        aes = AESCipher(key)
        log_path = os.path.join(os.path.dirname(__file__), "audit.log.enc")
        log_entry = f"[{datetime.now().isoformat()}] {event}\n"
        logs = b""
        if os.path.exists(log_path):
            with open(log_path, "rb") as f:
                encrypted = f.read()
            try:
                logs = aes.decrypt(encrypted)
            except Exception:
                logs = b""
        logs += log_entry.encode()
        encrypted = aes.encrypt(logs)
        with open(log_path, "wb") as f:
            f.write(encrypted)
    except Exception as e:
        # Em produção, logar em local seguro
        print(f"Erro ao registrar log de auditoria: {e}")
