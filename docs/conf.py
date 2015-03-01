#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hgtools.managers

# use hgtools to get the version
hg_mgr = hgtools.managers.RepoManager.get_first_valid_manager()

extensions = [
    'sphinx.ext.autodoc',
]

# General information about the project.
project = 'pytest-runner'
copyright = '2015 Jason R. Coombs'

# The short X.Y version.
version = hg_mgr.get_current_version()
# The full version, including alpha/beta/rc tags.
release = version

master_doc = 'index'
