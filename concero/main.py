#      ConCERO - a program to automate data format conversion and the execution of economic modelling software.
#      Copyright (C) 2018  CSIRO Energy Business Unit
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Created on Feb 05 10:42:27 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os

import concero.conf as conf
from concero.scenario import Scenario

def run(scenario, **kwargs):

    ns = {"log_level": "WARNING",
          "log_directory": os.getcwd(),
          "scenario": os.path.abspath(scenario), # scenario is received relative to CWD
          "fake_run": False,
          "check": False,
          "restrain_exceptions": False,
          }

    ns.update(kwargs)
    conf.set_log_level(ns["log_level"])
    conf.set_logd(ns["log_directory"])

    # Load Scenario(s)
    scens = Scenario.load_scenarios(ns["scenario"])

    if ns["fake_run"] or ns["check"]:
        for sc in scens:
            if not sc.is_valid(raise_exception=(not ns["restrain_exceptions"])):
                return False
            if not sc.run_checks(raise_exception=(not ns["restrain_exceptions"])):
                return False

    if not ns["fake_run"]:

        for sc in scens:
            # Run one or more scenarios
            print("Running scenario %s..." % sc.get_name())
            sc.run()
            print("Scenario run complete.")
