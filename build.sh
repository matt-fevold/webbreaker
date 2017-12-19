#!/bin/sh
# osx build
# pyinstaller --clean -y --windowed webbreaker-osx.spec
# hdiutil create ./webbreaker.dmg -srcfolder webbreaker.app -ov
# linux build
# pyinstaller --clean -y --onefile --dist $(pwd)/rpmbuild/SOURCES/webbreaker-2.0/opt/webbreaker/ --name webbreaker-cli $(pwd)/webbreaker/__main__.py 

if type pip 2>/dev/null; then
        if [ ! -f ./requirements.txt ]; then
                echo "You are not in the root directory of webbreaker where requirements.txt is located!"
        fi
else
        echo "Please install pip"
fi

if type python 2>/dev/null; then
        if [ -f ./setup.py ]; then
                pip install pyOpenSSL
                python setup.py build
                python setup.py install
        else
                echo "You are not in the root directory of webbreaker where setup.py is located!"
        fi
else
        echo "Please install Python 2.7 or higher"
fi
