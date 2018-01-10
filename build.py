
#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
from subprocess import Popen, PIPE, check_output, CalledProcessError, STDOUT
import sys

# Set up your files and dirs for the build
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(os.path.abspath(BASE_DIR), 'requirements.txt')
SETUP_FILE = os.path.join(os.path.abspath(BASE_DIR), 'setup.py')
WEBBREAKER_MAIN = os.path.join(os.path.abspath(BASE_DIR), 'webbreaker', '__main__.py')
PYINSTALLER_FILE= os.path.join(os.path.abspath(BASE_DIR), 'dist', 'webbreaker')
DISTRO = sys.platform
PIP = "pip"
PYINSTALLER = "pyinstaller"

# initialize python
try:
    # Use Mac OS Python Standard
    PYTHON = os.path.abspath(os.path.join('/System', 'Library', 'Frameworks', 'Python.framework', 'Versions', '2.7',
                                          'bin', 'python2.7'))
except (NameError, OSError, AttributeError):
    # Every other OS use this
    PYTHON = os.path.abspath(os.path.join('/usr', 'bin', 'python'))
finally:
    # When all else fails
    PYTHON = sys.executable


def main():
    # Declare exe and install deps
    requirements_install = [PIP, "install", "--user", "-r", REQUIREMENTS_FILE]
    open_ssl_module = [PIP, "install", "--user", "pyOpenSSL"]
    wheel_module = [PIP, "install", "--user", "wheel"]
    # Required for darwin mac
    hdiutil_dir = os.path.join(os.path.abspath(BASE_DIR), 'dist', 'webbreaker.app')
    hdiutil_cmd = ['/usr/bin/hdiutil', 'create', PYINSTALLER_FILE, '-srcfolder', hdiutil_dir, '-ov']

    def cmdline(command):
        process = Popen(
            args=command,
            stdout=PIPE,
            stderr=STDOUT
        )
        output = str(process.communicate()[0].decode('utf-8')).rstrip()
        if process.returncode != 0:
            sys.stderr.write("An error occurred while executing {} command.\n".format(command))
            raise SystemExit
        return output

    sitepackages_command = [PYTHON, '-m', 'site', '--user-site']
    pyinstaller_cmd = [PYINSTALLER, "--clean", "-y", "--windowed", "--noconsole", "--onefile",
                       "--name", "webbreaker", "-p",
                       cmdline(sitepackages_command), WEBBREAKER_MAIN]

    try:
        if os.path.exists(PYTHON):
            if cmdline(PIP):
                try:
                    # Install openssl, wheel and pyinstaller
                    print("Validating and/or installing pip open_ssl and wheel modules...\n")
                    cmdline(open_ssl_module)
                    cmdline(wheel_module)
                    # Run requirements
                    if os.path.isfile(REQUIREMENTS_FILE):
                        cmdline(requirements_install)
                        # Install and run pyinstaller
                        print("Starting pyinstaller build...\n")
                        cmdline(pyinstaller_cmd)
                        print("Successfully built {}!\n".format(PYINSTALLER_FILE))
                    else:
                        sys.stderr.write("{} does not exist\n".format(REQUIREMENTS_FILE))
                        raise SystemExit
                except (OSError, NameError):
                    print(
                        "There was an issue installing the python requirements and executing pyinstaller, "
                        "these commands manually --> \npip install --user -r{0}\n{1}{2}{3}".format(
                            "pyinstaller --clean -y --windowed --onefile --name webbreaker -p ",
                            REQUIREMENTS_FILE, cmdline(sitepackages_command), WEBBREAKER_MAIN, REQUIREMENTS_FILE))
                    exit(1)

                if DISTRO == "darwin":
                    try:
                        cmdline(hdiutil_cmd)
                        print("Successfully built your DMG package {}.dmg!\n".format(PYINSTALLER_FILE))
                    except OSError:
                        print(
                            "There was an issue executing --> {0}{1}{2}{3}{4}".format('hdiutil create', PYINSTALLER_FILE,
                                                                                      '-srcfolder', hdiutil_dir, '-ov'))
                else:
                    sys.stderr.write("Congratulations your build is successful on {0} version {1}!\n"
                                     .format(DISTRO, os.uname()[2]))
            else:
                sys.stderr.write("Please install pip\n")
                exit(1)
        else:
            sys.stderr.write("PyInstaller bindings prefer the original OSX Python 2.7\n")
            exit(1)

    except (IOError, NameError, CalledProcessError):
        sys.stderr.write("Your system does not meet the minimum requirements to compile the WebBreaker static binary!\n")

if __name__ == "__main__":
    main()
