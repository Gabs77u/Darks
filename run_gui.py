import os
import sys
import shutil
from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


def find_executable_win(exe_name, extra_paths=None):
    # Procura o executável no PATH e em caminhos extras
    path = shutil.which(exe_name)
    if path:
        return path
    if os.name == "nt" and extra_paths:
        for p in extra_paths:
            # Sanitiza o caminho
            if not isinstance(p, str) or not p:
                continue
            exe_path = os.path.join(p, exe_name + ".exe")
            if os.path.isfile(exe_path):
                return exe_path
    return None


def check_external_dependencies():
    missing = []
    extra_paths = [
        r"C:\Program Files\WireGuard",
        r"C:\Users\gabri\Downloads\tor-expert-bundle-windows-x86_64-14.5.3\\tor",
    ]
    # Verifica WireGuard
    if not (find_executable_win("wg", extra_paths)):
        missing.append("WireGuard (wg)")
    # Verifica Tor
    if not (find_executable_win("tor", extra_paths)):
        missing.append("Tor")
    if missing:
        print("Dependências externas ausentes:", ", ".join(missing))
        return False
    return True


def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Erro crítico ao iniciar a aplicação: {e}")
        sys.exit(2)


if __name__ == "__main__":
    if not check_external_dependencies():
        print("Corrija as dependências externas antes de rodar o sistema.")
        sys.exit(1)
    main()
