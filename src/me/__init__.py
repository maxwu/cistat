# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'maxwu'


import os

ORG_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(ORG_ROOT_DIR))


def get_root_dir():
    return ROOT_DIR
