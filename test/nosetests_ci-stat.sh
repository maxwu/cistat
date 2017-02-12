#!/usr/bin/env bash

nosetests --logging-level=INFO --debug=me.maxwu -s -v --with-xunit --xunit-file ci-stat_nose_xunit.xml --with-coverage --cover-package=me.maxwu --cover-html ./test