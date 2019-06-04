#!/usr/bin/env python

from setuptools import setup, find_packages
from polling import __version__

with open("./requirements.txt") as fp:
    requirements = fp.read()
    requirements = requirements.split("\n")

setup(
    name='polling2',
    description='Powerful polling utility with many configurable options',
    version=__version__,
    author='Donal Mee',
    url='http://github.com/ddmee/polling2',
    download_url='',
    py_modules=['polling2'],
    install_requires=requirements,
    test_suite='tests'
)