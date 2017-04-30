#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

import json
import unittest
import operator
from me.maxwu.cistat import config
from me.maxwu.cistat.stats.xunit_report import Xunitrpt


class TestXunitrpt(unittest.TestCase):

    def test_xunit_from_str_with_4_cases(self):
        with open('/'.join([config.get_root(),
                            'test',
                            'resources',
                            'TEST-org.maxwu.jrefresh.selenium.DriverFactoryTest.xml']
        )) as f:
            xml = f.read()

        cases = Xunitrpt(xunit=xml).get_cases()
        print "\nPretty format case dict:\n{}".format(json.dumps(cases, indent=2))

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

    def test_accumulate_wo_time(self):
        xunit1 = '''
            <testsuite tests="2" failures="0" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skipped="0">
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" />
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" />
            </testsuite>'''

        xunit2 = '''
            <testsuite tests="2" failures="1" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skipped="0">
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" />
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" >
                    <failure message="Faked"/>
                </testcase>
            </testsuite>'''

        cases = Xunitrpt()
        print("Empty xunit report: {}".format(cases))
        self.assertEquals(len(cases.get_cases()), 0)

        cases.accumulate_xunit_str(xunit1).accumulate_xunit_str(xunit2)
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
                    "skip": 0,
                    "rate": 0.5,
                    "pass": 1,
                    "time": 0
                }
            ),
            (
                "org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverReEntryTest",
                {
                    "fail": 0,
                    "sum": 2,
                    "skip": 0,
                    "rate": 1.0,
                    "pass": 2,
                    "time": 0
                }
            )]
        self.assertListEqual(cases_in_rate, expected)

    def test_accumulate_wi_time(self):
        str1 = '''
            <testsuite tests="2" failures="0" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skipped="0">
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="3.0"/>
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" time="2"/>
            </testsuite>'''

        str2 = '''
            <testsuite tests="2" failures="1" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skipped="0">
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="3.5"/>
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" time="1">
                    <failure message="Faked"/>
                </testcase>
            </testsuite>'''

        cases = Xunitrpt()
        print("Empty xunit report: {}".format(cases))
        self.assertEquals(len(cases.get_cases()), 0)

        cases.accumulate_xunit_str(str1).accumulate_xunit_str(str2)
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
                    "skip": 0,
                    "rate": 0.5,
                    "pass": 1,
                    "time": 3
                }
            ),
            (
                "org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverReEntryTest",
                {
                    "fail": 0,
                    "sum": 2,
                    "skip": 0,
                    "rate": 1.0,
                    "pass": 2,
                    "time": 6.5
                }
            )]
        self.assertListEqual(cases_in_rate, expected)

    def test_add_wi_time(self):
        xunit1 = '''
            <testsuite tests="2" failures="0" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skip="0">
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="3.0"/>
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" time="2"/>
            </testsuite>'''

        xunit2 = '''
            <testsuite tests="2" failures="1" name="org.maxwu.jrefresh.selenium.DriverFactoryTest" time="21.377" errors="0" skip="0">
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="3.5"/>
                <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" time="1">
                    <failure message="Faked"/>
                </testcase>
            </testsuite>'''

        cases = Xunitrpt()
        print("Empty xunit report: {}".format(cases))
        self.assertEquals(len(cases.get_cases()), 0)

        cases= Xunitrpt(xunit1) + Xunitrpt(xunit2)
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
                    "skip": 0,
                    "rate": 0.5,
                    "pass": 1,
                    "time": 3
                }
            ),
            (
                "org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverReEntryTest",
                {
                    "fail": 0,
                    "sum": 2,
                    "skip": 0,
                    "rate": 1.0,
                    "pass": 2,
                    "time": 6.5
                }
            )]
        self.assertListEqual(cases_in_rate, expected)

    def test_tc_shortname(self):
        tcname1 = "org.maxwu.jrefresh.selenium.DriverFactoryTest.quitDriverReEntryTest"
        tcshort1 = Xunitrpt.get_case_shortname(tcname1)
        self.assertEquals(tcshort1, '+tDriverReEntryTest')

        tcname2 = "quitDriverReEntryTest"
        tcshort2 = Xunitrpt.get_case_shortname(tcname2)
        self.assertEquals(tcshort2, '+tDriverReEntryTest')

        tcname3 = "3.quitTest"
        tcshort3 = Xunitrpt.get_case_shortname(tcname3)
        self.assertEquals(tcshort3, '3.quitTest')

    def test_barchart_rate(self):
        xunit_strs = ['''
        <testsuite >
          <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="3.496"/>
          <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverTest" time="2.628"/>
          <testcase classname="org.maxwu.jrefresh.selenium.Driver" name="getDriverTest" time="3.507"/>
          <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="navigateWeb" time="11.746"/>
        </testsuite>
        ''',
        '''
            <testsuite >
              <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="3.496">
                <failure message="Faked" type="org.junit.ComparisonFailure"> 
                    This is faked case
                </failure>
              </testcase>
              <testcase classname="org.maxwu.jrefresh.selenium.Driver" name="quitHook" time="2.628"/>
            </testsuite>
        ''',
        '''
            <testsuite >
              <testcase classname="org.maxwu.jrefresh.selenium.DriverFactoryTest" name="quitDriverReEntryTest" time="5">
                <failure message="Faked" type="org.junit.ComparisonFailure"> 
                    This is faked case
                </failure>
              </testcase>
              <testcase classname="org.maxwu.jrefresh.selenium.Driver" name="quitHook" time="2.628"/>
              <testcase classname="org.maxwu.jrefresh.selenium.Driver" name="getDriverTest" time="3.507">
              <failure message="Faked" type="org.junit.ComparisonFailure"> 
                    This is faked case
                </failure>
              </testcase>
            </testsuite>
        ''']
        report = reduce(operator.add, [Xunitrpt(xunit=x) for x in xunit_strs])
        print("**Dump XUnit Sum Stat:**\n{}".format(report.dump()))
        report.plot_barchart_rate()

if __name__ == '__main__':
    unittest.main()
