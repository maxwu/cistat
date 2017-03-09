#!/usr/bin/env bash

# Step 1: Setup virtualenv

# Path to virtualenv cmd installed by pip
# /usr/local/bin/virtualenv
PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
if [ ! -d "venv" ]; then
        virtualenv venv
fi
. venv/bin/activate
pip install -r requirements.txt -r test/test_requirements.txt --cache-dir /tmp/$JOB_NAME

# Step 2: Execute Test
nosetests --with-xunit --all-modules --traverse-namespace --with-xcoverage --cover-package=me.maxwu --cover-inclusive --logging-level=INFO --debug=me.maxwu -s -v --xunit-file ci-stat_nose_xunit.xml --cover-html ./test

# Step 3: PyLint
cd src
pylint -f parseable -d I0011,R0801 me.maxwu | tee ../pylint.out
cd ..

