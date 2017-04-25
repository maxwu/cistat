#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'


import yaml
import os
try:
    # Python 3
    from collections import ChainMap
except ImportError:
    # Python 2.7
    from chainmap import ChainMap
from me import ROOT_DIR
import logging

logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

HOME_PATH = os.path.expanduser('~')
CONFIG_PATH = '/'.join([HOME_PATH, '.cistat'])
CACHE_PATH = '/'.join([CONFIG_PATH, 'cache'])
CONFIG_YAML = '/'.join([CONFIG_PATH, 'config.yaml'])
DEFAULTS = {'cache_enable': 'true', 'cache_path': CACHE_PATH, 'circleci_api_token': None}


def get_cfg(path=None):
    """
    Read configuration items in order OS environment variables > config.yaml in path parameter > default.
    :param path: The YAML file of config, if path is None, use ~/.cistat/config.yaml by default
    :return: ChainMap of configuration items
    """
    # By default, the main module shall search config.yaml in app root dir.
    if not path:
        path = CONFIG_YAML

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
    """
    Token is sometimes not necessary on F/OSS projects if the flag is enabled already on them. 
    """
    return get_cfg(path)['circleci_api_token']


def get_circleci_vcs(path=None):
    return get_cfg(path)['circleci_vcs']


def get_circleci_username(path=None):
    return get_cfg(path)['circleci_username']


def get_circleci_project(path=None):
    return get_cfg(path)['circleci_project']