import logging
import os
import requests
import traceback
from datetime import datetime
import django
from django.core.management import execute_from_command_line
from crypto.security_protocols import generate_self_signed_cert

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


def start_django_api():
    # Garante que a API use TLS/SSL se necessário
    generate_self_signed_cert("api_cert.pem", "api_key.pem")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "integrations.django_settings")
    django.setup()
    execute_from_command_line(["manage.py", "runserver", "8000"])


if __name__ == "__main__":
    try:
        start_django_api()
    except Exception as e:
        handle_exception(e, context={"funcao": "start_django_api", "parametros": {}})
