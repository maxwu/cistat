#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""UT for class level logic on Xunitrpt
 .. moduleauthor:: Max Wu <http://maxwu.me>
 .. References::
    **None**
"""
import unittest
from me.maxwu.cistat import config
from me.maxwu.cistat.model.xunit_report import Xunitrpt


class TestXunitrptCls(unittest.TestCase):

    def setUp(self):
        with open('/'.join([config.get_root(),
                            'test',
                            'resources',
                            'TEST-org.maxwu.jrefresh.selenium.DriverFactoryTest.xml']
        )) as f:
            xml = f.read()
        self.rptf = Xunitrpt(xunit=xml)

        xunit1 = '''
                     <testsuite tests="2" failures="0" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skipped="0">
                        <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" />
                        <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" />
                    </testsuite>'''
        self.rpts = Xunitrpt(xunit=xunit1)

    def tearDown(self):
        # Nothing to collect for current test
        pass

    def test_class_level(self):
        self.cls_rpts = self.rpts.get_class_rpt()
        self.assertEqual(1, len(self.cls_rpts))
        expected_dict = {
            "org.maxwu.jrefresh.selenium.DriverFactoryTest": {
                "rate": 1.0,
                "pass": 1,
                "fail": 0,
                "skip": 0,
                "sum": 1,
                "time": 0.0
            }
        }
        self.assertDictEqual(expected_dict, self.cls_rpts.get_cases(), "Class level accumulation failed")
        print("**Dump Class Level XUnit Report**\n{}".format(self.cls_rpts.dump()))


if __name__ == '__main__':
    unittest.main()
