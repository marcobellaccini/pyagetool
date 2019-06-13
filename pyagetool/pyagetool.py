# -*- coding: utf-8 -*-
import re

"""Main module."""

RL_MAX_CHARS = 200
"""int: max number of chars per-line.
"""

class Age:
    """Main age format class"""

    # b64u stands for "Base 64 Encoding with URL and Filename Safe Alphabet"
    # https://tools.ietf.org/html/rfc4648#section-5

    def _parse_header(self, path):
        """This method parses encrypted file header.

        Args:
            path: encrypted file path.

        Returns:
            The tuple (age_version, recipients).

            If something goes wrong, it will raise an exception.
        """

        with open(path) as f:
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

            # parse recipients
            recipients = []
            for recipent_line in recipent_lines:
                # if recipient start
                if re.match(r"-> [a-zA-Z0-9\-]+ ", recipent_line):
                    # append recipient entry (type, arguments)
                    recipients.append( (_parse_recipient_start(recipent_line),
                                        []) )
                    continue
                # else, if recipient body, add body part to last recipient
                # (after checking that a recipient start was found)
                if recipients:
                    recipients[-1][1].append(recipient_line)
                else:
                    raise ValueError('Malformed recipients.')


            # TODO: CHECK HMAC AFTER EXTRACTING FILE KEY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return (age_version, 0)

    def _parse_recipient_start(self, recipent_line):
        """This method parses a recipent line.

        Args:
            recipent_line: recipent line.

        Returns:
            The tuple (type, arguments).

            Where arguments is a dictionary.
        """
        m = re.match(r"X25519 (?P<b64u_header_hmac>[a-zA-Z0-9\-_=]+)", line)
