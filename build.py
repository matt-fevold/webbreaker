#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
import platform
from subprocess import Popen, PIPE, check_output
import sys


PIP = "pip"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(os.path.abspath(BASE_DIR), 'requirements.txt')
SETUP_FILE = os.path.join(os.path.abspath(BASE_DIR), 'setup.py')
WEBBREAKER_MAIN = os.path.join(os.path.abspath(BASE_DIR), 'webbreaker', '__main__.py')

# Mac Python
if sys.platform == "darwin":
    PYTHON = os.path.abspath(os.path.join('/System', 'Library', 'Frameworks', 'Python.framework', 'Versions', '2.7',
                                        'bin', 'python2.7'))
    SITEPACKAGES_CMD = [PYTHON, '-m', 'site', '--user-site']
    SITEPACKAGES_RES = Popen(SITEPACKAGES_CMD, stdout=PIPE)
    SITEPACKAGES = str(SITEPACKAGES_RES.communicate()[0].decode()).rstrip()

    PYINSTALLER_CMD = ['pyinstaller', "--clean", "-y", "--windowed", "--noconsole", "--onefile", "--name", "webbreaker",
                       "-p",
                       SITEPACKAGES, WEBBREAKER_MAIN]
    # Make a macos dmg file
    HDIUTIL_DIR = os.path.join(os.path.abspath(BASE_DIR), 'dist', 'webbreaker.app')
    HDIUTIL_CMD = ['hdiutil', 'create', BASE_DIR, '-srcfolder', HDIUTIL_DIR, '-ov']

# Linux
elif sys.platform == "linux2":
    PYTHON = os.path.abspath(os.path.join('/usr', 'bin', 'python'))
    # TODO: Clean this up
    SITEPACKAGES_CMD = [PYTHON, '-m', 'site', '--user-site']
    SITEPACKAGES_RES = Popen(SITEPACKAGES_CMD, stdout=PIPE)
    SITEPACKAGES = str(SITEPACKAGES_RES.communicate()[0].decode()).rstrip()
    #
    RPMBUILD_DIR = os.path.join(os.path.abspath(BASE_DIR), 'rpmbuild', 'SOURCES', 'webbreaker-2.0', 'opt', 'webbreaker')
    PYINSTALLER_CMD = ['pyinstaller', "--clean", "-y", "--windowed", "--noconsole", "--onefile", "--dist", RPMBUILD_DIR,
                       "--name", "webbreaker-cli", "-p",
                       SITEPACKAGES, WEBBREAKER_MAIN]

REQ_INSTALL = [PIP, "install", "--user", "-r", REQUIREMENTS_FILE, "--upgrade"]
OPEN_SSL_REQ = [PIP, "install", "--user", "pyOpenSSL", "--upgrade"]
WHEEL_REQ = [PIP, "install", "--user", "wheel", "--upgrade"]
PYINSTALLER_REQ = [PIP, "install", "--user", "PyInstaller", "--upgrade"]
SETUP_BUILD = [PYTHON, SETUP_FILE, "build"]
SETUP_INSTALL = [PYTHON, SETUP_FILE, "install", "--user"]


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        stderr=False
    )
    return str(process.communicate()[0].decode()).rstrip()


# MacOS
if sys.platform == "darwin":
    if sys.version_info[0] > 2:
        sys.stderr.write("You must have python 2.7 or later to create installer\n")
        exit(1)
    try:
        if os.path.exists(PYTHON):
            if cmdline(PIP):
                # Install openssl, wheel and pyinstaller
                check_output(OPEN_SSL_REQ, shell=True)
                check_output(WHEEL_REQ, shell=True)
                # Build and install from setup.py
                # TODO: should breaker this out into an argv
                if os.path.isfile(SETUP_FILE):
                    cmdline(SETUP_BUILD)
                    cmdline(SETUP_INSTALL)
                    # Run install requirements.txt for pyinstaller
                    if os.path.isfile(REQUIREMENTS_FILE):
                        check_output(REQ_INSTALL, shell=True)
                        # Install and run pyinstaller
                        check_output(PYINSTALLER_REQ, shell=True)
                        check_output(PYINSTALLER_CMD)
                        cmdline(HDIUTIL_CMD)
                    else:
                        sys.stderr.write("requirements.txt does not exist\n")
                        exit(1)
                else:
                    sys.stderr.write("Error with build and install with setup.py\n")
                    exit(1)
            else:
                sys.stderr.write("Please install pip\n")
                exit(1)
        else:
            sys.stderr.write("PyInstaller bindings prefer the original macos Python 2.7\n")
            exit(1)

    # Run without pyinstaller
    except (IOError, NameError):
        sys.stderr.write("Performing build and install from source only!\n")
        if cmdline(PIP):
            # Install openssl and wheel
            check_output(OPEN_SSL_REQ, shell=True)
            check_output(WHEEL_REQ, shell=True)
            if os.path.isfile(SETUP_FILE):
                cmdline(SETUP_BUILD)
                cmdline(SETUP_INSTALL)
            else:
                sys.stderr.write("Error with build and install with setup.py\n")
                exit(1)
        else:
            sys.stderr.write("Please install pip\n")
            exit(1)

if sys.platform == "linux2":
    if sys.version_info[0] > 2:
        sys.stderr.write("You must have python 2.7 or later to create installer\n")
        exit(1)
    try:
        if os.path.exists(PYTHON):
            # Install openssl, wheel and pyinstaller
            if cmdline(PIP):
                check_output(OPEN_SSL_REQ, shell=True)
                check_output(WHEEL_REQ, shell=True)
                # Build and install from setup.py
                # TODO: should breaker this out into an argv
                if os.path.isfile(SETUP_FILE):
                    cmdline(SETUP_BUILD)
                    cmdline(SETUP_INSTALL)
                    # Install from requirements.txt
                    if os.path.isfile(REQUIREMENTS_FILE):
                        check_output(REQ_INSTALL, shell=True)
                        # Added to check for centos distro
                        if str(platform.dist()[0]) == "centos":
                            # Install and run pyinstaller
                            check_output(PYINSTALLER_REQ, shell=True)
                            check_output(PYINSTALLER_CMD)
                            '''
                            TODO: add rpmbuild -ba rpmbuild/SPECS/webbreaker.spec
                            and tar cvzf webbreaker-2.0.tar.gz rpmbuild/SOURCES/webbreaker
                            '''
                        else:
                            sys.stderr.write("We are not on RedHat or CentOS\n")
                    else:
                        sys.stderr.write("requirements.txt does not exist\n")
                        exit(1)
                else:
                    sys.stderr.write("Error with build and install with setup.py\n")
                    exit(1)
            else:
                sys.stderr.write("Please install pip\n")
                exit(1)
        else:
            sys.stderr.write("PyInstaller bindings prefer the original Python 2.7\n")
            exit(1)
        # Run without pyinstaller
    except (IOError, NameError):
        sys.stderr.write("Performing build and install from source!\n")
        if cmdline(PIP):
            # Install openssl, wheel and pyinstaller
            check_output(WHEEL_REQ, shell=True)
            check_output(OPEN_SSL_REQ, shell=True)
            if os.path.isfile(SETUP_FILE):
                cmdline(SETUP_BUILD)
                cmdline(SETUP_INSTALL)
            else:
                sys.stderr.write("Error with build and install with setup.py\n")
                exit(1)
        else:
            sys.stderr.write("Please install pip\n")
            exit(1)

