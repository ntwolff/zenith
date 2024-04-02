"""
setuptools Build Configuration
"""

from pathlib import Path
from setuptools import find_packages, setup

# -*- Installation Requires -*-

def strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req, *root):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*root, *path.split('/'))
    return [req]


def _reqs(*f):
    path = (Path.cwd() / '').joinpath(*f)
    with path.open() as fh:
        req_items = [strip_comments(l) for l in fh.readlines()]
        return [_pip_requirement(r, *f[:-1]) for r in req_items if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]

# -*- %%% -*-

setup(
    name='zenith',
    version='0.0.1',
    description='',
    author='Nick Wolff',
    author_email='wolff.nick@gmail.com',
    license='Proprietary',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    install_requires=reqs('requirements.txt'),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'zenith = app.stream.faust_app:main',
        ],
        'faust.codecs': [
            'event_serializer = app.stream.codec.event:EventSerializer',
            'admin_task_serializer = app.stream.codec.admin_task:AdminTaskSerializer',
            'risk_signal_serializer = app.stream.codec.risk_signal:RiskSignalSerializer',
        ],
    },
)
