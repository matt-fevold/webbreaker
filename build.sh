
#!/bin/sh

set -e

git clean -fXd

python setup.py bdist_wheel --universal
python setup.py build
python setup.py publish
