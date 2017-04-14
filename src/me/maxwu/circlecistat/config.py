#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap
import yaml
import os
from me import ROOT_DIR


CONFIG_YAML = "config.yaml"
DEFAULTS = {"report": "true"}


def get_cfg():
    # By default, the main module shall search config.yaml in app root dir.
    path = '/'.join([get_root(), CONFIG_YAML])
    cfg = file(path)
    ycfg = yaml.load(cfg)
    return ChainMap(os.environ, ycfg, DEFAULTS)


def get_root():
    return ROOT_DIR


def get_circleci_token():
    return get_cfg()['circleci_api_token']