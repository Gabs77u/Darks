import os
from gui.privacy_config import get_or_create_key, AESCipher
from datetime import datetime


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
