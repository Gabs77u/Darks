import subprocess
import sys
import os

# Script para instalar o WireGuard no Windows


def is_wireguard_installed():
    try:
        subprocess.check_output(["wg", "--version"])
        return True
    except Exception:
        return False


def install_wireguard():
    print("Instalando WireGuard...")
    url = "https://download.wireguard.com/windows-client/wireguard-installer.exe"
    installer_path = os.path.join(os.getcwd(), "wireguard-installer.exe")
    import requests

    r = requests.get(url)
    with open(installer_path, "wb") as f:
        f.write(r.content)
    os.startfile(installer_path)
    print("Execute o instalador e siga as instruções.")


if __name__ == "__main__":
    if is_wireguard_installed():
        print("WireGuard já está instalado.")
    else:
        install_wireguard()
