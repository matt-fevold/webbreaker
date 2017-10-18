#!/bin/sh
set -e

git clean -fXd

pip install -r requirements.txt
python setup.py build
