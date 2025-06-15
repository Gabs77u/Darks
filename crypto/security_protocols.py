"""
Módulo de protocolos de segurança e criptografia para tráfego ponta a ponta.
Inclui: AES, TLS/SSL, geração de aleatórios seguros, SSH, SFTP/FTPS, estrutura para IPsec/WPA2/WPA3.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives import keywrap
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PrivateFormat,
    NoEncryption,
)
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
import ssl
import paramiko
import logging
import requests


logging.basicConfig(level=logging.INFO)
LOG_EXTERNAL_URL = os.getenv("LOG_EXTERNAL_URL")


def log_external(msg, level="info"):
    if LOG_EXTERNAL_URL:
        try:
            requests.post(LOG_EXTERNAL_URL, json={"log": msg, "level": level})
        except Exception as e:
            logging.error(f"Falha ao enviar log externo: {e}")


# AES - Criptografia Simétrica
class AESCipher:
    def __init__(self, key: bytes):
        if not isinstance(key, bytes) or len(key) not in (16, 24, 32):
            raise ValueError(
                "Chave AES inválida. Deve ser bytes de 16, 24 ou 32 bytes."
            )
        self.key = key
        self.backend = default_backend()

    def encrypt(self, data: bytes) -> bytes:
        try:
            iv = os.urandom(16)
            cipher = Cipher(
                algorithms.AES(self.key), modes.CBC(iv), backend=self.backend
            )
            encryptor = cipher.encryptor()
            padder = sym_padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
            ct = encryptor.update(padded_data) + encryptor.finalize()
            return iv + ct
        except Exception as e:
            logging.error(f"Erro ao criptografar dados: {e}")
            log_external(f"Erro ao criptografar dados: {e}", level="error")
            raise RuntimeError(f"Erro ao criptografar dados: {e}")

    def decrypt(self, enc: bytes) -> bytes:
        try:
            iv = enc[:16]
            ct = enc[16:]
            cipher = Cipher(
                algorithms.AES(self.key), modes.CBC(iv), backend=self.backend
            )
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ct) + decryptor.finalize()
            unpadder = sym_padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            return data
        except Exception as e:
            logging.error(f"Erro ao descriptografar dados: {e}")
            log_external(f"Erro ao descriptografar dados: {e}", level="error")
            raise RuntimeError(f"Erro ao descriptografar dados: {e}")


# TLS/SSL - Geração de certificado autoassinado
from OpenSSL import crypto


def generate_self_signed_cert(cert_file: str, key_file: str, CN: str = "localhost"):
    try:
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        cert = crypto.X509()
        cert.get_subject().CN = CN
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, "sha256")
        with open(cert_file, "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        with open(key_file, "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
    except Exception as e:
        logging.error(f"Erro ao gerar certificado: {e}")
        log_external(f"Erro ao gerar certificado: {e}", level="error")
        raise RuntimeError(f"Erro ao gerar certificado: {e}")


# Geração de números aleatórios seguros
import secrets


def generate_secure_random_bytes(n: int) -> bytes:
    return secrets.token_bytes(n)


# SSH/SFTP - Conexão básica usando Paramiko
class SSHManager:
    def __init__(self, hostname, username, password=None, key_filename=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            self.hostname,
            username=self.username,
            password=self.password,
            key_filename=self.key_filename,
        )

    def run_command(self, command):
        if not self.client:
            self.connect()
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    def close(self):
        if self.client:
            self.client.close()


# SFTP/FTPS - Estrutura básica
# SFTP via Paramiko já incluso acima
# FTPS pode ser implementado com ftplib
from ftplib import FTP_TLS


def ftps_upload(host, username, password, filepath, destpath):
    ftps = FTP_TLS(host)
    ftps.login(user=username, passwd=password)
    ftps.prot_p()
    with open(filepath, "rb") as f:
        ftps.storbinary(f"STOR {destpath}", f)
    ftps.quit()


# IPsec/WPA2/WPA3 - Estrutura para integração futura
# Normalmente requer integração com o sistema operacional
class IPsecManager:
    def __init__(self):
        pass

    def configure(self):
        pass  # Implementação depende do SO


class WPA2WPA3Manager:
    def __init__(self):
        pass

    def configure(self):
        pass  # Implementação depende do SO


# Exemplo de uso:
# aes = AESCipher(key=os.urandom(32))
# encrypted = aes.encrypt(b'dados')
# decrypted = aes.decrypt(encrypted)
