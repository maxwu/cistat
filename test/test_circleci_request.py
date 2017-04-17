#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

import unittest
from me.maxwu.cistat.circleci_request import CircleCiReq
from me.maxwu.cistat import config


class CircleCiReqTest(unittest.TestCase):

    def test_30builds(self):
        builds = CircleCiReq.get_recent_30builds(token=config.get_circleci_token(), vcs='github', username='maxwu', project='cucumber-java-toy')
        self.assertEqual(30, len(list(builds)))

    # @unittest.skip("temporarily disabled, test one single artifact list instead")
    def test_30artifacts(self):
        builds = CircleCiReq.get_recent_30artifacts(token=config.get_circleci_token(), vcs='github', username='maxwu', project='cucumber-java-toy')
        self.assertEqual(30, len(list(builds)))

    def test_artifacts80(self):
        artifacts = CircleCiReq.get_artifacts(token=config.get_circleci_token(), vcs='github', username='maxwu', project='cucumber-java-toy', build_num=80)
        count = 0
        for artifact in artifacts:
            print 'XML artifact: {}'.format(artifact)
            self.assertTrue(artifact.endswith('.xml'), 'all artifacts of build 80 are XML files')
            count += 1
        self.assertEqual(4, count, 'build 80 shall have 4 artifacts')

    def test_get_artifact_report(self):
        artifacts = CircleCiReq.get_artifacts(token=config.get_circleci_token(), vcs='github', username='maxwu',
                                              project='cucumber-java-toy', build_num=80)
        for artifact in artifacts:
            report = CircleCiReq.get_artifact_report(artifact)
            self.assertTrue(report)


if __name__ == '__main__':
    unittest.main()
