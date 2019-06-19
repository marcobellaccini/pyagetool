#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `X25519`."""


import unittest
import base64

from pyagetool import X25519

class TestX25519(unittest.TestCase):
    """Tests for the `X25519` class."""

    def test__get_key_badkey(self):
        """Test _get_key method: cannot decrypt key"""
        argl = ['DJM36AHmTbdHSuOQL-NESqyVQE75f2e610iRdLPEN21',
                'E3ZAeY64NXS4QFrksLm3EGz-uPRyI0eQsWw7LWbbYih']
        pubkey = '38W5ph53zfPGOzEOH-fMojQ4jUY7VLEmtmozREqnw4I'
        privkey = 'TQvvHYA29yZk8Lelpiz8lW7QdlxkE4djb1NOjLgeUFg'
        x25519 = X25519.X25519()
        # key = x25519._get_key(argl, pubkey, privkey)
        self.assertRaisesRegex(ValueError, ('Cannot decrypt file key.'),
                               x25519._get_key, argl, pubkey, privkey)
        # self.assertEqual('12345', key)

    def test__get_key_ok(self):
        """Test _get_key method: good key"""
        argl = ['CJM36AHmTbdHSuOQL-NESqyVQE75f2e610iRdLPEN20',
                'C3ZAeY64NXS4QFrksLm3EGz-uPRyI0eQsWw7LWbbYig']
        pubkey = '98W5ph53zfPGOzEOH-fMojQ4jUY7VLEmtmozREqnw4I'
        privkey = 'RQvvHYA29yZk8Lelpiz8lW7QdlxkE4djb1NOjLgeUFg'
        x25519 = X25519.X25519()
        key = x25519._get_key(argl, pubkey, privkey)
        self.assertEqual('12345', key)
