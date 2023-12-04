v6.0.1
======

* Updated Trove classifier to indicate this project is inactive.

v6.0.0
======

* #49: Dropped workaround for older setuptools versions.
* Require Python 3.7.

v5.3.2
======

* #58: Fixed syntax issue in changelog.

v5.3.1
======

* Refreshed package metadata.

v5.3.0
======

* Require Python 3.6 or later.
* Refreshed package metadata.

5.2
===

* #50: This project is deprecated.

5.1
===

* #49: Surgically restore support for older setuptools versions.

5.0
===

* #42: Prefer pyproject.toml
* Refresh package metadata.
* This release now intentionally introduces the changes
  unintionally brought about in 4.5 and 4.3, where the
  adoption of declarative config adds a new requirement
  on setuptools 30.4 or later. On systems running older
  setuptools, installation of pytest-runner via
  ``easy_install`` (or ``setup_requires``), will result
  in a ``DistributionNotFound`` exception.

  All projects should pin to ``pytest-runner < 5``
  or upgrade the environment to ``setuptools >= 30.4``
  (prior to invoking setup.py).

4.5.1
=====

* #48: Revert changes from 4.5 - restoring project to the
  state at 4.4.

4.5
===

(Pulled from PyPI due to #43 and #48)

* Packaging (skeleton) refresh, including adoption of
  `black <https://pypi.org/project/black>`_ for style.

4.4
===

* #43: Detect condition where declarative config will cause
  errors and emit a UserWarning with guidance on necessary
  actions.

4.3.1
=====

* #43: Re-release of 4.2 to supersede the 4.3 release which
  proved to be backward-incompatible in that it requires
  setuptools 30.4 or possibly later (to install). In the future, a
  backward-incompatible release will re-release these changes.
  For projects including pytest-runner, particularly as
  ``setup_requires``, if support for older setuptools is required,
  please pin to ``pytest-runner < 5``.

4.3
===

(Pulled from PyPI due to #43)

* #42: Update project metadata, including pyproject.toml declaration.

4.2
===

* #40: Remove declared dependency and instead assert it at
  run time.

4.1
===

* #40: Declare dependency on Setuptools in package metadata.

4.0
===

* Drop support for Setuptools before Setuptools 27.3.0.

3.0.1
=====

* #38: Fixed AttributeError when running with ``--dry-run``.
  ``PyTest.run()`` no longer stores nor returns the result code.
  Based on the commit message for `840ff4c <https://github.com/pytest-dev/pytest-runner/commit/840ff4c2bf6c752d9770f0dd8d64a841060cf9bc>`_,
  nothing has ever relied on that value.

3.0
===

* Dropped support for Python 2.6 and 3.1.

2.12.2
======

* #33: Packaging refresh.

2.12.1
======

* #32: Fix support for ``dependency_links``.

2.12
====

* #30: Rework support for ``--allow-hosts`` and
  ``--index-url``, removing dependence on
  ``setuptools.Distribution``'s private member.
  Additionally corrects logic in marker evaluation
  along with unit tests!

2.11.1
======

* #28: Fix logic in marker evaluation.

2.11
====

* #27: Improved wording in the README around configuration
  for the distutils command and pytest proper.

2.10.1
======

* #21: Avoid mutating dictionary keys during iteration.

2.10
====

* #20: Leverage technique in `setuptools 794
  <https://github.com/pypa/setuptools/issues/794>`_
  to populate PYTHONPATH during test runs such that
  Python subprocesses will have a dependency context
  comparable to the test runner.

2.9
===

* Added Trove Classifier indicating this package is part
  of the pytest framework.

2.8
===

* #16: Added a license file, required for membership to
  pytest-dev.
* Releases are now made automatically by pushing a
  tagged release that passes tests on Python 3.5.

2.7
===

* Moved hosting to Github.

2.6
===

* Add support for un-named, environment-specific extras.

2.5.1
=====

* Restore Python 2.6 compatibility.

2.5
===

* Moved hosting to `pytest-dev
  <https://bitbucket.org/pytest-dev/pytest-runner>`_.

2.4
===

* Added `documentation <https://pythonhosted.org/pytest-runner>`_.
* Use setuptools_scm for version management and file discovery.
* Updated internal packaging technique. README is now included
  in the package metadata.

2.3
===

* Use hgdistver for version management and file discovery.

2.2
===

* Honor ``.eggs`` directory for transient downloads as introduced in Setuptools
  7.0.

2.1
===

* The preferred invocation is now the 'pytest' command.

2.0
===

* Removed support for the alternate usage. The recommended usage (as a
  distutils command) is now the only supported usage.
* Removed support for the --junitxml parameter to the ptr command. Clients
  should pass the same parameter (and all other py.test arguments) to py.test
  via the --addopts parameter.

1.1
===

* Added support for --addopts to pass any arguments through to py.test.
* Deprecated support for --junitxml. Use --addopts instead. --junitxml will be
  removed in 2.0.

1.0
===

Initial implementation.
