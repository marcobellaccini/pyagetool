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
        self.assertRaisesRegex(ValueError, ('Cannot decrypt file key.'),
                               X25519._get_key, argl, pubkey, privkey)

    def test__get_key_ok(self):
        """Test _get_key method: good key"""
        exp_file_key = b'\1' * 16
        argl = ['pOCSkrZRwni5dyxWn1-puxPZBrRqtoyd-dwrRAn4ogk',
                'brDpY8ypv2JgXKvNM0uANm92yH_odrZxwqzjE8NDGDw']
        # this is the encoded version of 32 * b'\2'
        privkey = 'AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI'
        # and this is the corresponding public key
        pubkey = 'zo060cy2M-x7cMF4FKXHbs0CloUFDTRHRboFhw5YfVk'
        file_key = X25519._get_key(argl, pubkey, privkey)
        self.assertEqual(exp_file_key, file_key)

    def test__put_key_allzeros(self):
        """Test _put_key method: all-zeros"""
        # this is b'\1' + b'\0'*31 after being encoded
        # took it from libsodium has_small_order() blacklist
        pubkeyb64 = 'AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        eph_secret = b'\1' * 32
        file_key = b'\1' * 16
        self.assertRaisesRegex(ValueError,
                               'Libsodium prevented all-zeros X25519 output.',
                               X25519._put_key, pubkeyb64, eph_secret, file_key)

    def test__put_key_ok(self):
        """Test _put_key method: encrypt key"""
        exp_argl = ['pOCSkrZRwni5dyxWn1-puxPZBrRqtoyd-dwrRAn4ogk',
                    'brDpY8ypv2JgXKvNM0uANm92yH_odrZxwqzjE8NDGDw']
        pubkeyb64 = 'zo060cy2M-x7cMF4FKXHbs0CloUFDTRHRboFhw5YfVk'
        eph_secret = b'\1' * 32
        file_key = b'\1' * 16
        argl = X25519._put_key(pubkeyb64, eph_secret, file_key)
        self.assertEqual(exp_argl, argl)
