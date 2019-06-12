# -*- coding: utf-8 -*-
import re

"""Main module."""

class Age:
    """Main age format class"""

    def readheader(self, path):
        with open(path) as f:
            first_line = f.readline()
            # parse file format version
            m = re.match(r"This is a file encrypted with age-tool.com, "
                          "version (?P<age_version>[a-zA-Z0-9_.]+)", first_line)
            # check whether file is in age format
            if not m:
                raise ValueError('Target file is not an age-tool file.')
            # check format version
            age_version = m.group('age_version')
            if age_version != '1':
                raise ValueError('Unsupported age-tool format version.')


        return 'hello world'
