#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Performance Test
 Since it costs seconds to pull data from CircleCI even with cache enabled, this test will analyze the time consumption
 not purely for algorithm but also for the network delay.

 .. moduleauthor:: Max Wu <http://maxwu.me>
"""
import cProfile
import json
from cistat import config
from cistat.model import Xunitrpt
from cistat.reqs import CircleCiReq


class PerfTest(object):
    @classmethod
    def test_time_profile_circleci_recent_builds(cls):
        cProfile.run("CircleCiReq.get_recent_builds(token='{}', vcs='github', username='maxwu', project='cucumber-java-toy')".format(config.get_circleci_token()))
        pass


if __name__ == '__main__':
    PerfTest.test_time_profile_circleci_recent_builds()
