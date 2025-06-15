import subprocess
from gui.privacy_config import load_config
from crypto.security_protocols import generate_secure_random_bytes


def start_tor():
    import platform
    import shutil
    import os

    config = load_config()
    if not config.get("tor_enabled", False):
        return
    session_token = generate_secure_random_bytes(16).hex()
    # O token pode ser usado para logs ou auditoria segura
    try:
        tor_cmd = "tor"
        if platform.system() == "Windows":
            possible_paths = [
                shutil.which("tor"),
                r"C:\Users\gabri\Downloads\tor-expert-bundle-windows-x86_64-14.5.3\tor\tor.exe",
                r"C:\Program Files\Tor\tor.exe",
            ]
            for path in possible_paths:
                if path and os.path.isfile(path):
                    tor_cmd = path
                    break
        subprocess.Popen([tor_cmd])
    except Exception as e:
        print("Erro ao iniciar Tor:", e)

    # (Opcional) criptografar configs sensíveis do Tor
    # Exemplo: aes = AESCipher(key); dados = aes.encrypt(b'config')
