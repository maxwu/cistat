#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Decorator to serve dick cache for artifacts.

http://www.grantjenks.com/docs/diskcache/tutorial.html
cache = Cache('/tmp/mycachedir', tag_index=False)
"""

from io import BytesIO
from diskcache import Cache
from cistat import config
from cistat.logger import Logger, LOG_LEVEL

logger = Logger(name=__name__).get_logger()
# logger.setLevel(LOG_LEVEL['DEBUG'])


class CacheIt(object):
    cache_expire = 3600*24*14   # 2 weeks
    cache_size = 2**25          # 32MB
    caches = []

    def __init__(self, func):
        self.enable = config.get_cache_enable()
        self.func = func
        self.name = func.__name__
        self.folder = config.get_cache_path()
        logger.debug("Set cache {} dir to {}".format(self.name, self.folder))

        # Disk cache requests each thread/process to create its own cache dir and instance.
        # Either a pool of [0~n] cache folders or a messaging queue will be added for concurrency.
        self.cache = Cache(self.folder, size_limit=CacheIt.cache_size)
        self.cache.stats(enable=True)
        CacheIt.caches.append(self)

    @classmethod
    def get_caches(cls):
        return cls.caches

    @classmethod
    def get_caches_stat_str(cls):
        res = []
        for s in cls.get_caches():
            res.append("cache report - 🏘 {} | 🏗 {}".format(s.name, s.get_stat_str()))
        return "\n".join(res)

    def close(self):
        if self.cache:
            self.enable = False
            self.cache.close()

    def __del__(self):
        self.close()
        logger.debug("Cache {} closed-".format(self.name))
        logger.debug(self.get_stat_str())

    def __getitem__(self, item):
        fetch = self.cache.get(item.encode("ascii"), default=None, read=True)
        return fetch.read() if fetch else None

    def __setitem__(self, key, value):
        """
        Set cached item to cache instance.
        :param key: str type key, e.g. url, key must be ascii coded str
        :param value: str type value, e.g. file content
        :return: True if set value successfully, otherwise False
        """
        try:
            self.cache.set(key.encode("ascii"), BytesIO(value.encode("ascii")), read=True, expire=CacheIt.cache_expire)
        except UnicodeEncodeError as uee:
            logger.error("Artifact is not compliant with ascii range(128), {}".format(uee))
            return False
        except IOError:
            return False
        else:
            return True

    def __call__(self, *args, **kwargs):
        """
        Here it is assumed all URLs are for "GET" request, AKA. Safe and Idempotent operation.
        :param func: The method to instrument with cache
        :return: Wrapped method with cache
        """

        func = self.func

        if not self.enable:
            logger.debug("Cache is not enabled")
            return func(*args, **kwargs)

        with self.cache:
            if 'url' not in kwargs.keys() or not kwargs.get('url'):
                # Now make url the only element for cache keys.
                logger.warn("No URL in call {}".format(func.__name__))
                return func(*args, **kwargs)

            cache_ind = kwargs.pop('cache', True)
            method_is_get = kwargs.get('method', 'GET').upper() == 'GET'
            if not cache_ind or not method_is_get:
                logger.debug("Intend not to cache {}, cache flag is {} and test if method is GET gets {}"
                             .format(func.__name__, cache_ind, method_is_get))
                return func(*args, **kwargs)

            url = kwargs.get('url', '**Empty URL**')
            fetch = self[url]

            if not fetch:
                logger.debug("Cache key missing {}".format(url))
                res = func(*args, **kwargs)
                if res:
                    logger.debug("caching value from {}".format(url))
                    self[url] = res
                else:
                    logger.debug("None value not cached for {}".format(url))
            else:
                logger.debug("Cache key hit {}".format(url))
                res = fetch

            if self.get_total() % 10 == 0:
                logger.debug(CacheIt.get_caches_stat_str())
            return res


    def get_stat_str(self):
        (hit, miss) = self.cache.stats(enable=True)
        return "total={:d}, hit={:d}, miss={:d}".format(hit+miss, hit, miss)

    def get_total(self):
        return sum(self.cache.stats())
