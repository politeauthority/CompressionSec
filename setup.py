#!/usr/bin/env python
from distutils.core import setup
import subprocess
import CompressSec

vers = subprocess.check_output([
    "git",
    "rev-list",
    "HEAD",
    "--count"
])

setup(
    name='Enterprise Data',
    version='0.0.%s' % vers,
    description='Compression Tool',
    author="""
    Alix Fullerton <alix@booj.com>,
    """,
    author_email='data@booj.com',
    packages=[
        'CompressSec',
    ],
)
