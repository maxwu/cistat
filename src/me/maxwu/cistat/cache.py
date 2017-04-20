#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

from diskcache import Cache

"""
Decorator to serve dick cache for artifacts.

http://www.grantjenks.com/docs/diskcache/tutorial.html
cache = Cache('/tmp/mycachedir', tag_index=True)
"""


def disk_cache(func):

	def cached_request(*args):
		if args in cache:
			print('func {} is already cached with arguments {}'.format(
				func.__name__, args))
			return cache[args]
		else:
			print('func {} is not cached with arguments {}'.format(
				func.__name__, args))
			res = func(*args)
			cache[args] = res
			return res
	return inner_deco