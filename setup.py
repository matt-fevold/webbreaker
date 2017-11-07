#!/usr/bin/env python
#  -*- coding: utf-8 -*-


import sys
import os
from webbreaker import __version__ as version
from cryptography.fernet import Fernet

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

requires = ['click',
            'configparser>=3.5.0',
            'cryptography>=1.8.0',
            'dpath>=1.4.0',
            'fortifyapi>=1.0.6',
            'gitpython',
            'httplib2',
            'mock',
            'ndg-httpsclient',
            'pyasn1',
            'pyfiglet>=0.7.5',
            'pyOpenSSL',
            'pytest-runner',
            'requests',
            'testfixtures',
            'validators',
            'webinspectapi>=1.0.15']


def set_secret():
    key = Fernet.generate_key()
    with open(".webbreaker", 'w') as secret_file:
        secret_file.write(key.decode())
    os.chmod('.webbreaker', 0o400)
    print("New secret has been set.")


if sys.argv[-1] == 'secret':
    set_secret()
    sys.exit(0)

if sys.argv[-1] == 'build':
    os.system('python setup.py sdist --formats=zip bdist_wheel')
    sys.exit(0)

try:
    setup(
        name='webbreaker',
        description='Client for Dynamic Application Security Test Orchestration (DASTO).',
        long_description=open('README.md').read(),
        version=version,
        author='Brandon Spruth, Jim Nelson, Matthew Dunaj, Kyler Witting',
        author_email='brandon.spruth2@target.com, jim.nelson2@target.com, matthew.dunaj@target.com, kyler.witting@target.com',
        license='MIT',
        url="https://github.com/target/webbreaker",
        packages=find_packages(exclude=['docs', 'images', 'tests*']),
        include_package_data=True,
        install_requires=requires,
        entry_points={
                    'console_scripts':[
                        'webbreaker = webbreaker.__main__:cli',
                    ],
                },
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
        tests_require=['pytest'],
    )
finally:
    if not os.path.isfile('.webbreaker'):
        set_secret()
