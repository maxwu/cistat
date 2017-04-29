#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__author__ = 'maxwu'

ME_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(ME_ROOT_DIR))


def get_root_dir():
    return ROOT_DIR


