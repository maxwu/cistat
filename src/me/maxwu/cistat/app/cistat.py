#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

import json

from me.maxwu.cistat import config
from me.maxwu.cistat.reqs.circleci_request import CircleCiReq
from me.maxwu.cistat.stats.xunit_report import Xunitrpt

"""Main script file to provide configuration loading, cli_app and version.
"""

VERSION = "1.0"


def cli_app():
    vcs, project, username = config.get_circleci_vcs(), config.get_circleci_project(), config.get_circleci_username()

    urls =CircleCiReq.get_recent_artifacts(
            token=config.get_circleci_token(),
            vcs=vcs,
            project=project,
            username=username
    )

    report = Xunitrpt()

    for artifact in urls:
        print("fetching {}".format(artifact))
        report += Xunitrpt(xunit=CircleCiReq.get_artifact_report(url=artifact))

    print("Top 10 failure cases: {}".format(report.get_cases_in_rate()[:10]))

    print("Plot Barchart of Pass Rate")
    report.plot_barchart_rate(project, "Pass Rate per case")


if __name__ == '__main__':
    cli_app()
