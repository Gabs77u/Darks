import json
import os

OVPN_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "ovpn_settings.json")


def default_ovpn_settings():
    return {
        "config_path": "openvpn_default.ovpn",
        "username": "",
        "password": "",
        "auth_user_pass": False,
    }


def advanced_ovpn_settings():
    return {
        "proto": "udp",
        "remote": "",
        "port": 1194,
        "cipher": "AES-256-CBC",
        "auth": "SHA256",
        "comp_lzo": False,
        "redirect_gateway": True,
        "tls_auth": "",
        "ca": "",
        "cert": "",
        "key": "",
    }


PRESETS = {
    "OpenVPN Default": {
        "proto": "udp",
        "port": 1194,
        "cipher": "AES-256-CBC",
        "auth": "SHA256",
        "comp_lzo": False,
        "redirect_gateway": True,
    },
    "NordVPN": {
        "proto": "udp",
        "port": 1194,
        "cipher": "AES-256-CBC",
        "auth": "SHA512",
        "comp_lzo": False,
        "redirect_gateway": True,
    },
    "ExpressVPN": {
        "proto": "udp",
        "port": 1195,
        "cipher": "AES-256-CBC",
        "auth": "SHA256",
        "comp_lzo": False,
        "redirect_gateway": True,
    },
    "Surfshark": {
        "proto": "udp",
        "port": 1194,
        "cipher": "AES-256-GCM",
        "auth": "SHA512",
        "comp_lzo": False,
        "redirect_gateway": True,
    },
}


def get_presets():
    return PRESETS


def load_ovpn_settings():
    try:
        if not os.path.exists(OVPN_CONFIG_PATH):
            base = default_ovpn_settings()
            base.update(advanced_ovpn_settings())
            save_ovpn_settings(base)
        with open(OVPN_CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar configurações OpenVPN: {e}")


def save_ovpn_settings(settings):
    adv = advanced_ovpn_settings()
    for k, v in adv.items():
        if k not in settings:
            settings[k] = v
    try:
        with open(OVPN_CONFIG_PATH, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar configurações OpenVPN: {e}")


def validate_ovpn_settings(settings):
    errors = []
    if not settings.get("config_path") or not settings["config_path"].endswith(".ovpn"):
        errors.append("Arquivo de configuração deve ser .ovpn")
    if settings.get("port") and (
        not isinstance(settings["port"], int) or not (1 <= settings["port"] <= 65535)
    ):
        errors.append("Porta inválida (1-65535)")
    if settings.get("proto") not in ["udp", "tcp"]:
        errors.append("Protocolo deve ser udp ou tcp")
    if settings.get("cipher") and not settings["cipher"].startswith("AES-"):
        errors.append("Cipher recomendada: AES-*")
    if settings.get("auth") and not settings["auth"].startswith("SHA"):
        errors.append("Auth recomendada: SHA*")
    # Campos obrigatórios para autenticação
    if settings.get("auth_user_pass"):
        if not settings.get("username") or not settings.get("password"):
            errors.append("Usuário e senha obrigatórios para autenticação USER/PASS")
    return errors
