"""
Setup scripts can use this to add setup.py test support for pytest runner.

Recommended usage:

execfile('pytest-runner/command.py')
setup_params = dict(...)
PyTest.install(setup_params)
setuptools.setup(**setup_params)
"""

from setuptools.command import test as _pytest_runner_test

class PyTest(_pytest_runner_test.test):
	user_options = [
		('junitxml=', None, "Output jUnit XML test results to specified "
			"file"),
		('extras', None, "Install (all) setuptools extras when running tests"),
	]

	def initialize_options(self):
		self.junitxml = None
		self.extras = False

	def finalize_options(self):
		pass

	def run(self):
		"""
		Override run to ensure requirements are available in this session (but
		don't install them anywhere).
		"""
		if self.distribution.install_requires:
			self.distribution.fetch_build_eggs(self.distribution.install_requires)
		if self.distribution.tests_require:
			self.distribution.fetch_build_eggs(self.distribution.tests_require)
		if self.distribution.extras_require and self.extras:
			map(self.distribution.fetch_build_eggs,
				self.distribution.extras_require.values())
		if self.dry_run:
			self.announce('skipping tests (dry run)')
			return
		self.with_project_on_sys_path(self.run_tests)

	def run_tests(self):
		"""
		Override run_tests to invoke pytest.
		"""
		import pytest
		import sys
		# hide command-line arguments from pytest.main
		argv_saved = list(sys.argv)
		del sys.argv[1:]
		if getattr(self, 'junitxml', None):
			sys.argv.append('--junitxml=%s' % self.junitxml)
		pytest.main()
		sys.argv[:] = argv_saved

	@classmethod
	def install(cls, setup_params):
		"""
		Given a dictionary of keyword parameters to be passed to setup(),
		update those parameters with tests_require and cmdclass to make
		pytest available.
		"""
		reqs = setup_params.setdefault('tests_require', [])
		if not any('pytest' in req for req in reqs):
			reqs.extend(['pytest>=2.1.2'])
		setup_params.setdefault('cmdclass', {}).update(
			test=cls,
		)
