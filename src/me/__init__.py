#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Package me.maxwu for all shared codes
http://maxwu.me

"""
import os

ME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(ME_ROOT_DIR))


def get_root_dir():
    return ROOT_DIR
