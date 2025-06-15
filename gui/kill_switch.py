import os
import platform
import subprocess
from gui.privacy_config import load_config
from crypto.security_protocols import generate_secure_random_bytes


def enable_kill_switch():
    config = load_config()
    if not config.get("kill_switch", True):
        return
    kill_token = generate_secure_random_bytes(8).hex()
    # O token pode ser usado para logs ou auditoria segura
    if platform.system() == "Windows":
        subprocess.call("netsh advfirewall set allprofiles state on", shell=True)
        subprocess.call(
            'netsh advfirewall firewall add rule name="KillSwitch" dir=out action=block remoteip=0.0.0.0/0',
            shell=True,
        )
    else:
        subprocess.call("iptables -I OUTPUT ! -o wg0 -j DROP", shell=True)


def disable_kill_switch():
    if platform.system() == "Windows":
        subprocess.call(
            'netsh advfirewall firewall delete rule name="KillSwitch"', shell=True
        )
    else:
        subprocess.call("iptables -D OUTPUT ! -o wg0 -j DROP", shell=True)
