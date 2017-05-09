CIstat: Get Statistic Data from common CI systems
========================

This project is host on Github, _`cistat <https://github.com/maxwu/cistat>`_.

----

The primitive idea is inspired by a fast ont-time prototype to count high runners of internal CI test from Bamboo achieved files.
At that time, our project was a Python app and the artifacts were in XUnit common format to enable Jenkins plugins.
With the fast prototype we can also compare the failure rate between Jenkins test statistics and Bamboo data.
This was due to the unstable external dependencies of this project. The prototype was fast and working well.
Based on the statistic hints, we can put more efforts on the high runners to mitigate the interrupt to developerment and test team and reduce the DevOps diagnose time.
By the way, a similar tool 'Bamboo_XUnit_Reader<https://github.com/maxwu/toy-box/tree/master/bamboo_xunit_reader>' could be found on Github.

So far only XUnit format artifacts are implemented. In the future, more measurement as "CodeQuality" cloud service, Lint score, Coverage history charts will be considered.
g.

Contents
----

 .. Refer to _'README.mk<https://github.com/maxwu/cistat>'_