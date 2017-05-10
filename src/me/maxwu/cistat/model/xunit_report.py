#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""XUnit Report Model  
 - Xunitrpt class with encapsulated add, iadd, iteritem, keys, get/setitem, et.
 - General utilities as class method.
 
 .. moduleauthor:: Max Wu <http://maxwu.me>
"""
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import json
from echarts import Echart, Legend, Bar, Axis
from me.maxwu.cistat.logger import Logger

logger = Logger(name=__name__).get_logger()


class Xunitrpt(object):
    """ The XUnit Test Report Class.
    Which represents an XML file as a test report in XUnit format.
    The XSD refers to below document:
    https://github.com/apache/maven-surefire/blob/master/maven-surefire-plugin/src/site/resources/xsd/surefire-test-report.xsd
    ----
    : __add__, __iadd__ is overridden to combine two reports.
    : In general, __iteritem__ is also delegated by internal dict but it is not a full surrogate and not recommended to use directly.
    : __getitem__() and __setitem__() are overridden to operate case dict counters.
    However, __delitem__, __set/get/delslice__ are not implemented. So it is not a full overriding for [] operator.
    : The class level statistics are handled with same type of Xunitrpt, based on original Xunitrpt object on method level.
    """
    DEFAULT_DICT = {'pass': 0, 'fail': 0, 'skip': 0, 'sum': 0, 'rate': 0, 'time': 0.0}

    def __init__(self, xunit=None):
        self.case_dict = dict()
        if xunit:
            self.accumulate_xunit_str(xunit)

    def __getitem__(self, item):
        return self.get_case(item)

    def __setitem__(self, key, value):
        return self.case_dict.__setitem__(key, value)

    def get_cases_in_rate(self, reverse=False):
        return sorted(self.case_dict.items(), lambda x, y: cmp(x[1]['rate'], y[1]['rate']), reverse=reverse)

    def __str__(self, indent=2, *args, **kwargs):
        return json.dumps(self.case_dict, indent=indent, *args, **kwargs) if self.case_dict else ''

    def __add__(self, other):
        """operator.add as: a = x + y or a = a + i
        Here __add__ will return a new object copy after operation. 
        :param other: An iterable as dict, Xunitrpt, et.
        :return: A new object of result Xunitrpt type
        """
        z = Xunitrpt()
        z.case_dict = self.case_dict.copy()
        z.extend(other)
        return z

    def __iadd__(self, other):
        """ operator.idd as: a += i
        :param other: An iterable as dict, Xunitrpt, et.
        :return: The original operand after updating with data from other.
        """
        return self.extend(other)

    def extend(self, other):
        for k, v in other:
            if k not in self.keys():
                self[k] = Xunitrpt.DEFAULT_DICT.copy()
                continue
            for sk in ['sum', 'pass', 'fail', 'skip', 'time']:
                self[k][sk] += v.get(sk, 0)
            self.cal_rate(k)
        return self

    def __iter__(self):
        return self.case_dict.iteritems()

    def keys(self):
        return self.case_dict.keys()

    def __eq__(self, other):
        if not self and not other:
            return True
        return self.get_cases() == other.get_cases()

    # __len__ also on the MRO chain of __nonzero__() call.
    def __len__(self):
        return self.case_dict.__len__()

    def dump(self):
        return self.__str__(indent=2)

    def get_cases(self):
        return self.case_dict.copy()

    def get_case(self, tcname=None):
        return self.case_dict.get(tcname, dict())

    @staticmethod
    def get_case_shortname(tcname):
        ls = tcname.split('.')
        if len(ls) <= 1:
            return tcname
        prefix = ''.join([x[0] for x in ls[:-1]])
        return prefix + '.' + ls[-1]

    @staticmethod
    def get_class_name(tcname):
        ls = tcname.split('.')
        return '.'.join(ls[:-1])

    @staticmethod
    def get_class_shortname(classname):
        return Xunitrpt.get_case_shortname(classname)

    @staticmethod
    def is_xunit_report(text=None):
        if not text:
            return False
        try:
            root = ET.fromstring(text)
        except:
            return False

        if not root.tag.lower() == 'testsuite':
            logger.info("doc root {} is not testsuite".format(root.tag))
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
            clsname = e.get('classname', 'Unnamed')
            if not clsname:
                clsname = 'Unamed'
            ttcname = e.get('name', 'unnamed')
            if not ttcname:
                ttcname = 'unnamed'
            tcname = clsname + '.' + ttcname

            if tcname not in self.case_dict:
                self[tcname] = Xunitrpt.DEFAULT_DICT.copy()

            self[tcname]['sum'] += 1
            # time is a float of seconds
            self[tcname]['time'] += float(e.get('time', 0))

            tags = [child.tag for child in e]
            if 'failure' in tags or 'error' in tags:
                self[tcname]['fail'] += 1
            elif 'skipped' in tags:
                self[tcname]['skip'] += 1
            else:
                self[tcname]['pass'] += 1

            self.cal_rate(tcname)

        # For cascade using.
        return self

    def cal_rate(self, tcname):
        if self[tcname]['sum'] == 0:
            self[tcname]['rate'] = 0
        else:
            self[tcname]['rate'] = (self[tcname]['pass'] + 0.0) / self[tcname]['sum']
        return self[tcname]['rate']

    # TODO: implement case granularity first.
    def plot_barchart_rate(self, *args, **kwargs):
        self.get_barchart_rate(*args, **kwargs).plot()

    def get_barchart_rate(self, title='CIStat', sub_title='Bar chart on pass rate'):
        tcnames = self.case_dict.keys()
        chart = Echart(title, sub_title)
        rates = [self.get_case(x)['rate'] for x in tcnames]
        chart.use(Bar('Pass Rate', rates))
        chart.use(Legend(['Pass Rate']))
        chart.use(Axis('category', 'bottom', data=map(Xunitrpt.get_case_shortname, tcnames)))
        return chart

    def get_class_rpt(self):
        """ Generate Class level statistics in Xunitrpt type.
        :return: Xunitrpt object on classes
        """
        clsrpt = Xunitrpt()
        for k, v in self:
            clsrpt += {Xunitrpt.get_class_name(k): v}.iteritems()

        return clsrpt
