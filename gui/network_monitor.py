import psutil
import time
from crypto.security_protocols import generate_secure_random_bytes


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
        print(get_network_stats())
        time.sleep(2)
