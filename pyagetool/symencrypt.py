# -*- coding: utf-8 -*-
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.exceptions import InvalidTag

"""symencrypt module."""


def _decrypt_key(kek, enc_key):
    """This method decrypts ChaCha20-Poly1305-encrypted key.

    It raises ValueError if something goes wrong.

    Args:
        kek: key encryption key.

        enc_key: encrypted key.

    Returns:
        Decrypted key.

    """
    chacha = ChaCha20Poly1305(kek)
    nonce = b'\0' * 12
    try:
        key = chacha.decrypt(nonce, enc_key, None)
    except InvalidTag:
        raise ValueError('Cannot decrypt file key.')

    return key


def _encrypt_key(kek, key):
    """This method encrypts key using ChaCha20-Poly1305.

    Args:
        kek: key encryption key.

        key: plaintext key.

    Returns:
        Encrypted key.

    """
    chacha = ChaCha20Poly1305(kek)
    nonce = b'\0' * 12
    enc_key = chacha.encrypt(nonce, key, None)

    return enc_key
