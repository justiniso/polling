#!/usr/bin/env python

from setuptools import setup, find_packages
from assertionchain import __version__

with open("./requirements.txt") as fp:
    requirements = fp.read()
    requirements = requirements.split("\n")

setup(
    name='polling',
    description='',
    version=__version__,
    author='Justin Iso',
    author_email='justin+polling@justiniso.com',
    url='',
    download_url='',
    py_modules=['polling'],
    install_requires=requirements,
    test_suite='tests'
)