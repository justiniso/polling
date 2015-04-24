#!/usr/bin/env python

from setuptools import setup, find_packages
from polling import __version__

with open("./requirements.txt") as fp:
    requirements = fp.read()
    requirements = requirements.split("\n")

setup(
    name='polling',
    description='Powerful polling utility with many configurable options',
    version=__version__,
    author='Justin Iso',
    author_email='justin+polling@justiniso.com',
    url='http://github.com/justiniso/polling',
    download_url='',
    py_modules=['polling'],
    install_requires=requirements,
    test_suite='tests'
)