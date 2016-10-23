"""
Implementation
"""

import os as _os
import shlex as _shlex
import contextlib as _contextlib
import sys as _sys
import operator as _operator
import itertools as _itertools

try:
	# ensure that map has the same meaning on Python 2
	from future_builtins import map
except ImportError:
	pass

import pkg_resources
import setuptools.command.test as orig


@_contextlib.contextmanager
def _save_argv(repl=None):
	saved = _sys.argv[:]
	if repl is not None:
		_sys.argv[:] = repl
	try:
		yield saved
	finally:
		_sys.argv[:] = saved


@_contextlib.contextmanager
def null():
	yield


class PyTest(orig.test):
	"""
	>>> import setuptools
	>>> dist = setuptools.Distribution()
	>>> cmd = PyTest(dist)
	"""

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

	@staticmethod
	def marker_passes(marker):
		"""
		Given an environment marker, return True if the marker is valid
		and matches this environment.
		"""
		return (
			marker
			and not pkg_resources.invalid_marker(marker)
			and pkg_resources.evaluate_marker(marker)
		)

	@staticmethod
	def _install_dists_compat(dist):
		"""
		Copy of install_dists from setuptools 27.3.0.
		"""
		ir_d = dist.fetch_build_eggs(dist.install_requires or [])
		tr_d = dist.fetch_build_eggs(dist.tests_require or [])
		return _itertools.chain(ir_d, tr_d)

	def install_dists(self, dist):
		"""
		Extend install_dists to include extras support
		"""
		i_d = getattr(orig.test, 'install_dists', self._install_dists_compat)
		return _itertools.chain(i_d(dist), self.install_extra_dists(dist))

	def install_extra_dists(self, dist):
		"""
		Install extras that are indicated by markers or
		install all extras if '--extras' is indicated.
		"""
		extras_require = dist.extras_require or {}

		spec_extras = (
			(spec.partition(':'), reqs)
			for spec, reqs in extras_require.items()
		)
		matching_extras = (
			reqs
			for (name, sep, marker), reqs in spec_extras
			# never include extras that fail to pass marker eval
			if marker and not self.marker_passes(marker)
			# include unnamed extras or all if self.extras indicated
			and (not name or self.extras)
		)
		results = list(map(dist.fetch_build_eggs, matching_extras))
		return _itertools.chain.from_iterable(results)

	@staticmethod
	def paths_on_pythonpath(paths):
		"""
		Backward compatibility for paths_on_pythonpath;
		Returns a null context if paths_on_pythonpath is
		not implemented in orig.test.
		Note that this also means that the paths iterable
		is never consumed, which incidentally means that
		the None values from dist.fetch_build_eggs in
		older Setuptools will be disregarded.
		"""
		try:
			return orig.test.paths_on_pythonpath(paths)
		except AttributeError:
			return null()

	def _super_run(self):
		if hasattr(orig.test, 'install_dists'):
			return orig.test.run(self)

		# for backward compatibility with setuptools < 27.3
		installed_dists = self.install_dists(self.distribution)
		if self.dry_run:
			self.announce('skipping tests (dry run)')
			return
		paths = map(_operator.attrgetter('location'), installed_dists)
		with self.paths_on_pythonpath(paths):
			self.with_project_on_sys_path(self.run_tests)

	def run(self):
		"""
		Override run to ensure requirements are available in this session (but
		don't install them anywhere).
		"""
		self._build_egg_fetcher()
		self._super_run()
		if self.result_code:
			raise SystemExit(self.result_code)
		return self.result_code

	def _build_egg_fetcher(self):
		"""Build an egg fetcher that respects index_url and allow_hosts"""
		# modified from setuptools.dist:Distribution.fetch_build_egg
		from setuptools.command.easy_install import easy_install
		main_dist = self.distribution
		# construct a fake distribution to store the args for easy_install
		dist = main_dist.__class__({'script_args': ['easy_install']})
		dist.parse_config_files()
		opts = dist.get_option_dict('easy_install')
		keep = (
			'find_links', 'site_dirs', 'index_url', 'optimize',
			'site_dirs', 'allow_hosts'
		)
		for key in list(opts.keys()):
			if key not in keep:
				del opts[key]   # don't use any other settings
		if main_dist.dependency_links:
			links = main_dist.dependency_links[:]
			if 'find_links' in opts:
				links = opts['find_links'][1].split() + links
			opts['find_links'] = ('setup', links)
		if self.allow_hosts:
			opts['allow_hosts'] = ('test', self.allow_hosts)
		if self.index_url:
			opts['index_url'] = ('test', self.index_url)
		install_dir_func = getattr(dist, 'get_egg_cache_dir', _os.getcwd)
		install_dir = install_dir_func()
		cmd = easy_install(
			dist, args=["x"], install_dir=install_dir, exclude_scripts=True,
			always_copy=False, build_directory=None, editable=False,
			upgrade=False, multi_version=True, no_report = True
		)
		cmd.ensure_finalized()
		main_dist._egg_fetcher = cmd

	@property
	def _argv(self):
		return ['pytest'] + self.addopts

	def run_tests(self):
		"""
		Invoke pytest, replacing argv.
		"""
		with _save_argv(_sys.argv[:1] + self.addopts):
			self.result_code = __import__('pytest').main()
