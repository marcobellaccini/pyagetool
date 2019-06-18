#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `X25519`."""


import unittest
import base64

from pyagetool import X25519

class TestX25519(unittest.TestCase):
    """Tests for the `X25519` class."""

    # def test__get_key(self):
    #     """Test _get_key method: get key"""
    #     argl = ['CJM36AHmTbdHSuOQL-NESqyVQE75f2e610iRdLPEN20',
    #             'C3ZAeY64NXS4QFrksLm3EGz-uPRyI0eQsWw7LWbbYig']
    #     privkey = 'RQvvHYA29yZk8Lelpiz8lW7QdlxkE4djb1NOjLgeUFg'
    #     x25519 = X25519.X25519()
    #     key = x25519._get_key(argl, privkey)
    #     self.assertEqual('12345', key)
