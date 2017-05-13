#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Interface to circleci.com services.

 .. moduleauthor:: Max Wu <http://maxwu.me>
 .. References:: None
 
"""


import requests
from requests.auth import HTTPBasicAuth
import logging
from me.maxwu.cistat.cache import CacheIt
from me.maxwu.cistat import config

try:
    # Python 3
    from collections import ChainMap
except ImportError:
    # Python 2.7
    from chainmap import ChainMap
from me.maxwu.cistat.logger import Logger

logger = Logger(name=__name__).get_logger()


class CircleCiReq(object):
    """Helper Class to fetch build artifacts from circleci.com
    The RESTful API document could be found at https://circleci.com/docs/api/v1-reference/ 
    https://circleci.com/docs/api/
    GET: /project/:vcs-type/:username/:project
    Build summary for each of the last 30 builds for a single git repo.
    """
    BASE_URL = "https://circleci.com/api/v1.1/"

    @staticmethod
    def __get_request(url=None, *args, **kwargs):
        """ Internal method to fetch resource with Web API
        :param url: 
        :return: response object
        """
        logger.debug("__fetching__ url={}".format(url))
        if not url:
            return None

        if 'timeout' not in kwargs:
            kwargs['timeout'] = config.get_timeout()

        res = requests.get(url, *args, **kwargs)

        # Raise exception if the return code is not requests.codes.ok (200)
        res.raise_for_status()
        return res

    @classmethod
    @CacheIt(enable=config.get_cache_enable())
    def get_artifact_report(cls, url=None, *args, **kwargs):
        """ Get the artifact for URL
        :param url: URL to XUnit XML format artifact
        :return: the resource in text, usually str of XML format artifact
        """
        if not url:
            return None
        res = cls.__get_request(url=url, *args, **kwargs)
        xunit = res.text if res else None
        return xunit

    @classmethod
    def get_build_artifacts(cls, token, vcs, username, project, build_num):
        """
        Get a list of artifacts generated with given build number
        It is recommended to test it with Xunitrpt.is_xunit_report since not all artifacts are XUnit report XMLs
        """
        build_num = str(build_num)
        url = cls.BASE_URL + '/'.join(['project', vcs, username, project, build_num, 'artifacts'])

        r = cls.__get_request(url, auth=HTTPBasicAuth(token, ''))
        json_res = r.json()

        return [artifact['url'] for artifact in json_res]

    @classmethod
    def get_recent_builds(cls, token, vcs, username, project, limit=None):
        """ Get recent build numbers. Circle CI returns latest 30 builds.
        :param token: 
        :param vcs: 
        :param username: 
        :param project: 
        :param limit: number of recent builds
        :return: list of build numbers
        """
        url = cls.BASE_URL + '/'.join(['project', vcs, username, project])

        if token:
            r = cls.__get_request(url, auth=HTTPBasicAuth(token, ''))
        else:
            # token is optional for some requests with circleci.
            r = cls.__get_request(url)

        res_json = r.json()
        if not res_json:
            return None

        res_json = res_json[:limit] if limit else res_json

        return [build['build_num'] for build in res_json]

    @classmethod
    def get_recent_artifacts(cls, token=None, vcs=None, username=None, project=None, limit=None):
        """ Get artifact URLs in list for specified build
        :return: list of artifacts URLs
        """
        build_nums = cls.get_recent_builds(token=token, vcs=vcs, username=username, project=project)

        # Sort builds in descending order.
        build_nums = sorted(build_nums, reverse=True)

        artifacts2d = [ cls.get_build_artifacts(token=token,
                                             vcs=vcs,
                                             username=username,
                                             project=project,
                                             build_num=num,
                                             ) for num in build_nums
                     ]
        artifacts = reduce(lambda x,y: x+y, artifacts2d)
        # Only return XML artifacts
        artifacts = [x for x in artifacts if x.endswith('.xml')]
        return artifacts[:limit] if limit else artifacts


if __name__ == "__main__":
    pass

