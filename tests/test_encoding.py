#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `encoding`."""


import unittest

from pyagetool import encoding

class TestEncoding(unittest.TestCase):
    """Tests for the encoding and decoding functions."""

    def test__encode_pad2(self):
        """Test _encode function: 2 chars pad"""
        data = b'a'
        encdata = encoding._encode(data)
        self.assertEqual('YQ', encdata)

    def test__encode_pad1(self):
        """Test _encode function: 1 char pad"""
        data = b'ab'
        encdata = encoding._encode(data)
        self.assertEqual('YWI', encdata)

    def test__encode_pad0(self):
        """Test _encode function: 0 char pad"""
        data = b'abc'
        encdata = encoding._encode(data)
        self.assertEqual('YWJj', encdata)

    def test__decode_pad2(self):
        """Test _decode function: 2 chars pad"""
        encdata = 'YQ'
        data = encoding._decode(encdata)
        self.assertEqual(b'a', data)

    def test__decode_pad1(self):
        """Test _decode function: 1 char pad"""
        encdata = 'YWI'
        data = encoding._decode(encdata)
        self.assertEqual(b'ab', data)

    def test__decode_pad0(self):
        """Test _decode function: 0 char pad"""
        encdata = 'YWJj'
        data = encoding._decode(encdata)
        self.assertEqual(b'abc', data)
