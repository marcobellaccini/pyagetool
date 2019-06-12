# -*- coding: utf-8 -*-
import re

"""Main module."""

RL_MAX_CHARS = 200
"""int: max number of chars per-line.
"""

class Age:
    """Main age format class"""

    def parse_header(self, path):
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
            b64_header_hmac = ""
            while True:
                line = f.readline(RL_MAX_CHARS)
                if re.match(r"--- (?P<b64_header_hmac>[a-zA-Z0-9+/=]+)",
                            line):
                    break
                if not line:
                    raise ValueError('Missing header HMAC.')
                lines.append(line)

            print(b64_header_hmac)
            for a in lines:
                print(a)

        return (age_version, 0)
