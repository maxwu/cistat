#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

import yaml
import os
from me import ROOT_DIR


CONFIG_YAML = "config.yaml"

def get_cfg():
    # By default, the main module shall search config.yaml in app root dir.
    path = '/'.join([get_root(), CONFIG_YAML])
    cfg = file(path)
    ycfg = yaml.load(cfg)
    return ycfg


def get_root():
    return ROOT_DIR


# FIXME: Considering a general env filter to figure out all "circleci_" prefixed environmental variables.
def get_cfg_token():
    if os.environ.has_key('circleci_api_token'):
        value = os.environ['circleci_api_token']
    else:
        value = get_cfg()['circleci']['api_token']
    return value