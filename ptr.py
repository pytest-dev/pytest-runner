"""
Implementation
"""

import shlex as _shlex
import contextlib as _contextlib
import sys as _sys
import itertools as _itertools
import distutils.cmd as _cmd

import rwt.deps


@_contextlib.contextmanager
def _save_argv(repl=None):
	saved = _sys.argv[:]
	if repl is not None:
		_sys.argv[:] = repl
	try:
		yield saved
	finally:
		_sys.argv[:] = saved


class Extra(list):
	def __init__(self, item):
		spec, reqs = item
		self.name, sep, self.marker = spec.partition(':')
		super(Extra, self).__init__(reqs)

	def __bool__(self):
		return bool(self.name)

	def __iter__(self):
		"""
		Move markers onto each of the requirements.
		"""
		for req in super(Extra, self).__iter__():
			if self.marker:
				req += ';' + self.marker
			yield req


class PyTest(_cmd.Command):
	user_options = [
		('extras', None, "Install (all) setuptools extras when running tests"),
		('index-url=', None, "Specify an index url from which to retrieve "
			"dependencies"),
		('allow-hosts=', None, "Whitelist of comma-separated hosts to allow "
			"when retrieving dependencies"),
		('addopts=', None, "Additional options to be passed verbatim to the "
			"pytest runner")
	]

	def initialize_options(self):
		self.extras = False
		self.index_url = None
		self.allow_hosts = None
		self.addopts = []

	def finalize_options(self):
		if self.addopts:
			self.addopts = _shlex.split(self.addopts)

	def iter_extras(self):
		return map(Extra, self.distribution.extras_require.items())

	def run(self):
		"""
		Override run to ensure requirements are available in this session (but
		don't install them anywhere).
		"""
		named_extras = (x for x in self.iter_extras() if x.name)
		unnamed_extras = (x for x in self.iter_extras() if not x.name)
		flatten = _itertools.chain.from_iterable
		reqs = set(_itertools.chain(
			self.distribution.install_requires,
			self.distribution.tests_require,
			flatten(unnamed_extras),
			flatten(named_extras) if self.extras else (),
		))
		if self.dry_run:
			self.announce('skipping tests (dry run)')
			list(reqs)
			return

		with rwt.deps.on_sys_path(*reqs):
			self.run_tests()

		if self.result_code:
			raise SystemExit(self.result_code)
		return self.result_code

	def run_tests(self):
		"""
		Invoke pytest, replacing argv.
		"""
		with _save_argv(_sys.argv[:1] + self.addopts):
			self.result_code = __import__('pytest').main()
