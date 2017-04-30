#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import json
import logging
from echarts import Echart, Legend, Bar, Axis


logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Xunitrpt(object):
    """ The XUnit Test Report Class.
    Which represents an XML file as a test report in XUnit format.
    The XSD refers to below document:
    https://github.com/apache/maven-surefire/blob/master/maven-surefire-plugin/src/site/resources/xsd/surefire-test-report.xsd
    """
    DEFAULT_DICT = {'pass': 0, 'fail': 0, 'skip': 0, 'sum': 0, 'rate': 0, 'time': 0.0}

    def __init__(self, xunit=None):
        self.case_dict = {}
        if xunit:
            self.accumulate_xunit_str(xunit)

    def get_cases(self):
        return self.case_dict.copy()

    def get_case(self, tcname=None):
        if not tcname:
            return {}
        return self.case_dict[tcname]

    def get_cases_in_rate(self, reverse=False):
        return sorted(self.case_dict.items(), lambda x, y: cmp(x[1]['rate'], y[1]['rate']), reverse=reverse)

    def __str__(self, indent=2, *args, **kwargs):
        return json.dumps(self.case_dict, indent=indent, *args, **kwargs) if self.case_dict else ''

    def dump(self):
        return self.__str__(indent=2)

    def __add__(self, other):
        z = Xunitrpt()
        z.case_dict = self.case_dict.copy()

        for k, v in other.get_cases().items():
            if k not in self.case_dict:
                z.case_dict[k] = Xunitrpt.DEFAULT_DICT.copy()
                continue

            z.case_dict[k]['sum'] += v.get('sum', 0)
            z.case_dict[k]['pass'] += v.get('pass', 0)
            z.case_dict[k]['fail'] += v.get('fail', 0)
            z.case_dict[k]['skip'] += v.get('skip', 0)
            z.case_dict[k]['time'] += v.get('time', 0)
            z.cal_rate(k)

        return z

    def __eq__(self, other):
        if not self and not other:
            return True
        return self.get_cases() == other.get_cases()

    @staticmethod
    def is_xunit_report(text=None):
        if not text:
            return False
        try:
            root = ET.fromstring(text)
        except:
            return False

        if not root.tag.lower() == 'testsuite':
            logger.debug("Root {} is not testsuite".format(root.tag))
            return False

        return True

    def accumulate_xunit_str(self, xunit=None):
        """ Update data in given XUnit str to current XUnitReport Object
        If supplied with malformed str or None, silently do nothing but return itself.
        :param xunit: XUnit in a string
        :return: XunitReport Object itself after the accumulation
        """

        if not xunit or not Xunitrpt.is_xunit_report(xunit):
            # Nothing to accumulate, return original case dict.
            return self

        root = ET.fromstring(xunit)

        for e in root.iter('testcase'):
            # Naming convention: Full.Class.Name.MethodName
            tcname = e.get('classname', '**NoClass**') + '.' + e.get('name', '**NoTC**')

            if tcname not in self.case_dict:
                self.case_dict[tcname] = Xunitrpt.DEFAULT_DICT

            self.case_dict[tcname]['sum'] += 1
            # time is a float of seconds
            self.case_dict[tcname]['time'] += float(e.get('time', 0))

            tags = [child.tag for child in e]
            if 'failure' in tags or 'error' in tags:
                self.case_dict[tcname]['fail'] += 1
            elif 'skipped' in tags:
                self.case_dict[tcname]['skip'] += 1
            else:
                self.case_dict[tcname]['pass'] += 1

            self.cal_rate(tcname)

        # For cascade using.
        return self

    def cal_rate(self, tcname):
        if self.case_dict[tcname]['sum'] == 0:
            self.case_dict[tcname]['rate'] = 0
        else:
            self.case_dict[tcname]['rate'] = (self.case_dict[tcname]['pass'] + 0.0) / self.case_dict[tcname]['sum']
        return self.get_case(tcname)['rate']

    # TODO: implement case granularity first.
    def plot_barchart_rate(self, title='CIStat', sub_title='Bar chart on pass rate'):
        tcnames = self.case_dict.keys()
        chart = Echart(title, sub_title)
        rates = [self.get_case(x)['rate'] for x in tcnames]
        chart.use(Bar('Pass Rate', rates))
        chart.use(Legend(['Pass Rate']))
        chart.use(Axis('category', 'bottom', data=map(Xunitrpt.get_case_shortname, tcnames)))
        chart.plot()

    @staticmethod
    def get_case_shortname(tcname):
        res = ''.join(tcname[-18:])
        if len(res) >= 18:
            res = '+' + res
        return res