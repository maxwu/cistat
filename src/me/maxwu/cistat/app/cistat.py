#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
from me.maxwu.cistat import config
from me.maxwu.cistat.reqs.circleci_request import CircleCiReq
from me.maxwu.cistat.model.xunit_report import Xunitrpt

"""Entry point of console_cli app for CIstat
"""

VERSION = "0.9.3"


def cli_app():
    # vcs, project, username = config.get_circleci_vcs(), config.get_circleci_project(), config.get_circleci_username()
    vcs, project, username = 'github', 'cistat', 'maxwu'

    urls = CircleCiReq.get_recent_artifacts(
            token=config.get_circleci_token(),
            vcs=vcs,
            project=project,
            username=username
    )

    report = Xunitrpt()

    for artifact in urls:
        print("fetching {}".format(artifact))
        report += Xunitrpt(xunit=CircleCiReq.get_artifact_report(url=artifact))

    print("Top 10 failure cases:")
    pprint.pprint(report.get_cases_in_rate()[:10])

    print("Plot Bar Chart on Pass Rate per Case")
    report.plot_barchart_rate(project, "Pass Rate per Case")

    print("Plot Bar Chart on Pass Rate per Class")
    report.get_class_rpt().plot_barchart_rate(project, "Pass Rate per Class")

    print("Plot Pie Chart on Case Num per Class")
    report.get_class_rpt().plot_piechart_casenum(project, "Case Num per Class")

    print("Plot Bubble Chart on Test ROI per Class")
    report.get_class_rpt().plot_scatter_roi(project, "Test ROI per Class")

if __name__ == '__main__':
    cli_app()
