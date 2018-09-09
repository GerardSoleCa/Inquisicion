#!/usr/bin/env python

import os
import platform
from setuptools import setup, find_packages

basedir = os.path.dirname(__file__)


def write_version_py(version):
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'inquisicion/version.py'), 'w') as f:
        f.write("VERSION = '{}'\n".format(version))


def read_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'VERSION'), 'r') as f:
        version = f.read().replace('\n', '')
        return version


def get_version():
    version = read_version()
    write_version_py(version)
    return version


def get_requirements():
    if platform.system() is 'Windows':
        return
    return 'requirements.txt'


def get_entry_points():
    return {
        'console_scripts': [
            'inquisicion_bot = inquisicion.bin.bot:main'
        ]
    }


setup(
    name='inquisicion',
    version=get_version(),
    url='https://github.com/GerardSoleCa/Inquisicion',
    description='InquisicionBot',
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    dependency_links=[],
    package_data={'': ['*.json', '*.ini']},
    include_package_data=True,
    entry_points=get_entry_points()
)
