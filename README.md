# ci-stat
Python lib to fetch CI statistics from common RESTful services as circleci, travis, jekins, or bamboo.

 - branch master: [![Build Status](https://travis-ci.org/maxwu/ci-stat.svg?branch=master)](https://travis-ci.org/maxwu/ci-stat) [![codecov](https://codecov.io/gh/maxwu/ci-stat/branch/master/graph/badge.svg)](https://codecov.io/gh/maxwu/ci-stat) [![CircleCI](https://circleci.com/gh/maxwu/ci-stat/tree/master.svg?style=svg)](https://circleci.com/gh/maxwu/ci-stat/tree/master)
 - branch dev: [![Build Status](https://travis-ci.org/maxwu/ci-stat.svg?branch=dev)](https://travis-ci.org/maxwu/ci-stat) [![codecov](https://codecov.io/gh/maxwu/ci-stat/branch/dev/graph/badge.svg)](https://codecov.io/gh/maxwu/ci-stat) [![CircleCI](https://circleci.com/gh/maxwu/ci-stat/tree/dev.svg?style=svg)](https://circleci.com/gh/maxwu/ci-stat/tree/dev)
 - Private Jenkins: [![Build Status](http://jenkins.maxwu.me/buildStatus/icon?job=ci-stat)](http://jenkins.maxwu.me/job/ci-stat)
 - Project License: [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## Targets
The target is to maintain a lib which could fetch CI test results from general services. 

Cloud CI Services: 
  - circle (in progress);
  - travis;

On-Premise CI Services:
  - Jenkins;
    - via Jenkins RESTful
        - Artifacts: "http://localhost:8080/job/Cucumber_Jvm_Selenium_Toy/13/testReport/api/json?pretty=true"
  - Bamboo;
  
Local CI files:
  - Load XUnit format files to generate the statistics.

Another target of current lib is to quickly figure out the high runners of failure cases from the statistic results.
Which requests a common XUnit format of test results. Considering the reality, each build could have multiple artifacts in XUnit XML format.


## Configuration

Travis and Circle.

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



