#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io
import sys

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

needs_pytest = set(['pytest', 'test']).intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
needs_sphinx = set(['release', 'build_sphinx', 'upload_docs']).intersection(sys.argv)
sphinx = ['sphinx', 'rst.linker'] if needs_sphinx else []
needs_wheel = set(['release', 'bdist_wheel']).intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

name = 'pytest-runner'
description = 'Invoke py.test as distutils command with dependency resolution'

setup_params = dict(
	name=name,
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/pytest-dev/" + name,
	namespace_packages=name.split('.')[:-1],
	py_modules=['ptr'],
	install_requires=[
	],
	extras_require={
	},
	setup_requires=[
		'setuptools_scm>=1.9',
	] + pytest_runner + sphinx + wheel,
	tests_require=[
		'pytest>=2.8',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Framework :: Pytest",
	],
	entry_points = {
		'distutils.commands': [
			'ptr = ptr:PyTest',
			'pytest = ptr:PyTest',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**setup_params)
