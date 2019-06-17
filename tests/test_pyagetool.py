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

    def test__parse_header_notage(self):
        """Test _parse_header method: not an age file"""
        age = pyagetool.Age()
        with open('tests/fixtures/notage.age') as f:
            self.assertRaisesRegex(ValueError, ('Target file is not an '
                                                'age-tool file\.'),
                                   age._parse_header, f)

    def test__parse_header_unsuppo_form_ver(self):
        """Test _parse_header method: unsupported format version"""
        age = pyagetool.Age()
        with open('tests/fixtures/unsuppformver.age') as f:
            self.assertRaisesRegex(ValueError, ('Unsupported age-tool '
                                                'format version.'),
                                   age._parse_header, f)

    def test__parse_header_no_header_hmac(self):
        """Test _parse_header method: missing header HMAC"""
        age = pyagetool.Age()
        with open('tests/fixtures/noheadhmac.age') as f:
            self.assertRaisesRegex(ValueError, ('Missing header HMAC.'),
                                   age._parse_header, f)

    def test__parse_header_no_recipients(self):
        """Test _parse_header method: no recipients"""
        age = pyagetool.Age()
        with open('tests/fixtures/norecipients.age') as f:
            self.assertRaisesRegex(ValueError, ('No recipients.'),
                                   age._parse_header, f)

    def test__parse_header_malformed_recipient(self):
        """Test _parse_header method: malformed recipient"""
        age = pyagetool.Age()
        with open('tests/fixtures/malformedrecipient.age') as f:
            self.assertRaisesRegex(ValueError, ('Malformed recipient line.'),
                                   age._parse_header, f)

    def test__parse_header_multirecipient(self):
        """Test _parse_header method: multirecipient"""
        age = pyagetool.Age()
        with open('tests/fixtures/multirecipient.age') as f:
            (age_version, recipients) = age._parse_header(f)
        exp_age_version = "1"
        exp_recipients = [
        ('X25519', ['CJM36AHmTbdHSuOQL-NESqyVQE75f2e610iRdLPEN20',
                   'C3ZAeY64NXS4QFrksLm3EGz-uPRyI0eQsWw7LWbbYig']),
        ('X25519', ['ytazqsbmUnPwVWMVx0c1X9iUtGdY4yAB08UQTY2hNCI',
                   'N3pgrXkbIn_RrVt0T0G3sQr1wGWuclqKxTSWHSqGdkc']),
        ('scrypt', ['bBjlhJVYZeE4aqUdmtRHfw',
                   '32768',
                   'ZV_AhotwSGqaPCU43cepl4WYUouAa17a3xpu4G2yi5k']),
        ('ssh-rsa', ['mhir0Q',
                   'xD7o4VEOu1t7KZQ1gDgq2FPzBEeSRqbnqvQEXdLRYy143BxR6oFxsUUJC'
                   'RB0ErXAmgmZq7tIm5ZyY89OmqZztOgG2tEB1TZvX3Q8oXESBuFjBBQkKa'
                   'MLkaqh5GjcGRrZe5MmTXRdEyNPRl8qpystNZR1q2rEDUHSEJInVLW8Otv'
                   'QRG8P303VpjnOUU53FSBwyXxDtzxKxeloceFubn_HWGcR0mHU-1e9l39m'
                   'yQEUZjIoqFIELXvh9o6RUgYzaAI-m_uPLMQdlIkiOOdbsrE6tFesRLZNH'
                   'AYspeRKI9MJ--Xg9i7rutU34ZM-1BL6KgZfJ9FSm-GFHiVWpr1MfYCo_w']
                   ),
        ('ssh-ed25519', ['BjH7FA',
                   'RO-wV4kbbl4NtSmp56lQcfRdRp3dEFpdQmWkaoiw6lY',
                   '51eEu5Oo2JYAG7OU4oamH03FDRP18_GnzeCrY7Z-sa8']),
        ]
        self.assertEqual(age_version, exp_age_version)
        self.assertEqual(recipients, exp_recipients)

    # RE-ENABLE THIS TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # def test__parse_header_bad_header_hmac(self):
    #     """Test _parse_header method: bad header HMAC"""
    #     age = pyagetool.Age()
    #     self.assertRaisesRegex(ValueError, ('Bad header HMAC.'),
    #                            age._parse_header,
    #                            'tests/fixtures/badheadhmac.age')
