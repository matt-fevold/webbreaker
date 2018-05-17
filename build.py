#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
from subprocess import Popen, PIPE, CalledProcessError, STDOUT
import sys


def main():
    # Set up your files and dirs for the build
    base_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(os.path.abspath(base_dir), 'requirements.txt')
    webbreaker_main = os.path.join(os.path.abspath(base_dir), 'webbreaker', '__main__.py')
    pyinstaller_file = os.path.join(os.path.abspath(base_dir), 'dist', 'webbreaker')
    distro = sys.platform

    # initialize python
    try:
        if os.path.isfile(sys.executable):
            python_exe = sys.executable
        else:
            print("No python executable was found!")

    except (NameError, OSError, AttributeError) as e:
        # Every other OS use this
        print("No python executable was found: {}".format(e))

    # Declare site-packages and user bin for console scripts on modules
    user_site = [python_exe, '-m', 'site', '--user-site']
    # Set user bin directory for py modules installed
    user_bin = [python_exe, '-m', 'site', '--user-base']

    def cmdline(command):
        process = Popen(
            args=command,
            stdout=PIPE,
            stderr=STDOUT
        )
        output = str(process.communicate()[0].decode('utf-8')).rstrip()
        if process.returncode >= 2:
            sys.stderr.write("An error occurred while executing {0} command.".format(command))
            raise SystemExit
        return output

    try:
        if os.path.exists(python_exe):
            if cmdline('pip'):
                try:
                    # Install openssl, wheel and pyinstaller
                    print("Validating and installing from pip open_ssl, wheel, and pyinstaller modules...")
                    # Added condition for virtual environments
                    retcode_pyopenssl = cmdline(['pip', 'install', '--user', 'pyOpenSSL'])
                    if retcode_pyopenssl != 0:
                        cmdline(['pip', 'install', 'pyOpenSSL'])

                    # Added condition for virtual environments
                    retcode_wheel = cmdline(['pip', 'install', '--user', 'wheel'])
                    if retcode_wheel != 0:
                        cmdline(['pip', 'install', 'wheel'])

                    # Added condition for virtual environments
                    retcode_pyinstaller = cmdline(['pip', 'install', '--user', 'pyinstaller==3.3'])
                    if retcode_pyinstaller != 0:
                        cmdline(['pip', 'install', 'pyinstaller==3.3'])
                        
                    # Run requirements
                    print("Installing requirements.txt...")
                    if os.path.isfile(requirements_file):
                        retcode_requirements = cmdline(['pip', "install", "--user", "-r", requirements_file])
                        if retcode_requirements !=0:
                            cmdline(['pip', "install", "-r", requirements_file])
                            
                        # Install and run pyinstaller
                        print("Starting pyinstaller build...")
                        try:
                            # Use scripts from user_base
                            pyinstaller_exe = os.path.abspath(os.path.join(cmdline(user_bin), 'bin', 'pyinstaller'))

                            if not os.path.exists(pyinstaller_exe):
                                pyinstaller_exe = os.path.abspath(os.path.join('/usr', 'bin', 'pyinstaller'))

                            if distro == "darwin":
                                cmdline([pyinstaller_exe, "--clean", "-y", "--nowindowed", "--console", "--onefile",
                                         "--name", "webbreaker", "--osx-bundle-identifier", "com.target.ps.webbreaker",
                                         "-p", str(user_site), str(webbreaker_main)])

                                print("Successfully built an osx distro {}!".format(pyinstaller_file))

                            elif distro == "linux2":
                                cmdline([pyinstaller_exe, "--clean", "-y", "--nowindowed", "--console", "--onefile",
                                 "--name", "webbreaker", "-p", str(user_site), str(webbreaker_main)])
                                print("Successfully built {}!".format(pyinstaller_file))

                            else:
                                print("We cannot build on your OS!")

                        except (NameError, AttributeError, OSError) as e:
                            print("No pyinstaller was found: {0} or an error occured with your pyinstaller command"
                                  " -> {1}!!"
                                  .format(e, 'pyinstaller'))

                    else:
                        sys.stderr.write("{} does not exist\n".format(requirements_file))
                        raise SystemExit
                except (OSError, NameError):
                    print(
                        "There was an issue installing the python requirements and executing pyinstaller, "
                        "these commands manually --> \npip install --user -r {0}\n"
                        "\npyinstaller --clean -y --onefile --name webbreaker -p "
                        "{1}, {2}\n".format(requirements_file, cmdline(user_site), webbreaker_main))
                    exit(1)

                else:
                    sys.stderr.write("Congratulations your build is successful on {0} version {1}!\n"
                                     .format(distro, os.uname()[2]))

            else:
                sys.stderr.write("Please install pip: \n"
                                 "curl -fsSL https://bootstrap.pypa.io/get-pip.py | sudo python")
                exit(1)
        else:
            sys.stderr.write("PyInstaller bindings prefer the original OSX Python 2.7\n")
            exit(1)

    except (IOError, NameError, CalledProcessError):
        sys.stderr.write("Your system does not meet the minimum requirements to compile the WebBreaker static binary!\n")
    except OSError as e:
        sys.stderr.write("Please install pip with...\n{0}\nor perhaps pyinstaller does not have the appropriate ownership or"
                         " permissions: {1}\n".format('sudo easy_install pip', e))


if __name__ == "__main__":
    main()

