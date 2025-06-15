import logging
import os
import requests
import traceback
from datetime import datetime
from PyQt5.QtGui import QIcon
from qtawesome import icon as qta_icon

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


def get_icon(name):
    # Ícones e cores condizentes com o tema dark, privacidade e VPN
    mapping = {
        "connect": ("fa5s.lock", "#00e676"),  # Cadeado verde (conectar)
        "disconnect": (
            "fa5s.unlock",
            "#ff1744",
        ),  # Cadeado aberto vermelho (desconectar)
        "settings": ("fa5s.cogs", "#00b8d4"),  # Engrenagem azul
        "privacy": ("fa5s.user-shield", "#ffd600"),  # Escudo amarelo
        "proxy": ("fa5s.exchange-alt", "#7c4dff"),  # Setas roxas (proxy)
        "user": ("fa5s.user-circle", "#00bfae"),  # Usuário verde-água
        "api": ("fa5s.server", "#ff9100"),  # Servidor laranja
        "search": ("fa5s.search", "#00b8d4"),  # Lupa azul
        "edit": ("fa5s.user-edit", "#ffd600"),  # Editar amarelo
        "remove": ("fa5s.user-times", "#ff1744"),  # Usuário removido vermelho
        "add": ("fa5s.user-plus", "#00e676"),  # Usuário adicionado verde
        "filter": ("fa5s.filter", "#7c4dff"),  # Filtro roxo
        "vpn": ("fa5s.shield-alt", "#00e676"),
        "vpn_on": ("fa5s.shield-alt", "#00e676"),
        "vpn_off": ("fa5s.shield-alt", "#ff1744"),
        "proxy_on": ("fa5s.exchange-alt", "#00e676"),
        "proxy_off": ("fa5s.exchange-alt", "#ff1744"),
        "tor": ("fa5s.user-secret", "#ffd600"),
        "tor_on": ("fa5s.user-secret", "#00e676"),
        "tor_off": ("fa5s.user-secret", "#ff1744"),
        "lan": ("fa5s.ethernet", "#00b8d4"),
        "wifi": ("fa5s.wifi", "#ffd600"),
        "network": ("fa5s.network-wired", "#7c4dff"),
    }
    if name in mapping:
        fa_name, color = mapping[name]
        return qta_icon(fa_name, color=color)
    return qta_icon("fa5s.question", color="#757575")
