#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

import unittest
import json
from me.maxwu.cistat.xunit_report import Xunitrpt
from me.maxwu.cistat import config


class TestXunitrpt(unittest.TestCase):

    def test_xunit_from_str_with_4_cases(self):
        with open('/'.join([config.get_root(),
                            'test',
                            'resources',
                            'TEST-org.maxwu.jrefresh.selenium.DriverFactoryTest.xml']
        )) as f:
            xml = f.read()

        cases = Xunitrpt(xunit=xml).get_cases()
        print "Pretty format case dict:\n{}".format(json.dumps(cases, indent=2))

        self.assertEqual(4, len(cases))
        # There are no failure cases in this given sample report.
        self.assertEqual(0, len([case for case in cases if cases[case]['fail']]))

    # TEST-org.maxwu.jrefresh.selenium.TemperatureConverterTest
    def test_xunit_from_str2_with_49_cases(self):
        with open('/'.join([
            config.get_root(),
            'test',
            'resources',
            'TEST-org.maxwu.jrefresh.selenium.TemperatureConverterTest.xml'
        ])) as f:
            xml = f.read()

        cases = Xunitrpt(xunit=xml).get_cases()
        print "Pretty format case dict:\n{}".format(json.dumps(cases, indent=2))

        self.assertEqual(49, len(cases))
        # There are 2 failure cases in this given sample report.
        self.assertEqual(2, len([case for case in cases if cases[case]['fail']]))

    def test_accumulate(self):
        xunit1 = '''
            <testsuite tests="2" failures="0" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skipped="0">
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="3.496"/>
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" time="2.628"/>
            </testsuite>'''

        xunit2 = '''
            <testsuite tests="2" failures="1" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skipped="0">
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="3.496"/>
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" time="2.628">
                    <failure message="Faked"/>
                </testcase>
            </testsuite>'''

        cases = Xunitrpt()
        print("Empty xunit report: {}".format(cases))
        self.assertEquals(len(cases.get_cases()), 0)

        cases.accumulate_xunit(xunit1).accumulate_xunit(xunit2)
        print("Cascaded xunit report: {}".format(cases))
        self.assertEquals(cases.get_case('org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverTest')['fail'], 1)
        self.assertEquals(cases.get_case('org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverTest')['pass'], 1)
        self.assertEquals(cases.get_case('org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverReEntryTest')['fail'], 0)
        self.assertEquals(cases.get_case('org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverReEntryTest')['pass'], 2)

        cases_in_rate = cases.get_cases_in_rate()
        print("Cases in rate: {}".format(json.dumps(cases_in_rate, indent=2)))
        expected = [
            (
                "org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverTest",
                {
                    "fail": 1,
                    "sum": 2,
                    "skipped": 0,
                    "rate": 0.5,
                    "pass": 1
                }
            ),
            (
                "org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverReEntryTest",
                {
                    "fail": 0,
                    "sum": 2,
                    "skipped": 0,
                    "rate": 1.0,
                    "pass": 2
                }
            )]
        self.assertListEqual(cases_in_rate, expected)

if __name__ == '__main__':
    unittest.main()
