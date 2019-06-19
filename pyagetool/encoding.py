# -*- coding: utf-8 -*-
import base64

"""encoding module."""


def _encode(data):
    """This method encodes bytes in Base 64 Encoding with URL and
    Filename Safe Alphabet, WITHOUT padding.

    Args:
        data: input data.

    Returns:
        Encoded data string.

    """
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip('=')


def _decode(encdata):
    """This method decodes bytes from Base 64 Encoding with URL and
    Filename Safe Alphabet, WITHOUT padding.

    Args:
        data: encoded input data (NO PADDING).

    Returns:
        Decoded data.

    """
    # add missing padding
    missing_padding = 4 - len(encdata) % 4
    return base64.urlsafe_b64decode((encdata +
                                     ('=' * missing_padding)).encode("utf-8"))
