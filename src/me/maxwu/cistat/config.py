#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Max Wu <http://maxwu.me>


import yaml
import os
try:
    # Python 3
    from collections import ChainMap
except ImportError:
    # Python 2.7
    from chainmap import ChainMap
from me import ROOT_DIR
from me.maxwu.cistat.logger import Logger

logger = Logger(name=__name__).get_logger()

HOME_PATH = os.path.expanduser('~')
CONFIG_PATH = '/'.join([HOME_PATH, '.cistat'])
CACHE_PATH = '/'.join([CONFIG_PATH, 'cache'])
CONFIG_YAML = '/'.join([CONFIG_PATH, 'config.yaml'])
DEFAULTS = dict(cache_enable='true',
                cache_path=CACHE_PATH,
                circleci_api_token=None,
                timeout=10
                )


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
    except IOError:
        yml_cfg = dict()
        logger.debug("config yaml not found, load ChainMap instead")

    return ChainMap(os.environ, yml_cfg, DEFAULTS)


def get_root():
    return ROOT_DIR


# TODO: simply replace with a __get_attr__() in close future.
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


def get_cache_path(path=None):
    return get_cfg(path)['cache_path']


def get_timeout(path=None):
    return get_cfg(path)['timeout']


def get_cache_enable(path=None):
    return get_cfg(path)['cache_enable']