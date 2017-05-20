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

LOG_LEVEL = dict(
        DEBUG=logging.DEBUG,
        INFO=logging.INFO,
        WARNING=logging.WARNING,
        ERROR=logging.ERROR,
        CRITICAL=logging.CRITICAL,
)


# TODO: file handler and exception processing
# TODO: Set to NullHandler and move config to ~/.cistat/log.yaml
class Logger(object):
    def __init__(self, name=None, log_level="INFO"):
        self.name = name
        self._logger = logging.getLogger(name)
        logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
        _logger = logging.getLogger(name)
        _logger.setLevel(LOG_LEVEL.get(log_level, logging.INFO))

    def get_logger(self):
        return self._logger

if __name__ == "__main__":
    pass

# EOF
