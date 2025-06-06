#!/usr/bin/env python

import os
import re
from setuptools import setup, find_packages

readme = open("README.rst").read()


def get_version():
    VERSIONFILE = os.path.join("astragalus", "__init__.py")
    VSRE = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = open(VERSIONFILE, "rt").read()
    return re.search(VSRE, version_file, re.M).group(1)


setup(
    name="astragalus",
    version=get_version(),
    description=" a utility for Cult of the Lamb's minigame Knucklebones",
    long_description=readme,
    license="MIT",
    author="lonnen",
    url="https://github.com/lonnen/astragalus",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    test_suite="tests",
)
