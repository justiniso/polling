#!/usr/bin/env python

from setuptools import setup, find_packages
from polling import __version__

with open("requirements_tests.txt") as fp:
    requirements_tests = fp.read()
    requirements_tests = requirements_tests.split("\n")

setup(
    name='polling',
    description='Powerful polling utility with many configurable options',
    version=__version__,
    author='Justin Iso',
    author_email='justin+polling@justiniso.com',
    url='http://github.com/justiniso/polling',
    download_url='',
    py_modules=['polling'],
    tests_require=requirements_tests,
    test_suite='tests'
)