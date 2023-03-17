#!/bin/zsh

rm -rf dist build dartrrig.egg-info

python3 setup.py clean --all install clean --all
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*