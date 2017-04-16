#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'


import yaml
import os
try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap
from me import ROOT_DIR
import logging

logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
CONFIG_YAML = "config.yaml"
DEFAULTS = {"report": "true"}


def get_cfg(path=None):
    # By default, the main module shall search config.yaml in app root dir.
    if not path:
        path = '/'.join([get_root(), CONFIG_YAML])

    try:
        with open(path, 'r') as cfg:
            yml_cfg = yaml.load(cfg)
        logger.debug("loaded config from {path}".format(path=path))
    except IOError as e:
        yml_cfg = {}
        logger.debug("config yaml not found, load chainmap instead")

    return ChainMap(os.environ, yml_cfg, DEFAULTS)


def get_root():
    return ROOT_DIR


def get_circleci_token(path=None):
    return get_cfg(path)['circleci_api_token']


def get_circleci_vcs(path=None):
    return get_cfg(path)['circleci_vcs']


def get_circleci_username(path=None):
    return get_cfg(path)['circleci_username']


def get_circleci_project(path=None):
    return get_cfg(path)['circleci_project']