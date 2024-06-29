#!/bin/zsh

rm -rf dist build dartrrig.egg-info

CACHE=`cat requirements.txt| grep adt_cache`
sed -i -e "s/adt_cache==0.0.[0-9]\{1,2\}/$CACHE/g" setup.py

CRAWLER=`cat requirements.txt| grep crawler_commons`
sed -i -e "s/crawler_commons==0.0.[0-9]\{1,2\}/$CRAWLER/g" setup.py

python3 setup.py clean --all install clean --all
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*.tar.gz dist/*.whl