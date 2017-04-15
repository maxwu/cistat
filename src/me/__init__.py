# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'maxwu'


import os

ME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(ME_ROOT_DIR))


def get_root_dir():
    return ROOT_DIR
