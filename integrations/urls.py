import logging
import os
import requests
import traceback
from datetime import datetime
from django.urls import path
from .api_base import (
    VPNStatusAPI,
    UserListAPI,
    UserDetailAPI,
    UserSearchAPI,
    UserFilterStatusAPI,
)

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


urlpatterns = [
    path("api/vpn/", VPNStatusAPI.as_view(), name="vpn-status"),
    path("api/users/", UserListAPI.as_view(), name="user-list"),
    path("api/users/<int:user_id>/", UserDetailAPI.as_view(), name="user-detail"),
    path("api/users/search/", UserSearchAPI.as_view(), name="user-search"),
    path("api/users/filter/", UserFilterStatusAPI.as_view(), name="user-filter-status"),
]
