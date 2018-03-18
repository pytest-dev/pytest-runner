#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

name = 'pytest-runner'
description = 'Invoke py.test as distutils command with dependency resolution'
nspkg_technique = 'native'
"""
Does this package use "native" namespace packages or
pkg_resources "managed" namespace packages?
"""

params = dict(
	name=name,
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/pytest-dev/" + name,
	namespace_packages=(
		name.split('.')[:-1] if nspkg_technique == 'managed'
		else []
	),
	py_modules=['ptr'],
	python_requires='>=2.7,!=3.0,!=3.1',
	install_requires=[
		# setuptools 27.3 is required at run time
	],
	extras_require={
		'testing': [
			# upstream
			'pytest>=2.8',
			'pytest-sugar>=0.9.1',
			'collective.checkdocs',
			'pytest-flake8',

			# local
			'pytest-virtualenv',
		],
		'docs': [
			# upstream
			'sphinx',
			'jaraco.packaging>=3.2',
			'rst.linker>=1.9',

			# local
		],
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Framework :: Pytest",
	],
	entry_points={
		'distutils.commands': [
			'ptr = ptr:PyTest',
			'pytest = ptr:PyTest',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**params)
