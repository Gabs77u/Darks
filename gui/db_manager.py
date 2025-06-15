import pandas as pd
import os
from gui.privacy_config import load_config
from crypto.security_protocols import AESCipher, generate_secure_random_bytes
import logging
import requests
import traceback
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "vpn_db.csv")
DB_KEY_PATH = os.path.join(os.path.dirname(__file__), "db.key")

LOG_EXTERNAL_URL = os.getenv("LOG_EXTERNAL_URL")
LOG_USER = os.getenv("LOG_USER", "sistema")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def log_external(msg, level="info", context=None):
    if LOG_EXTERNAL_URL:
        payload = {
            "log": msg,
            "level": level,
            "user": LOG_USER,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        try:
            requests.post(LOG_EXTERNAL_URL, json=payload, timeout=2)
        except Exception as e:
            logging.error(f"Falha ao enviar log externo: {e}")


def handle_exception(e, context=None):
    tb = traceback.format_exc()
    msg = f"Erro: {e}\nTraceback: {tb}"
    logging.error(msg)
    log_external(msg, level="error", context=context)
    print("Ocorreu um erro inesperado. Tente novamente ou contate o suporte.")


def get_or_create_db_key():
    if os.path.exists(DB_KEY_PATH):
        try:
            with open(DB_KEY_PATH, "rb") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Erro ao ler chave do banco: {e}")
    key = generate_secure_random_bytes(32)
    try:
        with open(DB_KEY_PATH, "wb") as f:
            f.write(key)
    except Exception as e:
        raise RuntimeError(f"Erro ao criar chave do banco: {e}")
    return key


class DBManager:
    @staticmethod
    def create_and_populate_db():
        config = load_config()
        if config.get("no_logs", True):
            return pd.DataFrame()
        data = {
            "id": [1, 2, 3],
            "usuario": ["admin", "user1", "user2"],
            "vpn_status": ["conectado", "desconectado", "conectado"],
            "proxy_host": ["127.0.0.1", "127.0.0.1", "127.0.0.1"],
            "proxy_port": [50000, 50001, 50002],
            "tipo_proxy": ["SOCKS5", "SOCKS5", "SOCKS5"],
        }
        df = pd.DataFrame(data)
        try:
            df.to_csv(DB_PATH, index=False)
        except Exception as e:
            raise RuntimeError(f"Erro ao criar banco: {e}")
        return df

    @staticmethod
    def load_db():
        config = load_config()
        if config.get("no_logs", True):
            return pd.DataFrame()
        if not os.path.exists(DB_PATH):
            return DBManager.create_and_populate_db()
        try:
            return pd.read_csv(DB_PATH)
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar banco: {e}")

    @staticmethod
    def update_status(user_id, status):
        config = load_config()
        if config.get("no_logs", True):
            return pd.DataFrame()
        df = DBManager.load_db()
        df.loc[df["id"] == user_id, "vpn_status"] = status
        try:
            df.to_csv(DB_PATH, index=False)
        except Exception as e:
            raise RuntimeError(f"Erro ao atualizar status: {e}")
        return df

    @staticmethod
    def add_user(usuario, status, host, port, tipo):
        config = load_config()
        if config.get("no_logs", True):
            return pd.DataFrame()
        df = DBManager.load_db()
        new_id = int(df["id"].max()) + 1 if not df.empty else 1
        new_row = {
            "id": new_id,
            "usuario": usuario,
            "vpn_status": status,
            "proxy_host": host,
            "proxy_port": port,
            "tipo_proxy": tipo,
        }
        errors = DBManager.validate_user(new_row)
        if errors:
            raise ValueError(f"Dados inválidos: {errors}")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        try:
            df.to_csv(DB_PATH, index=False)
        except Exception as e:
            raise RuntimeError(f"Erro ao adicionar usuário: {e}")
        return df

    @staticmethod
    def remove_user(user_id):
        config = load_config()
        if config.get("no_logs", True):
            return pd.DataFrame()
        df = DBManager.load_db()
        df = df[df["id"] != user_id]
        try:
            df.to_csv(DB_PATH, index=False)
        except Exception as e:
            raise RuntimeError(f"Erro ao remover usuário: {e}")
        return df

    @staticmethod
    def edit_user(user_id, usuario=None, status=None, host=None, port=None, tipo=None):
        config = load_config()
        if config.get("no_logs", True):
            return pd.DataFrame()
        df = DBManager.load_db()
        if not (df["id"] == user_id).any():
            # Usuário não existe, retorna DataFrame inalterado
            return df
        if usuario:
            df.loc[df["id"] == user_id, "usuario"] = usuario
        if status:
            df.loc[df["id"] == user_id, "vpn_status"] = status
        if host:
            df.loc[df["id"] == user_id, "proxy_host"] = host
        if port:
            df.loc[df["id"] == user_id, "proxy_port"] = port
        if tipo:
            df.loc[df["id"] == user_id, "tipo_proxy"] = tipo
        # Validação após edição
        user = df[df["id"] == user_id].iloc[0].to_dict()
        errors = DBManager.validate_user(user)
        if errors:
            raise ValueError(f"Dados inválidos: {errors}")
        try:
            df.to_csv(DB_PATH, index=False)
        except Exception as e:
            raise RuntimeError(f"Erro ao editar usuário: {e}")
        return df

    @staticmethod
    def search_users(query):
        config = load_config()
        if config.get("no_logs", True):
            return pd.DataFrame()
        df = DBManager.load_db()
        mask = df["usuario"].str.contains(query, case=False, na=False)
        return df[mask]

    @staticmethod
    def filter_by_status(status):
        config = load_config()
        if config.get("no_logs", True):
            return pd.DataFrame()
        df = DBManager.load_db()
        return df[df["vpn_status"] == status]

    @staticmethod
    def get_user(user_id):
        config = load_config()
        if config.get("no_logs", True):
            return None
        df = DBManager.load_db()
        user = df[df["id"] == user_id]
        return user.iloc[0] if not user.empty else None

    @staticmethod
    def validate_user(user):
        errors = []
        if (
            not user.get("usuario")
            or not isinstance(user["usuario"], str)
            or len(user["usuario"]) < 3
        ):
            errors.append("Nome de usuário inválido (mínimo 3 caracteres).")
        if user.get("vpn_status") not in ["conectado", "desconectado"]:
            errors.append("Status de VPN inválido.")
        if not user.get("proxy_host") or not isinstance(user["proxy_host"], str):
            errors.append("Host do proxy inválido.")
        try:
            port = int(user.get("proxy_port", 0))
            if not (20000 <= port <= 60000):
                errors.append(
                    "Porta do proxy fora do intervalo permitido (20000-60000)."
                )
        except Exception:
            errors.append("Porta do proxy inválida.")
        if user.get("tipo_proxy") not in ["SOCKS5", "HTTP"]:
            errors.append("Tipo de proxy inválido (apenas SOCKS5 ou HTTP suportados).")
        return errors

    @staticmethod
    def save_encrypted_db(df):
        key = get_or_create_db_key()
        aes = AESCipher(key)
        data = df.to_csv(index=False).encode()
        encrypted = aes.encrypt(data)
        try:
            with open(DB_PATH + ".enc", "wb") as f:
                f.write(encrypted)
        except Exception as e:
            raise RuntimeError(f"Erro ao salvar banco criptografado: {e}")

    @staticmethod
    def load_encrypted_db():
        key = get_or_create_db_key()
        aes = AESCipher(key)
        if not os.path.exists(DB_PATH + ".enc"):
            return pd.DataFrame()
        try:
            with open(DB_PATH + ".enc", "rb") as f:
                encrypted = f.read()
            data = aes.decrypt(encrypted)
            from io import StringIO

            return pd.read_csv(StringIO(data.decode()))
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar banco criptografado: {e}")

    @staticmethod
    def export_encrypted_db(export_path):
        key = get_or_create_db_key()
        aes = AESCipher(key)
        if os.path.exists(DB_PATH + ".enc"):
            try:
                with open(DB_PATH + ".enc", "rb") as f:
                    encrypted = f.read()
                with open(export_path, "wb") as f:
                    f.write(encrypted)
                return True
            except Exception as e:
                raise RuntimeError(f"Erro ao exportar banco criptografado: {e}")
        return False

    @staticmethod
    def import_encrypted_db(import_path):
        key = get_or_create_db_key()
        try:
            with open(import_path, "rb") as f:
                encrypted = f.read()
            with open(DB_PATH + ".enc", "wb") as f:
                f.write(encrypted)
            # Opcional: tenta decifrar para validar
            aes = AESCipher(key)
            from io import StringIO

            data = aes.decrypt(encrypted)
            pd.read_csv(StringIO(data.decode()))
            return True
        except Exception as e:
            return False
