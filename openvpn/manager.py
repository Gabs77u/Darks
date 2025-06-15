import subprocess
import os
from .settings import load_ovpn_settings
from crypto.security_protocols import generate_self_signed_cert


class OpenVPNManager:
    @staticmethod
    def start_tunnel(config_path=None):
        settings = load_ovpn_settings()
        config_path = config_path or settings.get("config_path", "openvpn_default.ovpn")
        if not os.path.exists(config_path):
            return False, "Arquivo de configuração OpenVPN não encontrado."
        args = ["openvpn", "--config", config_path]
        userpass_path = None
        if settings.get("auth_user_pass", False):
            userpass_path = os.path.join(os.path.dirname(config_path), "userpass.txt")
            try:
                with open(userpass_path, "w") as f:
                    f.write(
                        f"{settings.get('username','')}\n{settings.get('password','')}"
                    )
                args += ["--auth-user-pass", userpass_path]
            except Exception as e:
                return False, f"Erro ao criar arquivo de autenticação: {e}"
        try:
            subprocess.Popen(args)
            return True, "OpenVPN iniciado com sucesso."
        except Exception as e:
            return False, f"Erro ao iniciar OpenVPN: {e}"
        finally:
            if userpass_path and os.path.exists(userpass_path):
                try:
                    os.remove(userpass_path)
                except Exception:
                    pass

    @staticmethod
    def stop_tunnel():
        # Tenta finalizar todos os processos openvpn
        try:
            if os.name == "nt":
                subprocess.call("taskkill /IM openvpn.exe /F", shell=True)
            else:
                subprocess.call("pkill openvpn", shell=True)
            return True, "OpenVPN finalizado."
        except Exception as e:
            return False, f"Erro ao finalizar OpenVPN: {e}"

    @staticmethod
    def ensure_tls_cert(cert_path, key_path):
        """Gera certificado TLS/SSL autoassinado se não existir."""
        if not (os.path.exists(cert_path) and os.path.exists(key_path)):
            generate_self_signed_cert(cert_path, key_path)
