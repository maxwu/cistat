# ci-stat
Python lib to fetch CI statistics from common RESTful services as circleci, travis, jekins, or bamboo.

 - branch master: [![Build Status](https://travis-ci.org/maxwu/ci-stat.svg?branch=master)](https://travis-ci.org/maxwu/ci-stat) [![codecov](https://codecov.io/gh/maxwu/ci-stat/branch/master/graph/badge.svg)](https://codecov.io/gh/maxwu/ci-stat) [![CircleCI](https://circleci.com/gh/maxwu/ci-stat/tree/master.svg?style=svg)](https://circleci.com/gh/maxwu/ci-stat/tree/master)
 - branch dev: [![Build Status](https://travis-ci.org/maxwu/ci-stat.svg?branch=dev)](https://travis-ci.org/maxwu/ci-stat) [![codecov](https://codecov.io/gh/maxwu/ci-stat/branch/dev/graph/badge.svg)](https://codecov.io/gh/maxwu/ci-stat) [![CircleCI](https://circleci.com/gh/maxwu/ci-stat/tree/dev.svg?style=svg)](https://circleci.com/gh/maxwu/ci-stat/tree/dev)
 - Private Jenkins: [![Build Status](http://jenkins.maxwu.me/buildStatus/icon?job=ci-stat)](http://jenkins.maxwu.me/job/ci-stat)
 - Project License: [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Introduction

This Python lib is derived from personal project [circleci_stat](https://github.com/maxwu/circleci_stat) on Github.
After moving to this lib, the original circleci_stat will be in just maintenance status and the results could be a test source to ci-stat.

The primitive idea is inspired by a fast prototype I have done to count high runners of internal CI test from Bamboo achieved files. 
At that time, our project was a Python app and the artifacts were in XUnit common format to enable Jenkins plugins. 
With the fast prototype we can also compare the failure rate between Jenkins test statistics and Bamboo data. 
This was due to the unstable external dependencies of this project. The prototype was fast and working well.
Based on the statistic hints, we can put more efforts on the high runners to mitigate the interrupt to developerment and test team and reduce the DevOps diagnose time.
By the way, a similar tool [Bamboo_XUnit_Reader](https://github.com/maxwu/toy-box/tree/master/bamboo_xunit_reader) could be found on Github. 
The repo was coded with best memory. 

## Work Notes
The target is to deliver a lib which could fetch CI test results from widely used CI services as TravisCI, CircelCI, on-premise Jenkins and finally can define customized scheme for any XUnit artifacts.
This lib offers statistics functions on these artifacts.

### The Development Plan

- Therefore, the development work started from CircleCI first. 
- After that, cache will be introduced and verify the regression.
- Then a refactor step here will generate models for further using.
- The 4th step I plan to turn back to add statistic functions since cache is ready.
- At last, expand other services as Travis and Jenkins with regression supports.
- Consider to customize scheme as an option on demand.

### Progress Status

CircleCI functions developed and tested. 
    - CircleCI Request interface is too tedious;
    - Working on cache now.

#### Horizontal Stories

Cloud CI Services: 
  - circle (done);
  - travis;

On-Premise CI Services:
  - Jenkins;
    - via Jenkins RESTful
        - Artifacts: "http://localhost:8080/job/Cucumber_Jvm_Selenium_Toy/13/testReport/api/json?pretty=true"
  - Bamboo;
  
Local CI files:
  - Load XUnit format files to generate the statistics.

#### Vertical Stories

Requests:
  - Artifacts fetching (done)
  - Transparent config (in-progress)
  - Cache (in-progress)
  - Concurrent with map (in-progress)

XUnit Artifacts:
  - Parser (done)
  - Counter (done)
  - Passrate (done)
    
Report:
  - High runners in table

## Usage

Get latest 30 artifacts from circle CI service:

```python
cases = Xunitrpt()
for artifacts in CircleCiReq.get_recent_30artifacts(
        token=config.get_circleci_token(),
        vcs=config.get_circleci_vcs(),
        project=config.get_circleci_project(),
        username=config.get_circleci_username()
):
    for artifact in artifacts:
        print("fetching {}".format(artifact))
        cases.accumulate_xunit(CircleCiReq.get_request(artifact).text)
 
```

Extract top 10 failure test cases and the statistics:

```python
print("Top 10 failure cases: {}".format(
            json.dumps(cases.get_cases_in_rate()[:10], indent=2))
        )

```

## Test

Run ```nosetests_ci-stat.sh```, or nosetests execution under ./test folder.
Cloud based UT on Travis and Circle.

## Configuration

Configuration item preference order is:
 
    Cli Options -> Environment Variables > Local Config.yaml 

Configuration items:

- circleci_api_token: The 40 token characters to avoid throttling.

> To test string length with shell, ```printf $STR | wc -c```

## Issues

- JUnit with Cucumber-JVM generated XUnit file but the format is weird on parameterized cases.
 
  Action: pending, will get back to Cucumber-JVM after releasing v1.0;
  
  ```xml
  <testcase classname="| 65535 | 117995 |" name="| 65535 | 117995 |" time="0.038">
    <failure message="expected:&lt;[117995]&gt; but was:&lt;[32]&gt;" type="org.junit.ComparisonFailure">org.junit.ComparisonFailure: expected:&lt;[117995]&gt; but was:&lt;[32]&gt;
	at org.junit.Assert.assertEquals(Assert.java:115)
	at org.junit.Assert.assertEquals(Assert.java:144)
	at org.maxwu.jrefresh.selenium.stepdefs.TemperatureConverterCalStepdef.check_fahrenheit_degree(TemperatureConverterCalStepdef.java:170)
	at ✽.Then Check the value against &quot;117995&quot;(10_Convert_Celsius_To_Fahrenheit.feature:21)
</failure>
  </testcase>
  ```

## Change Logs

- Feb 12, Move to ci-stat and migrate to a more general target.
- Feb 09, Add UT and removed casual codes/doctest/ut.
- Jan 20, The prototype with IPython Notebook finished.



