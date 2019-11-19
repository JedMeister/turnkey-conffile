# Copyright (c) 2019 TurnKey GNU/Linux <admin@turnkeylinux.org>
#
# turnkey-conffile is open source software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.

import os
from pathlib import Path

class ConfFileError(Exception):
    pass


class ConfFile:
    """Configuration file class (targeted at simple shell type configs)

       Note v2 is not compatible with previous v1 ConfFile

    Usage:

        conf = ConfFile('path/to/conf', ['req_arg1', 'req_arg2'])

        print(conf[req_arg1]) # display ARG1 value from /path/to/conf
        conf[arg2] = value    # set ARG2 value
        conf.write()          # write new/update config to /path/to/conf

    Format:

        # comments are ignored
        NAME=alon
        AGE=29

    """
    def __init__(self, conf_file=None, required=[], error=True):
        self._dict = {}
        self.file = conf_file
        self.path = Path(conf_file)
        self.required = required
        self.read(error=error)
        self.validate_required(required, error=error)

    def validate_required(self, required=[], error=True):
        """Check if required values exist in conf. If all set, return True.
        If not all set and error=True, then raise exception, otherwise return
        False.
        """
        for attr in required:
            if attr not in self._dict:
                if error:
                    raise ConfFileError(
                        "'{attr}' not specified in {self.conf_file}.")
                else:
                    return False
        return True

    def read(self, error=True):
        conf_file = self.conf_path
        if not conf_file.is_file():
            if error:
                raise ConfFileError(f"Conf file '{conf_file}' not found.")
            return

        with conf_file.open() as fob:
            for line in fob:
                line = line.rstrip()
                if not line or line.startswith("#"):
                    continue
                key, *val = line.split("=")
                self._dict[key.strip().lower()] = ''.join(val).strip()

    def write(self):
        with self.conf_path.open("w") as fob:
            items = list(self.items())
            items.sort()
            for key, val in items:
                print("%s=%s" % (key.upper(), val), file=fob)

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def __iter__(self):
        return self._dict.__iter__()

    def __contains__(self, key):
        return self._dict.__contains__(key)

    def __len__(self):
        return self._dict.__len__()

    def __delete__(self, key):
        try:
            self._dict.__delete__(key)
        except KeyError as e:
            raise KeyError(e.msg)

    def __getitem__(self, key):
        try:
            return self._dict__getitem__(key)
        except KeyError as e:
            raise KeyError(e.msg)

    def __setitem__(self, key, val):
        self._dict.__setitem__(key, value)
