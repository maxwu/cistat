#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Interface to circleci.com services.

 .. moduleauthor:: Max Wu <http://maxwu.me>
 
"""
import requests
import json
from cistat import config
from cistat.cache import CacheIt
from requests.auth import HTTPBasicAuth

try:
    # Python 3
    from collections import ChainMap
except ImportError:
    # Python 2.7
    from chainmap import ChainMap
from cistat.logger import Logger, LOG_LEVEL

logger = Logger(name=__name__).get_logger()
# logger.setLevel(LOG_LEVEL['DEBUG'])


class CircleCiReq(object):
    """CircleCiReq holds the interaction with circleci.com
    The RESTful API document could be found at https://circleci.com/docs/api/v1-reference/ 
    https://circleci.com/docs/api/
    GET: /project/:vcs-type/:username/:project
    Build summary for each of the last 30 builds for a single git repo.
    """
    BASE_URL = "https://circleci.com/api/v1.1/"

    @staticmethod
    @CacheIt
    def __get_request(url=None, token=None, method='GET', *args, **kwargs):
        """ Internal method to fetch resource with Web API
        This method is the uniformed interface to fetch information from CI APIs.
        :param url: 
        :return: response object
        """
        logger.debug("__fetching__ url={}".format(url))
        if not url:
            return None

        if 'timeout' not in kwargs:
            kwargs['timeout'] = config.get_timeout()

        method = method.upper()
        method_dict = dict(GET=requests.get,
                           POST=requests.post,
                           PUT=requests.put,
                           PATCH=requests.patch,
                           DELETE=requests.delete,
                           OPTIONS=requests.options,
                           HEAD=requests.head)
        invoker = method_dict.get(method, requests.get)

        if token:
            res = invoker(url, auth=HTTPBasicAuth(token, ''), *args, **kwargs)
        else:
            res = invoker(url, *args, **kwargs)

        # Raise exception if the return code is not requests.codes.ok (2**)
        res.raise_for_status()

        # Caution: it will dump long messages in text lines.
        # logger.debug("Req for {} \nRes text: \n{}".format(url, res))

        return res.text

    @classmethod
    def get_artifact_report(cls, url=None, *args, **kwargs):
        """ Get the artifact for URL
        :param url: URL to XUnit XML format artifact
        :return: the resource in text, usually str of XML format artifact
        """
        if not url:
            return None
        res = cls.__get_request(url=url, *args, **kwargs)
        xunit = res
        return xunit

    @classmethod
    def get_build_artifacts(cls, token, vcs, username, project, build_num):
        """
        Get a list of artifacts generated with given build number
        It is recommended to test it with Xunitrpt.is_xunit_report since not all artifacts are XUnit report XMLs
        """
        build_num = str(build_num)
        url = cls.BASE_URL + '/'.join(['project', vcs, username, project, build_num, 'artifacts'])

        r = cls.__get_request(url=url, token=token)
        json_res = json.loads(r)

        return [artifact['url'] for artifact in json_res]

    @classmethod
    def get_recent_builds(cls, token=None, vcs='gh', username=None, project=None, limit=None):
        """ Get recent build json details. Circle CI returns latest 30 builds.
        :param token: 
        :param vcs: 
        :param username: 
        :param project: 
        :param limit: number of recent builds
        :return: list of build objects
        """
        if not username or not project:
            raise ValueError('Username or Project cannot be empty')

        url = cls.BASE_URL + '/'.join(['project', vcs, username, project])

        r = cls.__get_request(url=url, token=token, cache=False)

        res_json = json.loads(r)

        if not res_json:
            logger.info("Error in processing return from {}".format(url))
            return None

        if limit:
            res_json = res_json[:limit]

        return res_json

    @classmethod
    def get_recent_build_nums(cls, *args, **kwargs):
        """ Get recent build numbers. Circle CI returns latest 30 builds.
        :params: Refer to get_recent_build_nums()
        """
        return [build['build_num'] for build in cls.get_recent_builds(*args, **kwargs)]

    @classmethod
    def get_recent_artifacts(cls, token=None, vcs='gh', username=None, project=None, limit=None):
        """ Get artifact URLs in list for specified build
        :return: list of artifacts URLs
        """

        if not token:
            token = config.get_circleci_token()

        build_nums = cls.get_recent_build_nums(token=token, vcs=vcs, username=username, project=project)

        # Sort builds in descending order.
        build_nums = sorted(build_nums, reverse=True)

        artifacts2d = [cls.get_build_artifacts(token=token,
                                               vcs=vcs,
                                               username=username,
                                               project=project,
                                               build_num=num,
                                               ) for num in build_nums
                       ]
        artifacts = reduce(lambda xi, yi: xi + yi, artifacts2d)
        # Only return XML artifacts
        artifacts = [x for x in artifacts if x.endswith('.xml')]

        return artifacts[:limit] if limit else artifacts

if __name__ == "__main__":
    pass

