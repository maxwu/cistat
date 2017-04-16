#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

from me.maxwu.circlecistat import config
import unittest
import os


class CircleCiReqCfg(unittest.TestCase):
    def test_config_token_from_cfg(self):
        if os.environ.get("circleci_api_token"):
            del os.environ["circleci_api_token"]
        path = '/'.join([config.get_root(),
                         'test',
                         'resources',
                         'test_config.yaml']
                        )
        self.assertTrue(os.path.isfile(path))
        print "read config from fake config {path}".format(path=path)
        token = config.get_circleci_token(path)
        self.assertEqual(token, '123456789a' * 4)

    def test_config_token_from_env(self):
        path = '/'.join([config.get_root(),
                         'test',
                         'resources',
                         'test_config_not_exists.yaml']
                        )
        fake_token = '123456789a' * 4
        os.environ["circleci_api_token"] = fake_token
        token = config.get_circleci_token(path)
        self.assertEqual(token, fake_token)

if __name__ == '__main__':
    unittest.main()
