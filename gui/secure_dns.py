import subprocess
import platform
from gui.privacy_config import load_config
from crypto.security_protocols import generate_secure_random_bytes


def set_secure_dns():
    config = load_config()
    if not config.get("secure_dns", True):
        return
    dns = config.get("custom_dns") or "1.1.1.1"
    dns_session_id = generate_secure_random_bytes(8).hex()
    # O identificador pode ser usado para logs ou auditoria segura
    if platform.system() == "Windows":
        subprocess.call(
            f'netsh interface ip set dns name="Ethernet" static {dns}', shell=True
        )
    else:
        subprocess.call(f"resolvectl dns eth0 {dns}", shell=True)
