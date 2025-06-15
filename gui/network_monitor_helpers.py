import psutil
import socket
import os
from collections import deque
import time
from crypto.security_protocols import generate_secure_random_bytes
import logging
import requests
import traceback
from datetime import datetime


def get_network_stats():
    stats = {}
    session_id = generate_secure_random_bytes(8).hex()
    for name, addrs in psutil.net_if_addrs().items():
        stats[name] = {
            "addresses": [a.address for a in addrs if a.family == socket.AF_INET],
            "isup": psutil.net_if_stats()[name].isup,
            "speed": psutil.net_if_stats()[name].speed,
            "bytes_sent": psutil.net_io_counters(pernic=True)[name].bytes_sent,
            "bytes_recv": psutil.net_io_counters(pernic=True)[name].bytes_recv,
            "session_id": session_id,
        }
    return stats


traffic_history = {
    "time": deque(maxlen=60),
    "sent": deque(maxlen=60),
    "recv": deque(maxlen=60),
}
_last_bytes = None


def get_connections(proto_filter=None, only_vpn=False, only_tor=False):
    conns = []
    for c in psutil.net_connections(kind="inet"):
        laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
        raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""
        proc = None
        try:
            if c.pid:
                proc = psutil.Process(c.pid)
        except Exception:
            pass
        proto = "TCP" if c.type == socket.SOCK_STREAM else "UDP"
        if proto_filter and proto != proto_filter:
            continue
        if only_vpn and not (
            laddr.startswith("10.")
            or laddr.startswith("172.")
            or laddr.startswith("192.168.")
        ):
            continue
        if only_tor and not (proc and "tor" in proc.name().lower()):
            continue
        conns.append(
            {
                "type": proto,
                "family": c.family,
                "status": c.status,
                "laddr": laddr,
                "raddr": raddr,
                "pid": c.pid,
                "proc": proc.name() if proc else "",
            }
        )
    return conns


def update_traffic_history():
    global _last_bytes
    stats = psutil.net_io_counters()
    now = time.time()
    if _last_bytes is None:
        _last_bytes = (stats.bytes_sent, stats.bytes_recv)
    sent = stats.bytes_sent - _last_bytes[0]
    recv = stats.bytes_recv - _last_bytes[1]
    _last_bytes = (stats.bytes_sent, stats.bytes_recv)
    traffic_history["time"].append(now)
    traffic_history["sent"].append(max(sent, 0))
    traffic_history["recv"].append(max(recv, 0))
    return (
        list(traffic_history["time"]),
        list(traffic_history["sent"]),
        list(traffic_history["recv"]),
    )


def get_vpn_status():
    # Simples: verifica se interface wg* ou tun* está ativa
    stats = psutil.net_if_stats()
    for iface in stats:
        if (iface.startswith("wg") or iface.startswith("tun")) and stats[iface].isup:
            return True, iface
    return False, None


def get_tor_status():
    # Verifica se processo tor está rodando
    for p in psutil.process_iter(["name"]):
        if "tor" in p.info["name"].lower():
            return True
    return False


def get_proxy_status():
    # Simples: verifica se processo python com proxy está rodando
    for p in psutil.process_iter(["name", "cmdline"]):
        cmdline = p.info.get("cmdline")
        if not isinstance(cmdline, list):
            cmdline = []
        if "proxy" in " ".join(cmdline).lower():
            return True
    return False


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
