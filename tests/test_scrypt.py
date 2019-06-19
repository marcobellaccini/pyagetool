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
        argl = ['bBjlhJVYZeE4aqUdmtRHfw32768',
                'ZV_AhotwSGqaPCU43cepl4WYUouAa17a3xpu4G2yi5k']
        password = 'test'
        self.assertRaisesRegex(ValueError, ('Cannot decrypt file key.'),
                               scrypt._get_key, argl, password)

    def test__get_key_ok(self):
        """Test _get_key method: good key"""
        argl = ['bBjlhJVYZeE4aqUdmtRHfw32768',
                'ZV_AhotwSGqaPCU43cepl4WYUouAa17a3xpu4G2yi5k']
        password = 'test'
        key = scrypt._get_key(argl, password)
        self.assertEqual('12345', key)
