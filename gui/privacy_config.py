import json
import os
import shutil
from crypto.security_protocols import AESCipher, generate_secure_random_bytes

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "privacy_config.json")
KEY_PATH = os.path.join(os.path.dirname(__file__), "privacy_config.key")


def default_config():
    return {
        "kill_switch": True,
        "secure_dns": True,
        "custom_dns": "",
        "no_logs": True,
        "multi_hop": False,
        "tor_enabled": False,
        "proxy_rotation": True,
    }


def get_or_create_key():
    try:
        if os.path.exists(KEY_PATH):
            with open(KEY_PATH, "rb") as f:
                return f.read()
        key = generate_secure_random_bytes(32)
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        return key
    except Exception as e:
        raise RuntimeError(f"Erro ao acessar ou criar chave de configuração: {e}")


def save_config(config):
    try:
        key = get_or_create_key()
        aes = AESCipher(key)
        data = json.dumps(config).encode()
        encrypted = aes.encrypt(data)
        with open(CONFIG_PATH + ".enc", "wb") as f:
            f.write(encrypted)
        # Salva também em texto puro para compatibilidade
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar configuração: {e}")


def load_config():
    try:
        key = get_or_create_key()
        aes = AESCipher(key)
        if os.path.exists(CONFIG_PATH + ".enc"):
            with open(CONFIG_PATH + ".enc", "rb") as f:
                encrypted = f.read()
            try:
                data = aes.decrypt(encrypted)
                return json.loads(data.decode())
            except Exception:
                pass
        # Fallback para texto puro
        if not os.path.exists(CONFIG_PATH):
            save_config(default_config())
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar configuração: {e}")


def backup_config():
    if os.path.exists(CONFIG_PATH):
        shutil.copy(CONFIG_PATH, CONFIG_PATH + ".bak")


def reset_config():
    save_config(default_config())


def validate_privacy_config(config):
    errors = []
    if "custom_dns" in config and config["custom_dns"]:
        dns = config["custom_dns"]
        if not (dns.count(".") == 3 or ":" in dns):
            errors.append("DNS customizado inválido.")
    return errors


def export_encrypted_config(export_path):
    key = get_or_create_key()
    aes = AESCipher(key)
    if os.path.exists(CONFIG_PATH + ".enc"):
        with open(CONFIG_PATH + ".enc", "rb") as f:
            encrypted = f.read()
        with open(export_path, "wb") as f:
            f.write(encrypted)
        return True
    return False


def import_encrypted_config(import_path):
    key = get_or_create_key()
    with open(import_path, "rb") as f:
        encrypted = f.read()
    with open(CONFIG_PATH + ".enc", "wb") as f:
        f.write(encrypted)
    # Opcional: tenta decifrar para validar
    aes = AESCipher(key)
    try:
        data = aes.decrypt(encrypted)
        json.loads(data.decode())
        return True
    except Exception:
        return False
