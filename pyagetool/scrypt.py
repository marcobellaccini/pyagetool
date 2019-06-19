# -*- coding: utf-8 -*-
from . import encoding
from . import symencrypt

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

"""scrypt module."""


def _get_key(self, argl, password):
    """This method decrypts file key from scrypt line arguments.

    Args:
        argl: scrypt line argument list.

        password: password.

    Returns:
        File key.

    """

    # decode salt
    salt = encoding._decode(argl[0])
    # get cost
    n = argl[1]
    # decode encrypted file key
    enc_file_key = encoding._decode(argl[2])
    # compute key encryption key
    kdf = Scrypt(
            salt=salt,
            length=32,
            n=n,
            r=8,
            p=1,
            backend=default_backend()
            )
    kek = kdf.derive(password.encode("utf-8"))
    # decrypt and return file key
    return symencrypt._decrypt_key(kek, enc_file_key)
