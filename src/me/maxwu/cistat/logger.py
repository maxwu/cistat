#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logger Class
 Simple encapsulation on logging functions.
 - Console printing
 - File handler and the mapping for multithreading file handlers are under design yet.

 .. moduleauthor:: Max Wu <http://maxwu.me>
 .. References::
    **ReadtheDocs**: https://pythonguidecn.readthedocs.io/zh/latest/writing/logging.html
"""
import logging


# TODO: file handler and exception processing
# TODO: Set to NullHandler and move config to ~/.cistat/log.yaml
class Logger(object):
    def __init__(self, name=None, log_level=logging.INFO):
        self._logger = logging.getLogger(name)
        logging.basicConfig(format='%(asctime) [%(levelname)s]: %(message)s')
        _logger = logging.getLogger(name)
        _logger.setLevel(log_level)

    def get_logger(self):
        return self._logger

if __name__ == "__main__":
    pass

# EOF
