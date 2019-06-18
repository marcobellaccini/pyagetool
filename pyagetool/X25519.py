# -*- coding: utf-8 -*-
from . import encoding

"""X25519 module."""

class X25519:
    """X25519 class"""

    def _get_key(self, argl, privkey):
        """This method decrypts file key from X25519 line arguments.

        Args:
            argl: X25519 line argument list.

            privkey: base64url-encode X25519 private key.

        Returns:
            File key.

        """
        # decode ephemeral share
        eph_share = encoding.decode(argl[0])
        # decode encrypted key
        enc_key = encoding.decode(argl[1])
