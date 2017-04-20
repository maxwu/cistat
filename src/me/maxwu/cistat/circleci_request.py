#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'


import requests
from requests.auth import HTTPBasicAuth
import logging
import json
from multiprocessing.dummy import Pool as ThreadPool

logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class CircleCiReq(object):
    """Helper to fetch build artifacts from circleci.com
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
        """
        build_num = str(build_num)
        url = cls.BASE_URL + '/'.join(['project', vcs, username, project, build_num, 'artifacts'])

        r = cls.__get_request(url, auth=HTTPBasicAuth(token, ''))
        json_res = r.json()

        for artifact in json_res:
            yield artifact['url']

    @classmethod
    def get_recent_30builds(cls, token, vcs, username, project):
        url = cls.BASE_URL + '/'.join(['project', vcs, username, project])

        r = cls.__get_request(url, auth=HTTPBasicAuth(token, ''))

        res_json = r.json()
        for index, build in enumerate(res_json):
            logger.debug("number {} \n {}\n".format(index, json.dumps(build, indent=2)))
            yield build

    @classmethod
    def get_recent_30artifacts(cls, token, vcs, username, project):
        builds = cls.get_recent_30builds(token=token, vcs=vcs, username=username, project=project)
        build_nums = [build['build_num'] for build in builds]

        for num in build_nums:
            yield cls.get_artifacts(token=token,
                                    vcs=vcs,
                                    username=username,
                                    project=project,
                                    build_num=num,
                                  )

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

