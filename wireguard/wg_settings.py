import json
import os

WG_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "wg_settings.json")


def default_wg_settings():
    return {
        "interface": "wg0",
        "private_key": "",
        "address": "",
        "dns": "",
        "peer_public_key": "",
        "endpoint": "",
        "allowed_ips": "0.0.0.0/0",
        "persistent_keepalive": 25,
    }


def load_wg_settings():
    if not os.path.exists(WG_CONFIG_PATH):
        save_wg_settings(default_wg_settings())
    try:
        with open(WG_CONFIG_PATH, "r") as f:
            data = json.load(f)
        errors = validate_wg_settings(data)
        if errors:
            raise ValueError(f"Configuração inválida: {errors}")
        return data
    except (json.JSONDecodeError, ValueError) as e:
        # Log do erro pode ser adicionado aqui
        save_wg_settings(default_wg_settings())
        return default_wg_settings()
    except Exception as e:
        # Log do erro pode ser adicionado aqui
        raise RuntimeError(f"Erro ao carregar configurações WireGuard: {e}")


def save_wg_settings(settings):
    # Sanitização básica: remove chaves desconhecidas
    valid_keys = set(default_wg_settings().keys())
    sanitized = {k: v for k, v in settings.items() if k in valid_keys}
    # Validação ANTES de salvar
    errors = validate_wg_settings(sanitized)
    if errors:
        raise ValueError(f"Configurações inválidas: {errors}")
    try:
        with open(WG_CONFIG_PATH, "w") as f:
            json.dump(sanitized, f, indent=4)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar configurações WireGuard: {e}")


def validate_wg_settings(settings):
    errors = []
    if not settings.get("private_key") or len(settings["private_key"]) < 32:
        errors.append("Chave privada inválida ou ausente.")
    if not settings.get("address") or "/" not in settings["address"]:
        errors.append("Endereço inválido (ex: 10.0.0.2/24)")
    if not settings.get("peer_public_key") or len(settings["peer_public_key"]) < 32:
        errors.append("Chave pública do peer inválida ou ausente.")
    if not settings.get("endpoint"):
        errors.append("Endpoint do peer é obrigatório.")
    if not settings.get("allowed_ips"):
        errors.append("Allowed IPs é obrigatório.")
    if settings.get("dns") and not (
        settings["dns"].count(".") == 3 or ":" in settings["dns"]
    ):
        errors.append("DNS inválido.")
    return errors
