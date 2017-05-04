#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'


from functools import wraps
from io import BytesIO
from diskcache import Cache
from me.maxwu.cistat import config
from me.maxwu.cistat.logger import Logger

logger = Logger(name=__name__).get_logger()

"""
Decorator to serve dick cache for artifacts.

http://www.grantjenks.com/docs/diskcache/tutorial.html
cache = Cache('/tmp/mycachedir', tag_index=False)
"""


class CacheIt(object):
    cache_expire = 3600*24  # 24hr
    cache_size = 2**22      # 100MB
    stat = dict(
        hit=0,
        miss=0,
        total=0
    )

    @classmethod
    def __add_hit(cls):
        cls.stat['hit'] += 1
        cls.stat['total'] += 1

    @classmethod
    def __add_miss(cls):
        cls.stat['miss'] += 1
        cls.stat['total'] += 1

    def __init__(self, folder=None, enable=False, *args, **kwargs):
        self.enable = enable

        if not folder:
            # If folder is not specified, use configuration items.
            folder = config.get_cache_path()
            logger.debug("Set cache_dir to {}".format(folder))

        self.cache = Cache(folder, size_limit=CacheIt.cache_size, *args, **kwargs)

    def __call__(self, func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if not self.enable:
                logger.debug("Cache is not enabled")
                return func(*args, **kwargs)

            if 'url' not in kwargs.keys() or not kwargs.get('url'):
                # Now make url the only element for cache keys.
                logger.info("No URL in call {}".format(func.__name__))
                return func(*args, **kwargs)

            logger.debug("Cache check on call {} against url {}".format(func.__name__, kwargs['url']))
            fetch = self.cache.get(kwargs['url'], default=None)

            if not fetch:
                logger.debug("Cache key missing {}".format(kwargs.get('url', '**Empty URL**')))
                CacheIt.__add_miss()
                res = func(*args, **kwargs)
                if res:
                    logger.debug("caching value from {}".format(kwargs.get('url', '**Empty URL**')))
                    self.cache.set([kwargs['url']], BytesIO(res.encode("ascii")), expire=CacheIt.cache_expire)
                else:
                    logger.debug("None value not cached for {}".format(kwargs.get('url', '**Empty URL**')))
            else:
                logger.debug("Cache key hit {}".format(kwargs.get('url', '**Empty URL**')))
                CacheIt.__add_hit()
                res = unicode(fetch, "ascii")
            if CacheIt.stat.get('total', 0) % 10 == 0:
                print("Cache stat: total={}, hit={}".format(CacheIt.stat.get('total', 0), CacheIt.stat.get('hit', 0)))
                logger.info("Cache stat: total=%d, hit=%d" % (CacheIt.stat.get('total', 0), CacheIt.stat.get('hit', 0)))
            return res

        return wrap
