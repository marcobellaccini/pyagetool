# -*- coding: utf-8 -*-
from . import encoding
from . import symencrypt

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

"""X25519 module."""


def _get_key(argl, pubkeyb64, privkeyb64):
    """This method decrypts file key from X25519 line arguments.

    Args:
        argl: X25519 line argument list.

        pubkeyb64: base64url-encode X25519 public key.

        privkeyb64: base64url-encode X25519 private key.

    Returns:
        File key.

    """
    # decode peer public key
    peer_pub_key = encoding._decode(argl[0])
    # decode encrypted file key
    enc_file_key = encoding._decode(argl[1])
    # decode public key
    pub_key = encoding._decode(pubkeyb64)
    # decode private key
    priv_key = encoding._decode(privkeyb64)

    # load private key
    ld_priv_key = x25519.X25519PrivateKey.from_private_bytes(priv_key)
    # load peer public key
    ld_pub_key = x25519.X25519PublicKey.from_public_bytes(peer_pub_key)
    # compute shared key
    shared_key = ld_priv_key.exchange(ld_pub_key)
    # compute key encryption key
    kek = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=peer_pub_key + pub_key,
        info=b'age-tool.com X25519',
        backend=default_backend()
        ).derive(shared_key)
    # decrypt and return file key
    return symencrypt._decrypt_key(kek, enc_file_key)
