#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""reqs: The package to hold all RESTful request models.
  
 1. Only circleci APIs are implemented so far till version 0.92
 2. The RESTful call is no compliant to HATEOAS. 
    Next pre-rev version will start from the HATEOAS engine entry point and leave the backend freedom of operation concrete APIs.
 
 ..moduleauthor:: Max Wu < http: // maxwu.me >
"""
from cistat.reqs.circleci_request import *
