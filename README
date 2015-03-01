pytest-runner
=============

Setup scripts can use pytest-runner to add setup.py test support for pytest
runner.

Usage
-----

- Add 'pytest-runner' to your 'setup_requires'. Pin to '>=2.0,<3dev' (or
  similar) to avoid pulling in incompatible versions.
- Include 'pytest' and any other testing requirements to 'tests_require'.
- Invoke tests with ``setup.py pytest``.
- Pass ``--index-url`` to have test requirements downloaded from an alternate
  index URL.
- Pass additional py.test command-line options using ``--addopts``.
- Set permanent options for the pytest distutils command in the ``[pytest]``
  section of setup.cfg.
- Set permanent options for the pytest run itself in the ``[pytest]``
  section of pytest.ini or tox.ini. See `pytest 567
  <https://bitbucket.org/hpk42/pytest/issue/567>`_ for details on
  why setup.cfg is inadequate.
- Optionally, set ``test=pytest`` in the ``[aliases]`` section of setup.cfg
  to cause ``setup.py test`` to invoke pytest.

Example
-------

The most simple usage looks like this in setup.py::

    setup(
        setup_requires=[
            'pytest-runner',
        ],
        tests_require=[
            'pytest',
        ],
    )

Additional dependencies require to run the tests (e.g. mock or pytest
plugins) may be added to tests_require and will be downloaded and
required by the session before invoking pytest.

See the `jaraco.collections
<https://bitbucket.org/jaraco/jaraco.collections/>`_ project
for real-world usage.

Standalone Example
------------------

Although ``pytest-runner`` is typically used to add pytest test
runner support to maintained packages, ``pytest-runner`` may
also be used to create standalone tests. Consider `this example
failure <https://gist.github.com/jaraco/d979a558bc0bf2194c23>`_,
reported in `jsonpickle #117
<https://github.com/jsonpickle/jsonpickle/issues/117>`_.

That single file may be cloned or downloaded and simply run on
any system with Python and Setuptools. It will download the
specified dependencies and run the tests. Afterward, the the
cloned directory can be removed and with it all trace of
invoking the test. No other dependencies are needed and no
system configuration is altered.

Then, anyone trying to replicate the failure can do so easily
and with all the power of pytest (rewritten assertions,
rich comparisons, interactive debugging, extensibility through
plugins, etc).

As a result, the communication barrier for describing and
replicating failures is made almost trivially low.

Considerations
--------------

Conditional Requirement
~~~~~~~~~~~~~~~~~~~~~~~

Because it uses Setuptools setup_requires, pytest-runner will install itself
on every invocation of setup.py. In some cases, this causes delays for
invocations of setup.py that will never invoke pytest-runner. To help avoid
this contingency, consider requiring pytest-runner only when pytest
is invoked::

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner = ['pytest_runner'] if needs_pytest else []

    # ...

    setup(
        #...
        setup_requires=[
            #... (other setup requirements)
        ] + pytest_runner,
    )


Changes
-------

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
