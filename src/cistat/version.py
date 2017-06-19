#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cistat version

 .. moduleauthor:: Max Wu <http://maxwu.me>
"""
import re

VERSION = '0.93.dev20170619'


def get_version(naked=False):
    if naked:
        return re.split('(a|b|rc|.dev)', VERSION)[0]
    return VERSION


if __name__ == "__main__":
    pass
