#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Decorator to serve dick cache for artifacts.

http://www.grantjenks.com/docs/diskcache/tutorial.html
cache = Cache('/tmp/mycachedir', tag_index=False)
"""

from functools import wraps
from io import BytesIO

from diskcache import Cache
from cistat import config
from cistat.logger import Logger

logger = Logger(name=__name__).get_logger()
# logger.setLevel(LOG_LEVEL['DEBUG'])


class CacheIt(object):
    cache_expire = 3600*24  # 24hr
    cache_size = 2**25      # 32MB

    def __init__(self, folder=None, enable=False, name=None):
        self.enable = enable
        self.name = name if name else 'Default'
        if not folder:
            folder = config.get_cache_path()
        self.folder = folder
        logger.debug("Set cache {} dir to {}".format(self.name, folder))

        # Disk cache requests each thread/process to create its own cache dir and instance.
        # Either a pool of [0~n] cache folders or a messaging queue will be added for concurrency.
        self.cache = Cache(folder, size_limit=CacheIt.cache_size)
        self.cache.stats(enable=True)

    def close(self):
        if self.cache:
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
        :param key: str type key, e.g. url
        :param value: str type value, e.g. file content
        :return: True if set value successfully, otherwise False
        """
        try:
            self.cache.set(key.encode("ascii"), BytesIO(value.encode("ascii")), read=True, expire=CacheIt.cache_expire)
        except UnicodeEncodeError as uee:
            logger.error("Artifact is not compliant with ascii range(128), {}".format(uee))
            return False
        except:
            return False
        else:
            return True

    def __call__(self, func):
        """
        Here it is assumed all URLs are for "GET" request, AKA. Safe and Idempotent operation.
        :param func: The method to instrument with cache
        :return: Wrapped method with cache
        """
        @wraps(func)
        def wrap(*args, **kwargs):
            if not self.enable:
                logger.debug("Cache is not enabled")
                return func(*args, **kwargs)

            with self.cache:
                if 'url' not in kwargs.keys() or not kwargs.get('url'):
                    # Now make url the only element for cache keys.
                    logger.warn("No URL in call {}".format(func.__name__))
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
                    logger.info(self.get_stat_str())
                return res
        return wrap

    def get_stat_str(self):
        (hit, miss) = self.cache.stats(enable=True)
        return "Cache stat: total={:d}, hit={:d}, miss={:d}".format(hit+miss, hit, miss)

    def get_total(self):
        return sum(self.cache.stats())
