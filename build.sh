
#!/bin/sh

set -e

git clean -fXd

python setup.py bdist_wheel --universal
python setup.py bdist_egg
python setup.py sdist --formats=bztar,zip,gztar,tar
