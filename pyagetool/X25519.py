# -*- coding: utf-8 -*-
from . import encoding
from . import symencrypt

from nacl.exceptions import RuntimeError as NaclRuntimeError
from nacl.bindings import crypto_scalarmult_base, crypto_scalarmult
# here we use pyca/cryptography because libsodium seems to miss
# HKDF-SHA256 (it's Blake2-only)
# https://github.com/jedisct1/libsodium/issues/367
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

"""X25519 module."""


def _get_key(argl, pubkeyb64, privkeyb64):
    """This method decrypts file key from X25519 line arguments.

    Args:
        argl: X25519 line argument list.

        pubkeyb64: base64url-encode X25519 public key.

        privkeyb64: base64url-encode X25519 private key.

    Returns:
        File key.

    It raises ValueError whether some issue is detected.

    """
    # decode ephemeral public key
    eph_pub_key = encoding._decode(argl[0])
    # decode encrypted file key
    enc_file_key = encoding._decode(argl[1])
    # decode static public key
    static_pub_key = encoding._decode(pubkeyb64)
    # decode static private key
    priv_key = encoding._decode(privkeyb64)
    # compute shared key
    try:
        shared_key = crypto_scalarmult(priv_key, eph_pub_key)
    except NaclRuntimeError:
        raise ValueError('Libsodium prevented all-zeros X25519 output.')
    # compute key encryption key
    kek = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=eph_pub_key + static_pub_key,
        info=b'age-tool.com X25519',
        backend=default_backend()
        ).derive(shared_key)
    # decrypt and return file key
    return symencrypt._decrypt_key(kek, enc_file_key)


def _put_key(pubkeyb64, eph_secret, file_key):
    """This method encrypts file key using X25519 and returns X25519 line
    argument list.

    Args:
        pubkeyb64: target base64url-encode X25519 public key.

        eph_secret: 32-bytes ephemeral secret.

        file_key: file key to encrypt using X25519.

    Returns:
        X25519 line argument list.

    It raises ValueError whether some issue is detected.

    """
    # compute ephemeral public key
    try:
        eph_pub_key = crypto_scalarmult_base(eph_secret)
    except NaclRuntimeError:
        raise ValueError('Libsodium prevented all-zeros X25519 output.')
    # decode static public key
    static_pub_key = encoding._decode(pubkeyb64)
    # compute shared key
    try:
        shared_key = crypto_scalarmult(eph_secret, static_pub_key)
    except NaclRuntimeError:
        raise ValueError('Libsodium prevented all-zeros X25519 output.')
    # compute key encryption key
    kek = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=eph_pub_key + static_pub_key,
        info=b'age-tool.com X25519',
        backend=default_backend()
        ).derive(shared_key)
    # encrypt file key
    enc_file_key = symencrypt._encrypt_key(kek, file_key)
    # build and return X25519 line argument list
    argl = [encoding._encode(eph_pub_key),
            encoding._encode(enc_file_key)]
    return argl
