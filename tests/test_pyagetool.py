#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyagetool` package."""


import unittest

from pyagetool import pyagetool


class TestPyagetool(unittest.TestCase):
    """Tests for `pyagetool` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_parse_header_notage(self):
        """Test parse_header method: not an age file"""
        age = pyagetool.Age()
        self.assertRaisesRegex(ValueError, ('Target file is not an '
                                            'age-tool file\.'),
                               age.parse_header, 'tests/fixtures/notage.age')

    def test_parse_header_unsuppo_form_ver(self):
        """Test parse_header method: unsupported format version"""
        age = pyagetool.Age()
        self.assertRaisesRegex(ValueError, ('Unsupported age-tool '
                                            'format version.'),
                               age.parse_header,
                               'tests/fixtures/unsuppformver.age')

    def test_parse_header_no_header_hmac(self):
        """Test parse_header method: missing header HMAC"""
        age = pyagetool.Age()
        self.assertRaisesRegex(ValueError, ('Missing header HMAC.'),
                               age.parse_header,
                               'tests/fixtures/noheadhmac.age')

    def test_parse_header_bad_header_hmac(self):
        """Test parse_header method: bad header HMAC"""
        age = pyagetool.Age()
        self.assertRaisesRegex(ValueError, ('Bad header HMAC.'),
                               age.parse_header,
                               'tests/fixtures/badheadhmac.age')

    # def test_parse_header(self):
    #     """Test parse_header method."""
    #     exp_header = """This is a file encrypted with age-tool.com, version 1
    #                     -> X25519 CJM36AHmTbdHSuOQL-NESqyVQE75f2e610iRdLPEN20
    #                     C3ZAeY64NXS4QFrksLm3EGz-uPRyI0eQsWw7LWbbYig
    #                     -> X25519 ytazqsbmUnPwVWMVx0c1X9iUtGdY4yAB08UQTY2hNCI
    #                     N3pgrXkbIn_RrVt0T0G3sQr1wGWuclqKxTSWHSqGdkc
    #                     -> scrypt bBjlhJVYZeE4aqUdmtRHfw 32768
    #                     ZV_AhotwSGqaPCU43cepl4WYUouAa17a3xpu4G2yi5k
    #                     -> ssh-rsa mhir0Q
    #                     xD7o4VEOu1t7KZQ1gDgq2FPzBEeSRqbnqvQEXdLRYy143BxR6oFxsUUJC
    #                     RB0ErXAmgmZq7tIm5ZyY89OmqZztOgG2tEB1TZvX3Q8oXESBuFjBBQkKa
    #                     MLkaqh5GjcGRrZe5MmTXRdEyNPRl8qpystNZR1q2rEDUHSEJInVLW8Otv
    #                     QRG8P303VpjnOUU53FSBwyXxDtzxKxeloceFubn_HWGcR0mHU-1e9l39m
    #                     yQEUZjIoqFIELXvh9o6RUgYzaAI-m_uPLMQdlIkiOOdbsrE6tFesRLZNH
    #                     AYspeRKI9MJ--Xg9i7rutU34ZM-1BL6KgZfJ9FSm-GFHiVWpr1MfYCo_w
    #                     -> ssh-ed25519 BjH7FA RO-wV4kbbl4NtSmp56lQcfRdRp3dEFpdQmWkaoiw6lY
    #                     51eEu5Oo2JYAG7OU4oamH03FDRP18_GnzeCrY7Z-sa8
    #                     --- fgMiVLJHMlg9fW7CVG+hPS5EAU4Zeg19LyCP7SoH5nA"""
    #
    #     age = pyagetool.Age()
    #     self.assertEqual(age.parse_header('fixtures/test.age'), exp_header)
