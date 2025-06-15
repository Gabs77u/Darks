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


# Exemplo de uso:
# try:
#     ...existing code...
# except Exception as e:
#     handle_exception(e, context={'funcao': 'NOME_FUNCAO', 'parametros': {...}})

SECRET_KEY = "vpn-projeto-wireguard"
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    "rest_framework",
]
MIDDLEWARE = []
ROOT_URLCONF = "integrations.urls"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
USE_TZ = True
