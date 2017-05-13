# CIstat
Python lib to fetch CI statistics from common RESTful services as circleci, travis, jekins, or bamboo.

 - Master: [![Build Status](https://travis-ci.org/maxwu/cistat.svg?branch=master)](https://travis-ci.org/maxwu/cistat) [![codecov](https://codecov.io/gh/maxwu/cistat/branch/master/graph/badge.svg)](https://codecov.io/gh/maxwu/cistat) [![CircleCI](https://circleci.com/gh/maxwu/cistat/tree/master.svg?style=shield)](https://circleci.com/gh/maxwu/cistat/tree/master)
 - Dev: [![Build Status](https://travis-ci.org/maxwu/cistat.svg?branch=dev)](https://travis-ci.org/maxwu/cistat) [![codecov](https://codecov.io/gh/maxwu/cistat/branch/dev/graph/badge.svg)](https://codecov.io/gh/maxwu/cistat) [![CircleCI](https://circleci.com/gh/maxwu/cistat/tree/dev.svg?style=shield)](https://circleci.com/gh/maxwu/cistat/tree/dev) 
 - Jenkins: [![Build Status](http://jenkins.maxwu.me/buildStatus/icon?job=ci-stat)](http://jenkins.maxwu.me/job/ci-stat)
 - [![Code Climate](https://codeclimate.com/github/maxwu/cistat/badges/gpa.svg)](https://codeclimate.com/github/maxwu/cistat) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/007f5205467b44489394b042b5ebf83e/badge.svg)](https://www.quantifiedcode.com/app/project/007f5205467b44489394b042b5ebf83e)
 - [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Analytics](https://ga-beacon.appspot.com/UA-89976940-2/cistat-readme)](https://github.com/maxwu/cistat) [![](http://progressed.io/bar/91?title=v1%20progress)](https://github.com/maxwu/cistat)
 

## Introduction

This Python lib is derived from personal project [circleci_stat](https://github.com/maxwu/circleci_stat) on Github.
After moving to this lib, the original circleci_stat will be in just maintenance status and the results could be a test source to cistat.

The primitive idea is inspired by a fast ont-time prototype to count high runners of internal CI test from Bamboo achieved files. 
At that time, our project was a Python app and the artifacts were in XUnit common format to enable Jenkins plugins. 
With the fast prototype we can also compare the failure rate between Jenkins test statistics and Bamboo data. 
This was due to the unstable external dependencies of this project. The prototype was fast and working well.
Based on the statistic hints, we can put more efforts on the high runners to mitigate the interrupt to developerment and test team and reduce the DevOps diagnose time.
By the way, a similar tool [Bamboo_XUnit_Reader](https://github.com/maxwu/toy-box/tree/master/bamboo_xunit_reader) could be found on Github. 

So far only XUnit format artifacts are implemented. In the future, more measurement as "CodeQuality" cloud service, Lint score, Coverage history charts will be considered. 

## Installation

Install cistat Pypi dist with dev branch latest code from Github:

```shell
pip install https://github.com/maxwu/cistat/archive/dev.zip
# or
pip install git+https://github.com/maxwu/cistat.git@dev
```

Install cistat from master (release) branch on Github:
 
```shell
pip install https://github.com/maxwu/cistat/archive/master.zip
# or
pip install git+https://github.com/maxwu/cistat.git
```

## Usage

### Get latest 20 artifacts from circle CI service:

```python
vcs, project, username = 'github', 'cistat', 'maxwu'
urls = CircleCiReq.get_recent_artifacts(vcs=vcs, project=project, username=username)

# XUnit Report Object supports operator '+' and '+='
report = Xunitrpt()
for artifact in urls:
    print("fetching {}".format(artifact))
    report += Xunitrpt(xunit=CircleCiReq.get_artifact_report(url=artifact))
```

Extract top 10 failure test cases and the statistics:

```python
import pprint
print("Top 10 failure cases:")
pprint.pprint(report.get_cases_in_rate()[:10])
```

### Plot the statistic charts:

__Pie Chart__

```python
report.get_class_rpt().plot_piechart_casenum(project, "Case Num per Class")
```
The Pie Chart for case numbers per class level is:

![Pie Chart on Case Number per Class](http://oei21r8n1.bkt.clouddn.com/CIstat_PieCaseNum_Snip20170511_7_Med.png?imageView/2/w/400/q/100)

[Link to original sized Pie Chart](http://oei21r8n1.bkt.clouddn.com/CIstat_PieCaseNum_Snip20170511_7_Orig.png)

__Bar Chart__

```python
report.plot_barchart_rate(project, "Pass Rate per case")
```

The Bar Chart of Pass Rate for cistat project is:

![Bar Chart on Pass Rate](http://oei21r8n1.bkt.clouddn.com/cistat_passrate_Snip20170501_39.png?imageView/2/w/400/q/100)

[Link to original sized Bar Chart](http://oei21r8n1.bkt.clouddn.com/cistat_passrate_Snip20170501_39.png)

__Bubble Chart__

> The ROI chart is more considerable for nightly build result analysis in a testing project within XUnit test framework to control the resources as case, docker/cpu, feature integration.

> In the sample height of bubble represents the pass rate and the size of bubble shows the test efforts (Currently it is simply the case number; It will be updated to a formula on test time and case number).
> The lower the bubble positions, the bigger it shall grow to get more resource and invest to float up to 1.0 the stable status.

```python
report.get_class_rpt().plot_scatter_roi(project, "Test ROI per Class")
```

The Bubble Chart to present case ROI per class as below:

![Bubble Chart on Test ROI](http://oei21r8n1.bkt.clouddn.com/CIstat_ScatterROI_Snip20170512_9.png?imageView/2/w/400/q/100)

[Link to original sized Bubble Chart](http://oei21r8n1.bkt.clouddn.com/CIstat_ScatterROI_Snip20170512_9.png)

### Cli_app

Quick step to run above sample: `cistat-cli`. Since circleci.com has throttling limit on RESTful API, it is recommended to configure an API-Key in environmental variable or local config.yaml.

This console command is installed with Pypi dist. `cistat-cli` is the console entry point planted by PIP installer setup.py.

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
  - [X] Support operator.add
  - [X] Support operator get/set/iteritems/keys
  - [X] Add Github vcs PyPi supports
  - [X] Enhance logging
  - [X] Add class level statistic aggregation
  - [ ] Add aggregation for any level
  - [ ] Replace Xunit module counters with collections.Counter
  - [ ] Refactor to expand logging to stream/file_handler
  - [ ] Push to PyPi.org
  - [ ] Make Requests as plugins to extend with new py codes

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



