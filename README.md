# CIstat
Python lib to fetch CI statistics from common RESTful services as circleci, travis, jekins, or bamboo.

 - branch master: [![Build Status](https://travis-ci.org/maxwu/cistat.svg?branch=master)](https://travis-ci.org/maxwu/cistat) [![codecov](https://codecov.io/gh/maxwu/cistat/branch/master/graph/badge.svg)](https://codecov.io/gh/maxwu/cistat) [![CircleCI](https://circleci.com/gh/maxwu/cistat/tree/master.svg?style=svg)](https://circleci.com/gh/maxwu/cistat/tree/master)
 - branch dev: [![Build Status](https://travis-ci.org/maxwu/cistat.svg?branch=dev)](https://travis-ci.org/maxwu/cistat) [![codecov](https://codecov.io/gh/maxwu/cistat/branch/dev/graph/badge.svg)](https://codecov.io/gh/maxwu/cistat) [![CircleCI](https://circleci.com/gh/maxwu/cistat/tree/dev.svg?style=svg)](https://circleci.com/gh/maxwu/cistat/tree/dev) 
 - Private Jenkins: [![Build Status](http://jenkins.maxwu.me/buildStatus/icon?job=ci-stat)](http://jenkins.maxwu.me/job/ci-stat)
 - [![Code Issues](https://www.quantifiedcode.com/api/v1/project/007f5205467b44489394b042b5ebf83e/badge.svg)](https://www.quantifiedcode.com/app/project/007f5205467b44489394b042b5ebf83e)
 - [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Analytics](https://ga-beacon.appspot.com/UA-89976940-2/cistat-readme)](https://github.com/maxwu/cistat) [![](http://progressed.io/bar/66?title=v1%20progress)](https://github.com/maxwu/cistat)
 

## Introduction

This Python lib is derived from personal project [circleci_stat](https://github.com/maxwu/circleci_stat) on Github.
After moving to this lib, the original circleci_stat will be in just maintenance status and the results could be a test source to cistat.

The primitive idea is inspired by a fast ont-time prototype to count high runners of internal CI test from Bamboo achieved files. 
At that time, our project was a Python app and the artifacts were in XUnit common format to enable Jenkins plugins. 
With the fast prototype we can also compare the failure rate between Jenkins test statistics and Bamboo data. 
This was due to the unstable external dependencies of this project. The prototype was fast and working well.
Based on the statistic hints, we can put more efforts on the high runners to mitigate the interrupt to developerment and test team and reduce the DevOps diagnose time.
By the way, a similar tool [Bamboo_XUnit_Reader](https://github.com/maxwu/toy-box/tree/master/bamboo_xunit_reader) could be found on Github. 
The repo was coded with best memory. 

## Usage

Install from Github.
>Not 

Get latest 20 artifacts from circle CI service:

```python
   vcs, project, username = config.get_circleci_vcs(), config.get_circleci_project(), config.get_circleci_username()
   urls =CircleCiReq.get_recent_artifacts(
            token=config.get_circleci_token(),
            vcs=vcs,
            project=project,
            username=username
    )
    report = Xunitrpt()

    # XUnit Report Object supports operator.add "+"
    for artifact in urls:
        print("fetching {}".format(artifact))
        report += Xunitrpt(xunit=CircleCiReq.get_artifact_report(url=artifact))
```

Extract top 10 failure test cases and the statistics:

```python
    print("Top 10 failure cases: {}".format(report.get_cases_in_rate()[:10]))
```

Plot the statistic chart:

```python
    print("Plot Barchart of Pass Rate")
    report.plot_barchart_rate(project, "Pass Rate per case")
```
The bar chart of Pass Rate for cistat project as below:

![Bar Chart on Pass Rate](http://oei21r8n1.bkt.clouddn.com/cistat_passrate_Snip20170501_38.png?imageView/2/w/400/q/100)

## Test

Run ```nosetests_ci-stat.sh```, or nosetests execution under ./test folder.
Cloud based UT on Travis and Circle.

## Configuration

Configuration item preference order is:
 
    Cli Options >> Environment Variables >> Local Config.yaml 

Configuration items:

- circleci_api_token: The 40 token characters to avoid throttling.

> To test string length with shell, ```printf $STR | wc -c```

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
 
  - [x] CircleCI Request interface is too tedious;
  - [x] Disk Cache for RESTful request;
  - [X] Support time stat
  - [X] Echart introduction and bar chart demo
  - [ ] Add bubble chart of test ROI presentation
  - [ ] Threading on requests with map
        (Low priority since cache speeds up queries)
  - [X] Support operator \__add\__()
  - [ ] Add Github based PyPi supports

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
  - Cache (in-progress, with apache disk-map)
  - Concurrent (in-progress, multiprocessing.dummy with map)

XUnit Artifacts:
  - Parser (done)
  - Counter (done)
  - Passrate (done)
    
Report:
  - High runners in table

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



