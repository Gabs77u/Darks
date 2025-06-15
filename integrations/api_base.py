from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gui.db_manager import DBManager
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


# Exemplo de base para integração com APIs Django/DRF
class VPNStatusAPI(APIView):
    def get(self, request):
        # Retorna status fictício da VPN
        return Response({"status": "ok", "vpn": "conectado"}, status=status.HTTP_200_OK)

    def post(self, request):
        # Aqui você pode receber comandos para conectar/desconectar a VPN
        action = request.data.get("action")
        if action == "connect":
            # Chamar função de conectar
            return Response({"result": "VPN conectada"}, status=status.HTTP_200_OK)
        elif action == "disconnect":
            # Chamar função de desconectar
            return Response({"result": "VPN desconectada"}, status=status.HTTP_200_OK)
        return Response({"error": "Ação inválida"}, status=status.HTTP_400_BAD_REQUEST)


class UserListAPI(APIView):
    def get(self, request):
        df = DBManager.load_db()
        return Response(df.to_dict(orient="records"))

    def post(self, request):
        usuario = request.data.get("usuario")
        status_ = request.data.get("vpn_status", "desconectado")
        host = request.data.get("proxy_host", "127.0.0.1")
        port = request.data.get("proxy_port", 50000)
        tipo = request.data.get("tipo_proxy", "SOCKS5")
        df = DBManager.add_user(usuario, status_, host, port, tipo)
        return Response(df.to_dict(orient="records"))


class UserDetailAPI(APIView):
    def get(self, request, user_id):
        user = DBManager.get_user(user_id)
        if user is not None:
            return Response(user.to_dict())
        return Response(
            {"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request, user_id):
        usuario = request.data.get("usuario")
        status_ = request.data.get("vpn_status")
        host = request.data.get("proxy_host")
        port = request.data.get("proxy_port")
        tipo = request.data.get("tipo_proxy")
        df = DBManager.edit_user(user_id, usuario, status_, host, port, tipo)
        return Response(df.to_dict(orient="records"))

    def delete(self, request, user_id):
        df = DBManager.remove_user(user_id)
        return Response(df.to_dict(orient="records"))


class UserSearchAPI(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        df = DBManager.search_users(query)
        return Response(df.to_dict(orient="records"))


class UserFilterStatusAPI(APIView):
    def get(self, request):
        status_ = request.GET.get("status", "")
        df = DBManager.filter_by_status(status_)
        return Response(df.to_dict(orient="records"))
