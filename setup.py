#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

def main():
    setuptools.setup(
        name             = "r245",
        version          = "2019.01.10.1606",
        description      = "kill blacklisted programs on high volatile memory usage",
        long_description = long_description(),
        url              = "https://github.com/wdbm/r245",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        packages         = setuptools.find_packages(),
        install_requires = [
                           "docopt",
                           "psutil"
                           ],
        entry_points     = {
                           "console_scripts": ("r245 = r245.__init__:main")
                           },
        zip_safe         = False
    )

def long_description(
    filename = "README.md"
    ):
    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
