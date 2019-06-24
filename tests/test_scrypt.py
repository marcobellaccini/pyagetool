#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `scrypt`."""


import unittest
import base64

from pyagetool import scrypt

class Testscrypt(unittest.TestCase):
    """Tests for the `scrypt` class."""

    def test__get_key_badpass(self):
        """Test _get_key method: cannot decrypt key"""
        argl = ['AQEBAQEBAQEBAQEBAQEBAQ',
                '32768',
                'yiFepxeu4fBPvGzYzeYKcCdyu8gyysPU8S5fBF-0z3s']
        password = 'testbad'
        self.assertRaisesRegex(ValueError, ('Cannot decrypt file key.'),
                               scrypt._get_key, argl, password)

    def test__get_key_ok(self):
        """Test _get_key method: good key"""
        argl = ['AQEBAQEBAQEBAQEBAQEBAQ',
                '32768',
                'yiFepxeu4fBPvGzYzeYKcCdyu8gyysPU8S5fBF-0z3s']
        password = 'test'
        exp_file_key = b'\1' * 16
        key = scrypt._get_key(argl, password)
        self.assertEqual(exp_file_key, key)
    
    def test__put_key_ok(self):
        """Test _put_key method: encrypt key"""
        exp_argl = ['AQEBAQEBAQEBAQEBAQEBAQ',
                '32768',
                'yiFepxeu4fBPvGzYzeYKcCdyu8gyysPU8S5fBF-0z3s']
        password = 'test'
        salt = b'\1' * 16
        file_key = b'\1' * 16
        argl = scrypt._put_key(password, 32768, salt, file_key)
        self.assertEqual(exp_argl, argl)
