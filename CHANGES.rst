2.9
~~~

* Added Trove Classifier indicating this package is part
  of the pytest framework.

2.8
~~~

* #16: Added a license file, required for membership to
  pytest-dev.
* Releases are now made automatically by pushing a
  tagged release that passes tests on Python 3.5.

2.7
~~~

* Moved hosting to Github.

2.6
~~~

* Add support for un-named, environment-specific extras.

2.5.1
~~~~~

* Restore Python 2.6 compatibility.

2.5
~~~

* Moved hosting to `pytest-dev
  <https://bitbucket.org/pytest-dev/pytest-runner>`_.

2.4
~~~

* Added `documentation <https://pythonhosted.org/pytest-runner>`_.
* Use setuptools_scm for version management and file discovery.
* Updated internal packaging technique. README is now included
  in the package metadata.

2.3
~~~

* Use hgdistver for version management and file discovery.

2.2
~~~

* Honor ``.eggs`` directory for transient downloads as introduced in Setuptools
  7.0.

2.1
~~~

* The preferred invocation is now the 'pytest' command.

2.0
~~~

* Removed support for the alternate usage. The recommended usage (as a
  distutils command) is now the only supported usage.
* Removed support for the --junitxml parameter to the ptr command. Clients
  should pass the same parameter (and all other py.test arguments) to py.test
  via the --addopts parameter.

1.1
~~~

* Added support for --addopts to pass any arguments through to py.test.
* Deprecated support for --junitxml. Use --addopts instead. --junitxml will be
  removed in 2.0.

1.0
~~~

Initial implementation.
