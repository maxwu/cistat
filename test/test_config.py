#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

import unittest
import os
from me.maxwu.circlecistat import config


class CircleCiReqCfg(unittest.TestCase):
    def test_config_token_from_cfg(self):
        path = '/'.join([config.get_root(),
                         'test',
                         'resources',
                         'test_config.yaml']
                        )
        self.assertTrue(os.path.isfile(path))
        token = config.get_circleci_token(path)
        self.assertEqual(token, '1234567890a' * 4)

    def test_config_token_from_env(self):
        path = '/'.join([config.get_root(),
                         'test',
                         'resources',
                         'test_config_not_exists.yaml']
                        )
        fake_token = '1234567890a' * 4
        os.environ["circleci_api_token"] = fake_token
        token = config.get_circleci_token(path)
        self.assertEqual(token, fake_token)