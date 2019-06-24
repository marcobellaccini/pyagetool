# -*- coding: utf-8 -*-
from . import encoding
from . import symencrypt

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

"""scrypt module."""


def _get_key(argl, password):
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
    try:
        n = int(argl[1])
    except ValueError:
        raise ValueError('Invalid scrypt cost')
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


def _put_key(password, n, salt, file_key):
    """This method encrypts file key and returns scrypt line arguments.

    Args:
        password: password.

        n: scrypt cost.

        salt: 16-bytes random salt.

        file_key: file key.

    Returns:
        scrypt line argument list.

    """

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
    # encrypt file key
    enc_file_key = symencrypt._encrypt_key(kek, file_key)
    # build and return argument list
    argl = [encoding._encode(salt),
            str(n),
            encoding._encode(enc_file_key)]
    return argl
