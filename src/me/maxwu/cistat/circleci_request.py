#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'


import requests
from requests.auth import HTTPBasicAuth
import logging
import json
from multiprocessing.dummy import Pool as ThreadPool
try:
    # Python 3
    from collections import ChainMap
except ImportError:
    # Python 2.7
    from chainmap import ChainMap


logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class CircleCiReq(object):
    """Helper Class to fetch build artifacts from circleci.com
    The RESTful API document could be found at https://circleci.com/docs/api/v1-reference/ 
    https://circleci.com/docs/api/
    GET: /project/:vcs-type/:username/:project
    Build summary for each of the last 30 builds for a single git repo.
    """
    BASE_URL = "https://circleci.com/api/v1.1/"

    @classmethod
    def __get_request(cls, url=None, *args, **kwargs):
        logger.debug("__fetching__ url={}".format(url))
        if not url:
            return None

        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
        res = requests.get(url, *args, **kwargs)

        # Raise exception if the return code is not requests.codes.ok (200)
        res.raise_for_status()
        return res

    @classmethod
    def get_artifacts(cls, token, vcs, username, project, build_num):
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

        r = cls.__get_request(url, auth=HTTPBasicAuth(token, ''))

        res_json = r.json()
        if not res_json:
            return None

        res_json = res_json[:limit] if limit else res_json

        return [build['build_num'] for build in res_json]

    @classmethod
    def get_recent_artifacts(cls, token=None, vcs=None, username=None, project=None):
        """ Get artifact URLs in list for specified build
        :param token: 
        :param vcs: 
        :param username: 
        :param project: 
        :param limit: 
        :return: list of artifacts URLs
        """
        build_nums = cls.get_recent_builds(token=token, vcs=vcs, username=username, project=project)

        return [cls.get_artifacts(token=token,
                                    vcs=vcs,
                                    username=username,
                                    project=project,
                                    build_num=num,
                                  ) for num in build_nums
                ]

    @classmethod
    def get_artifact_report(cls, url=None, *args, **kwargs):
        """ Get the artifact and parse it to XUnit to return
        :param url: URL to XUnit XML format artifact
        :return: string of XML
        """
        res = cls.__get_request(url=url, *args, **kwargs)
        xunit = res.text if res else None
        return xunit

if __name__ == "__main__":
    pass

