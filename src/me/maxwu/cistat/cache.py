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

    def __init__(self, folder=None, enable=False):
        self.enable = enable
        self.folder = folder

        if not folder:
            # If folder is not specified, use configuration items.
            folder = config.get_cache_path()
            logger.debug("Set cache_dir to {}".format(folder))

        self.cache = Cache(folder, size_limit=CacheIt.cache_size)
        self.cache.stats(enable=True)

    def __del__(self):
        if self.cache:
            self.cache.close()

    def __call__(self, func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if not self.enable:
                logger.debug("Cache is not enabled")
                return func(*args, **kwargs)

            with self.cache:
                if 'url' not in kwargs.keys() or not kwargs.get('url'):
                    # Now make url the only element for cache keys.
                    logger.info("No URL in call {}".format(func.__name__))
                    return func(*args, **kwargs)
                url = kwargs.get('url', '**Empty URL**')
                logger.debug("Cache check on call {} against url {}".format(func.__name__, url))
                fetch = self.cache.get(url.encode("ascii"), default=None, read=True)

                if not fetch:
                    logger.debug("Cache key missing {}".format(url))
                    res = func(*args, **kwargs)
                    if res:
                        logger.debug("caching value from {}".format(url))
                        self.cache.set(url.encode("ascii"), BytesIO(res.encode("ascii")), read=True, expire=CacheIt.cache_expire)
                    else:
                        logger.debug("None value not cached for {}".format(url))
                else:
                    logger.debug("Cache key hit {}".format(url))
                    res = fetch.read()
                if self.get_total() % 10 == 0:
                    logger.info(self.get_stat_str())
                return res
        return wrap

    def get_stat_str(self):
        return "Cache stat: hit=%d, miss=%d" % (self.cache.stats(enable=True))

    def get_total(self):
        (hit, miss) = self.cache.stats()
        return hit + miss