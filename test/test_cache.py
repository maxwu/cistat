#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cache regression test, designed for apache disk-cache decorator.
 .. moduleauthor:: Max Wu <http://maxwu.me>
"""
import unittest
from me.maxwu.cistat.cache import CacheIt
from me.maxwu.cistat import config
from me.maxwu.cistat.reqs.circleci_request import CircleCiReq


def get_cache_stat():
    dc = CacheIt(enable=config.get_cache_enable())
    hit, miss = dc.cache.stats()
    dc.close()
    print(">>>Test>>> Cache Stat: hit={:d} miss={:d}".format(hit, miss))
    return hit, miss

class MyTestCase(unittest.TestCase):
    """ We assume Apache disk cache will keep hot data local.
    Therefore, even in ultimate case of size limit exceeded, the LRF or LRU won't move the item just being called.
    """
    def setUp(self):
        self.hit_orig, self.miss_orig = get_cache_stat()
        self.url = 'https://80-77958022-gh.circle-artifacts.com/0/tmp/circle-junit.BxjS188/junit/TEST-org.maxwu.jrefresh.HttpApi.SourceIpApiTest.xml'

    def test_cache_stat(self):
        hit_0, miss_0 = get_cache_stat()
        xunit1 = CircleCiReq.get_artifact_report(url=self.url)
        hit_1, miss_1 = get_cache_stat()
        self.assertEqual(1, hit_1 + miss_1 - hit_0 - miss_0)

        xunit2 = CircleCiReq.get_artifact_report(url=self.url)
        hit_2, miss_2 = get_cache_stat()
        self.assertEqual(miss_2, miss_1)   # For the 2nd fetch, it won't be missed.
        self.assertEqual(1, hit_2 - hit_1) # For the 2nd fetch, it shall hit at least once

    def test_cache_stat(self):
        hit_0, miss_0 = get_cache_stat()
        xunit1 = CircleCiReq.get_artifact_report()  # No url provided
        hit_1, miss_1 = get_cache_stat()
        self.assertEqual((hit_0, miss_0), (hit_1, miss_1))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
