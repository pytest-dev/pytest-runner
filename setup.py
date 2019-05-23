#!/usr/bin/env python

import setuptools


compat = dict(
    name='pytest-runner',
    py_modules=['ptr'],
    setup_requires=['setuptools_scm >= 1.15.0'],
    entry_points={'distutils.commands': ['ptr = ptr:PyTest', 'pytest = ptr:PyTest']},
)
"""
Because pytest-runner is frequently installed by
setup_requires and thus easy_install, and because
many systems still run with setuptools prior to
30.4 in which support for declarative config was
added, supply the basic metadata here. Ref #49.
"""

if __name__ == "__main__":
    setuptools.setup(use_scm_version=True, **compat)
