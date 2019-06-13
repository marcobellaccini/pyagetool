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

    def test_parse_header_malformed_recipients_no_start(self):
        """Test parse_header method: malformed recipients - no start"""
        age = pyagetool.Age()
        self.assertRaisesRegex(ValueError, ('Malformed recipients.'),
                               age.parse_header,
                               'tests/fixtures/norecipientsstart.age')

    # RE-ENABLE THIS TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # def test_parse_header_bad_header_hmac(self):
    #     """Test parse_header method: bad header HMAC"""
    #     age = pyagetool.Age()
    #     self.assertRaisesRegex(ValueError, ('Bad header HMAC.'),
    #                            age.parse_header,
    #                            'tests/fixtures/badheadhmac.age')
