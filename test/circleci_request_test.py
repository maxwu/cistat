#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

import unittest
from me.maxwu.circlecistat.circleci_request import CircleCiReq
from me.maxwu.circlecistat import config
import json


class CircleCiReqTest(unittest.TestCase):
    def test_30builds(self):
        builds = CircleCiReq.get_recent_30builds(token=config.get_cfg_token(), vcs='github', username='maxwu', project='cucumber-java-toy')
        self.assertEqual(30, len(list(builds)))

    #@unittest.skip("temporarily disabled, test one single artifact list instead")
    def test_30artifacts(self):
        builds = CircleCiReq.get_recent_30artifacts(token=config.get_cfg_token(), vcs='github', username='maxwu', project='cucumber-java-toy')
        self.assertEqual(30, len(list(builds)))

    def test_artifacts80(self):
        artifacts = CircleCiReq.get_artifacts(token=config.get_cfg_token(), vcs='github', username='maxwu', project='cucumber-java-toy', build_num=80)
        count = 0
        for artifact in artifacts:
            print 'XML artifact: {}'.format(artifact)
            self.assertTrue(artifact.endswith('.xml'), 'all artifacts of build 80 are XML files')
            count += 1
        self.assertEqual(4, count, 'build 80 shall have 4 artifacts')

    def test_get_artifact_report(self):
        artifacts = CircleCiReq.get_artifacts(token=config.get_cfg_token(), vcs='github', username='maxwu',
                                              project='cucumber-java-toy', build_num=80)
        for artifact in artifacts:
            report = CircleCiReq.get_artifact_report(artifact)
            self.assertTrue(report)

    def test_xunit_DriverFactoryTest_Sample(self):
        with open('/'.join([config.get_root(),
                            'test',
                            'resources',
                            'TEST-org.maxwu.jrefresh.selenium.DriverFactoryTest.xml']
        )) as f:
            xml = f.read()

        cases = CircleCiReq.get_case_dict(xml)
        print "Pretty format case dict:\n{}".format(json.dumps(cases, indent=2))

        self.assertEqual(4, len(cases))
        # There are no failure cases in this given sample report.
        self.assertEqual(0, len([case for case in cases if cases[case]['fail']]))

    # TEST-org.maxwu.jrefresh.selenium.TemperatureConverterTest
    def test_xunit_TemperatureConverterTest_Sample(self):

        with open('/'.join([
            config.get_root(),
            'test',
            'resources',
            'TEST-org.maxwu.jrefresh.selenium.TemperatureConverterTest.xml'
        ])) as f:
            xml = f.read()

        cases = CircleCiReq.get_case_dict(xml)
        print "Pretty format case dict:\n{}".format(json.dumps(cases, indent=2))

        self.assertEqual(49, len(cases))
        # There are 2 failure cases in this given sample report.
        self.assertEqual(2, len([case for case in cases if cases[case]['fail']]))


if __name__ == '__main__':
    unittest.main()
