from __future__ import unicode_literals

import io
import os
import shutil
import sys
import tarfile
import textwrap
import time
import itertools

import pytest


def DALS(s):
    "dedent and left-strip"
    return textwrap.dedent(s).lstrip()


def make_sdist(dist_path, files):
    """
    Create a simple sdist tarball at dist_path, containing the files
    listed in ``files`` as ``(filename, content)`` tuples.
    """

    with tarfile.open(dist_path, 'w:gz') as dist:
        for filename, content in files:
            file_bytes = io.BytesIO(content.encode('utf-8'))
            file_info = tarfile.TarInfo(name=filename)
            file_info.size = len(file_bytes.getvalue())
            file_info.mtime = int(time.time())
            dist.addfile(file_info, fileobj=file_bytes)


@pytest.fixture
def venv(virtualenv):
    yield virtualenv
    # Workaround virtualenv not cleaning itself as it should...
    virtualenv.delete = True
    virtualenv.teardown()


setuptools_reqs = [
    'setuptools',
    'setuptools==27.3.0',
    'setuptools==32.3.1',
    'setuptools==36.3.0',
] if sys.version_info < (3, 7) else [
    'setuptools',
    'setuptools==38.4.1',
]
args_variants = ['', '--extras']


@pytest.mark.parametrize(
    'setuptools_req, test_args',
    itertools.product(setuptools_reqs, args_variants),
)
def test_egg_fetcher(venv, setuptools_req, test_args):
    test_args = test_args.split()
    # Install pytest & pytest-runner.
    venv.run('python setup.py develop', cwd=os.getcwd())
    venv.run('pip install pytest')
    # Install setuptools version.
    venv.run('pip install -U'.split() + [setuptools_req])
    # For debugging purposes.
    venv.run('pip freeze --all')
    # Prepare fake index.
    index_dir = (venv.workspace / 'index').mkdir()
    for n in range(5):
        dist_name = 'barbazquux' + str(n + 1)
        dist_version = '0.1'
        dist_sdist = '%s-%s.tar.gz' % (dist_name, dist_version)
        dist_dir = (index_dir / dist_name).mkdir()
        make_sdist(dist_dir / dist_sdist, (
            ('setup.py', textwrap.dedent(
                '''
                from setuptools import setup
                setup(
                    name={dist_name!r},
                    version={dist_version!r},
                    py_modules=[{dist_name!r}],
                )
                '''
            ).format(dist_name=dist_name, dist_version=dist_version)),
            (dist_name + '.py', ''),
        ))
        with (dist_dir / 'index.html').open('w') as fp:
            fp.write(DALS(
                '''
                <!DOCTYPE html><html><body>
                <a href="{dist_sdist}" rel="internal">{dist_sdist}</a><br/>
                </body></html>
                '''
            ).format(dist_sdist=dist_sdist))
    # Move barbazquux1 out of the index.
    shutil.move(index_dir / 'barbazquux1', venv.workspace)
    barbazquux1_link = (
        'file://' + str(venv.workspace.abspath())
        + '/barbazquux1/barbazquux1-0.1.tar.gz'
        + '#egg=barbazquux1-0.1'
    )
    # Prepare fake project.
    project_dir = (venv.workspace / 'project-0.1').mkdir()
    with open(project_dir / 'setup.py', 'w') as fp:
        fp.write(DALS(
            '''
            from setuptools import setup
            setup(
                name='project',
                version='0.1',
                dependency_links = [
                    {barbazquux1_link!r},
                ],
                setup_requires=[
                    'pytest-runner',
                ],
                install_requires=[
                    'barbazquux1',
                ],
                tests_require=[
                    'pytest',
                    'barbazquux2',
                ],
                extras_require={{
                    ':"{sys_platform}" in sys_platform': 'barbazquux3',
                    ':"barbazquux" in sys_platform': 'barbazquux4',
                    'extra': 'barbazquux5',
                }}
            )
            ''').format(sys_platform=sys.platform,
                        barbazquux1_link=barbazquux1_link))
    with open(project_dir / 'setup.cfg', 'w') as fp:
        fp.write(DALS(
            '''
            [easy_install]
            index_url = .
            '''))
    with open(project_dir / 'test_stuff.py', 'w') as fp:
        fp.write(DALS(
            '''
            import pytest

            def test_stuff():
                import barbazquux1
                import barbazquux2
                import barbazquux3
                with pytest.raises(ImportError):
                    import barbazquux4
                if {importable_barbazquux5}:
                    import barbazquux5
                else:
                    with pytest.raises(ImportError):
                        import barbazquux5
            ''').format(importable_barbazquux5=('--extras' in test_args)))
    # Run fake project tests.
    cmd = 'python setup.py pytest'.split()
    cmd += ['--index-url=' + index_dir.abspath()]
    cmd += test_args
    venv.run(cmd, cwd=project_dir)
