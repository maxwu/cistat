#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CIstat: Python package to fetch and analyze CI data.

 ..moduleauthor:: Max Wu < http: // maxwu.me >
 .. References::
    **Blog**: http://maxwu.me/2017/05/12/CIstat-preview-version-released/
"""
import os

VERSION = "0.92"
ME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(ME_ROOT_DIR))


def get_root_dir():
    return ROOT_DIR
