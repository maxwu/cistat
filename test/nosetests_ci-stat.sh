#!/usr/bin/env bash
set -o xtrace
########################
# Step 1: Setup virtualenv
# This step is only for Jenkins. Travis and CircleCI will ignore this step.
########################

if [ -n "${WORKSPACE:+1}" ]; then
    # Path to virtualenv cmd installed by pip
    # /usr/local/bin/virtualenv
    PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
    if [ ! -d "venv" ]; then
            virtualenv venv
    fi
    . venv/bin/activate
else
    # Alternatively, $TRAVIS_REPO_SLUG could be utilized here to provide name.
    export JOB_NAME="cistat"
fi
pip install -r requirements.txt -r test/test_requirements.txt --cache-dir /tmp/$JOB_NAME

########################
# Step 2: Copy Config
########################
export CONFIG_PATH="$HOME/.cistat"
export CONFIG_YAML="$CONFIG_PATH/config.yaml"
export LOCAL_YAML="./config.yaml"
mkdir -p $CONFIG_PATH
[ -e $LOCAL_YAML ] && cp $LOCAL_YAML $CONFIG_YAML


########################
# Step 3: Execute Test
########################

DATE_STR=`date +%Y-%m-%d_%H-%M-%S`
nosetests --with-xunit --all-modules --traverse-namespace --with-html --html-report=nose_$DATE_STR.html \
--with-xcoverage --cover-package=me.maxwu --cover-inclusive --cover-html \
--logging-level=INFO --debug=me.maxwu -s -v \
--xunit-file ci-stat_nose_xunit.xml ./test
RET=$?

########################
# Step 4: PyLint
########################
cd src
pylint -f parseable -d I0011,R0801 me.maxwu | tee ../pylint.out
cd ..

########################
# Step 5: Return Nosetests Result
########################
exit $RET

