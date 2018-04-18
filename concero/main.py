"""
Created on Feb 05 10:42:27 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os

import concero.conf as conf
from concero.scenario import ScenariosSet, Scenario

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

    _pd = os.path.dirname(__file__) + os.sep  # parent directory
    # Load ScenariosSet (used to check a Scenario definition is valid)
    if ns.get("scenarios_set"):
        ss = ScenariosSet(scen_defs=ns["scenarios_set"])
    else:
        ss = None

    # Load Scenario(s)
    scens = Scenario.load_scenarios(ns["scenario"], scenarios_set=ss)

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
