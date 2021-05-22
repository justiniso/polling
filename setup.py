#!/usr/bin/env python

from setuptools import setup
from polling import __version__


setup(
    name='polling',
    description='Powerful polling utility with many configurable options',
    version=__version__,
    author='Polling',
    author_email='',
    url='http://github.com/justiniso/polling',
    license='MIT',
    download_url='',
    py_modules=['polling'],
    tests_require=[
        'mock==3.0.5',
        'pytest==5.1.1'
    ],
    test_suite='tests'
)