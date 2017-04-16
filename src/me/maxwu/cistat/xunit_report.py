#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import json

class Xunitrpt(object):
    """ The XUnit Test Report Class.
    Which represents an XML file as a test report in XUnit format.
    The XSD refers to https://github.com/apache/maven-surefire/blob/master/maven-surefire-plugin/src/site/resources/xsd/surefire-test-report.xsd
    """

    def __init__(self, xunit=None):
        self.case_dict = {}
        self.accumulate_xunit(xunit)

    def get_cases(self):
        return self.case_dict.copy()

    def get_case(self, tcname=None):
        if not tcname:
            return {}
        return self.case_dict[tcname]

    def get_cases_in_rate(self, reverse=False):
        return sorted(self.case_dict.items(), lambda x, y: cmp(x[1]['rate'], y[1]['rate']), reverse=reverse)

    def __str__(self):
        return json.dumps(self.case_dict, indent=2)

    def accumulate_xunit(self, xunit=None):
        """ Get test results in dict
        :param xunit: XUnit in a string
        :param case_dict: the dict to add current xunit data onto
        :return: dict of test case {'pass': pass_count, 'fail': failure_count
        """

        if not xunit:
            # Nothing to accumulate, return original case dict.
            return self.case_dict

        root = ET.fromstring(xunit)

        for e in root.iter('testcase'):
            tcname = e.get('classname') + '.' + e.get('name')
            if tcname not in self.case_dict:
                self.case_dict[tcname] = {'pass': 0, 'fail': 0, 'skipped': 0, 'sum': 0, 'rate': 0}

            self.case_dict[tcname]['sum'] += 1

            tags = [child.tag for child in e]
            if 'failure' in tags or 'error' in tags:
                self.case_dict[tcname]['fail'] += 1
            elif 'skipped' in tags:
                self.case_dict[tcname]['skipped'] += 1
            else:
                self.case_dict[tcname]['pass'] += 1

            self.case_dict[tcname]['rate'] = (self.case_dict[tcname]['pass'] + 0.0)/self.case_dict[tcname]['sum']

        # For cascade using.
        return self

