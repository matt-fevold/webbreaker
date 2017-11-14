#!/usr/bin/env python
#  -*- coding: utf-8 -*-


import sys
import os
from webbreaker import __version__ as version
from pip.req import parse_requirements
from pip.download import PipSession

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

links = []
requires = []

# Compatibility with requirements.txt and setuptools bug with cryptography module
if os.path.isfile('requirements.txt'):
    requirements = parse_requirements('requirements.txt',
                                      session=PipSession())
    for item in requirements:
        if getattr(item, 'url', None):
            links.append(str(item.url))
        if getattr(item, 'link', None):
            links.append(str(item.link))
        if item.req:
            requires.append(str(item.req))

if sys.argv[-1] == 'build':
    os.system('python setup.py sdist --formats=zip bdist_wheel')
    sys.exit(0)

setup(
    author='Brandon Spruth, Jim Nelson, Matthew Dunaj, Kyler Witting',
    author_email='brandon.spruth2@target.com, jim.nelson2@target.com, matthew.dunaj@target.com,'
                 'kyler.witting@target.com',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation ::CPython'],
    description='Client for Dynamic Application Security Test Orchestration (DASTO).',
    entry_points={
        'console_scripts': [
            'webbreaker = webbreaker.__main__:cli',
        ],
    },
    include_package_data=True,
    install_requires=requires,
    dependency_links=links,
    license='MIT',
    long_description=open('README.md').read(),
    name='webbreaker',
    packages=find_packages(exclude=['docs', 'images', 'tests*']),
    tests_require=['pytest'],
    url="https://github.com/target/webbreaker",
    version=version,
)

