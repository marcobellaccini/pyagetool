# -*- coding: utf-8 -*-
import re

"""Main module."""

RL_MAX_CHARS = 8000
"""int: max number of chars per-line.
"""


class Age:
    """Main age format class"""

    # b64u stands for "Base 64 Encoding with URL and Filename Safe Alphabet"
    # https://tools.ietf.org/html/rfc4648#section-5

    def _parse_header(self, f):
        """This method parses encrypted file header.

        BEWARE: THIS METHOD DOES NOT PERFORM HMAC CHECK

        Args:
            f: input file object.

        Returns:
            The tuple (age_version, recipients).

            If something goes wrong, it will raise an exception.
        """

        lines = [f.readline(RL_MAX_CHARS)]
        # parse file format version
        m = re.match(r"This is a file encrypted with age-tool.com, "
                     "version (?P<age_version>[a-zA-Z0-9_.]+)", lines[0])
        # check whether file is in age format
        if not m:
            raise ValueError('Target file is not an age-tool file.')
        # check format version
        age_version = m.group('age_version')
        if age_version != '1':
            raise ValueError('Unsupported age-tool format version.')
        # read the remaining part of the header and get the HMAC
        b64u_header_hmac = ""
        recipent_lines = []
        while not b64u_header_hmac:
            line = f.readline(RL_MAX_CHARS)
            # if EOF
            if not line:
                raise ValueError('Missing header HMAC.')
            # try to match HMAC
            m = re.match(r"--- (?P<b64u_header_hmac>[a-zA-Z0-9\-_=]+)", line)
            # if HMAC was found
            if m:
                b64u_header_hmac = m.group('b64u_header_hmac')
            # else, collect recipent lines
            else:
                recipent_lines.append(line)
            # collect lines for the HMAC
            lines.append(line)

        # merge recipient lines
        recipients_data = "".join(recipent_line for recipent_line
                                  in recipent_lines).rstrip("\n")
        # parse recipients
        recipents = []
        rdata_rest = recipients_data
        while rdata_rest:
            (recipient, rdata_rest) = self._get_recipient(rdata_rest)
            recipents.append(recipient)

        if not recipents:
            raise ValueError('No recipients.')

        # TODO: CHECK HMAC AFTER EXTRACTING FILE KEY!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return (age_version, recipents)

    def _get_recipient(self, recipients_data):
        """This method parses a recipent from recipients data.

        Args:
            recipients_data: recipients data.

        Returns:
            The tuple (recipient, rdata_rest).

            Where:

            - recipient is the tuple (type, arguments)

            - rdata_rest is the residual recipients data

        """
        # X25519
        m = re.match(r"-> X25519" "[ \n]"
                     "(?P<arg1>[a-zA-Z0-9-_=]+)" "[ \n]"
                     # the following will match everything until ->, EOS or
                     # whitespace is found, without consuming these
                     # expressions
                     # (i.e. it performs a lookahead assertion)
                     # https://docs.python.org/3/library/re.html
                     "(?P<arg2>.+?(?=(->)|($)|( )))"
                     "(?P<rdata_rest>.*)", recipients_data, re.DOTALL)
        if m:
            return (('X25519', [m.group('arg1'),
                                m.group('arg2').replace('\n', '')]),
                    m.group('rdata_rest'))

        # scrypt
        m = re.match(r"-> scrypt" "[ \n]"
                     "(?P<arg1>[a-zA-Z0-9-_=]+)" "[ \n]"
                     "(?P<arg2>[a-zA-Z0-9-_=]+)" "[ \n]"
                     "(?P<arg3>.+?(?=(->)|($)|( )))"
                     "(?P<rdata_rest>.*)", recipients_data, re.DOTALL)
        if m:
            return (('scrypt',
                     [m.group('arg1'), m.group('arg2'),
                      m.group('arg3').replace('\n', '')]),
                    m.group('rdata_rest'))

        # ssh-rsa
        m = re.match(r"-> ssh-rsa" "[ \n]"
                     "(?P<arg1>[a-zA-Z0-9-_=]+)" "[ \n]"
                     "(?P<arg2>.+?(?=(->)|($)|( )))"
                     "(?P<rdata_rest>.*)", recipients_data, re.DOTALL)
        if m:
            return (('ssh-rsa', [m.group('arg1'),
                                 m.group('arg2').replace('\n', '')]),
                    m.group('rdata_rest'))

        # ssh-ed25519
        m = re.match(r"-> ssh-ed25519" "[ \n]"
                     "(?P<arg1>[a-zA-Z0-9-_=]+)" "[ \n]"
                     "(?P<arg2>[a-zA-Z0-9-_=]+)" "[ \n]"
                     "(?P<arg3>.+?(?=(->)|($)|( )))"
                     "(?P<rdata_rest>.*)", recipients_data, re.DOTALL)
        if m:
            return (('ssh-ed25519',
                     [m.group('arg1'), m.group('arg2'),
                      m.group('arg3').replace('\n', '')]),
                    m.group('rdata_rest'))

        # if no match
        raise ValueError('Malformed recipient line.')
