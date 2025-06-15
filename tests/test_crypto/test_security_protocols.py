import pytest
from crypto.security_protocols import *


def test_dummy_crypto():
    # Adapte para funções reais do módulo
    assert True


def test_aes_cipher_wrong_decrypt():
    key1 = generate_secure_random_bytes(32)
    key2 = generate_secure_random_bytes(32)
    cipher1 = AESCipher(key1)
    cipher2 = AESCipher(key2)
    data = b"test"
    enc = cipher1.encrypt(data)
    with pytest.raises(Exception):
        cipher2.decrypt(enc)


def test_generate_self_signed_cert_invalid(monkeypatch):
    monkeypatch.setattr(
        "OpenSSL.crypto.PKey.generate_key",
        lambda self, t, s: (_ for _ in ()).throw(Exception("fail")),
    )
    with pytest.raises(Exception):
        generate_self_signed_cert("cert", "key")


def test_aes_cipher_decrypt_corrupted():
    key = generate_secure_random_bytes(32)
    cipher = AESCipher(key)
    with pytest.raises(Exception):
        cipher.decrypt(b"corrompido")


def test_generate_secure_random_bytes_zero():
    bts = generate_secure_random_bytes(0)
    assert bts == b""


def test_generate_secure_random_bytes_large():
    bts = generate_secure_random_bytes(1024)
    assert len(bts) == 1024
