#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'


import requests
from requests.auth import HTTPBasicAuth
import logging
import json
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CircleCiReq(object):
    """Helper to fetch build artifacts from circleci.com
    https://circleci.com/docs/api/
    GET: /project/:vcs-type/:username/:project
    Build summary for each of the last 30 builds for a single git repo.
    """
    BASE_URL = "https://circleci.com/api/v1.1/"

    @classmethod
    def get_request(cls, *args, **kwargs):
        logger.debug("req url is {}".format(args[0]))

        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
        res = requests.get(*args, **kwargs)
        logger.debug("result is {}".format(res.text))

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

        r = cls.get_request(url, auth=HTTPBasicAuth(token, ''))
        json_res = r.json()

        for artifact in json_res:
            yield artifact['url']

    @classmethod
    def get_recent_30builds(cls, token, vcs, username, project):
        url = cls.BASE_URL + '/'.join(['project', vcs, username, project])

        r = cls.get_request(url, auth=HTTPBasicAuth(token, ''))

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
    def get_artifact_report(cls, url):
        """ Get the artifact and parse it to XUnit to return
        :param url: URL to XUnit XML format artifact
        :return: string of XML
        """
        res = cls.get_request(url)
        xunit = res.text
        return xunit

    @classmethod
    def get_case_dict(cls, xunit):
        """ Get test results in dict
        :param xunit: XUnit in a string
        :return: dict of test case {'pass': pass_count, 'fail': failure_count
        """
        root = ET.fromstring(xunit)

        case_dict = {}
        case_num = 0

        for elem in root.iter('testcase'):
            tcname = elem.get('classname') + '.' + elem.get('name')

            if 'failure' not in [child.tag for child in elem]:
                if tcname not in case_dict:
                    case_dict[tcname] = {'pass': 1, 'fail': 0}
                    case_num += 1
                else:
                    case_dict[tcname]['pass'] += 1
            else:
                if tcname not in case_dict:
                    case_dict[tcname] = {'pass': 0, 'fail': 1}
                    case_num += 1
                else:
                    case_dict[tcname]['fail'] += 1

        return case_dict

if __name__ == "__main__":
    pass

