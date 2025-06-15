import psutil
import time
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


def get_network_stats():
    stats = {}
    # Exemplo de uso de aleatório seguro para gerar um ID de sessão de monitoramento
    session_id = generate_secure_random_bytes(8).hex()
    try:
        # Interfaces e endereços
        for name, addrs in psutil.net_if_addrs().items():
            stats[name] = {
                "addresses": [a.address for a in addrs if a.family == 2],
                "isup": psutil.net_if_stats()[name].isup,
                "speed": psutil.net_if_stats()[name].speed,
                "bytes_sent": psutil.net_io_counters(pernic=True)[name].bytes_sent,
                "bytes_recv": psutil.net_io_counters(pernic=True)[name].bytes_recv,
                "session_id": session_id,
            }
    except Exception as e:
        stats["error"] = str(e)
    return stats


if __name__ == "__main__":
    while True:
        try:
            print(get_network_stats())
        except Exception as e:
            handle_exception(
                e, context={"funcao": "get_network_stats", "parametros": {}}
            )
        time.sleep(2)
