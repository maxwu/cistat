#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test CircleCI interfaces

 .. moduleauthor:: Max Wu <http://maxwu.me>
"""

import unittest
from cistat import config
from cistat.model import Xunitrpt
from cistat.reqs import CircleCiReq


class CircleCiReqTest(unittest.TestCase):
    def test_30builds(self):
        builds = CircleCiReq.get_recent_builds(token=config.get_circleci_token(), vcs='github', username='maxwu', project='cucumber-java-toy')
        self.assertEqual(30, len(builds))

    def test_2builds(self):
        builds = CircleCiReq.get_recent_builds(token=config.get_circleci_token(),
                                               vcs='github',
                                               username='maxwu',
                                               project='cucumber-java-toy',
                                               limit=2)
        self.assertEqual(2, len(builds))

    # @unittest.skip("temporarily disabled, test one single artifact list instead")
    def test_artifacts(self):
        artifacts = CircleCiReq.get_recent_artifacts(token=config.get_circleci_token(),
                                                     vcs='github', username='maxwu',
                                                     project='cucumber-java-toy',
                                                     )

        for artifact in artifacts:
            self.assertTrue(artifact.startswith('http'), 'artifact url does not start with http')

    def test_artifacts80(self):
        artifacts = CircleCiReq.get_build_artifacts(token=config.get_circleci_token(),
                                                    vcs='github', username='maxwu',
                                                    project='cucumber-java-toy', build_num=80)

        for artifact in artifacts:
            print 'XML artifact: {}'.format(artifact)
            self.assertTrue(artifact.endswith('.xml'), 'all artifacts of build 80 are XML files')

        self.assertEqual(4, len(artifacts), 'build 80 shall have 4 artifacts')

    def test_get_artifact_report_from_build_num(self):
        artifacts = CircleCiReq.get_build_artifacts(token=config.get_circleci_token(),
                                                    vcs='github', username='maxwu',
                                                    project='cucumber-java-toy', build_num=80)
        for artifact in artifacts:
            report = CircleCiReq.get_artifact_report(url=artifact)
            print 'XUnit artifact: {}'.format(artifact)
            self.assertTrue(Xunitrpt.is_xunit_report(report))

    def test_get_artifact_report(self):
        url = 'https://80-77958022-gh.circle-artifacts.com/0/tmp/circle-junit.BxjS188/junit/TEST-org.maxwu.jrefresh.HttpApi.SourceIpApiTest.xml'

        str_xunit = CircleCiReq.get_artifact_report(url=url)
        print("----Artifact:----\n{}".format(str_xunit))

        report = Xunitrpt(xunit=str_xunit)
        print("----XUnitObj:----\n{}".format(report))

        self.assertDictEqual(report.get_case('org.maxwu.jrefresh.HttpApi.SourceIpApiTest.httpFreegeoipJsonTest'),
                             {
                                 "fail": 0,
                                 "sum": 1,
                                 "skip": 0,
                                 "rate": 1.0,
                                 "pass": 1,
                                 'time': 0.365,
                             }
                             )

    def test_get_artifact_report_none_url(self):
        self.assertIsNone(CircleCiReq.get_artifact_report(timeout=5))

    def test_get_artifact_report_empty_url(self):
        self.assertIsNone(CircleCiReq.get_artifact_report(url=''))


if __name__ == '__main__':
    unittest.main()
