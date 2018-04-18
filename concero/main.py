"""
Created on Feb 05 10:42:27 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
script_run = True if __name__ == "__main__" else False
# __name__ = "concero.main"

import os
import sys
import argparse as ap

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

if script_run:

    argpar = ap.ArgumentParser(prog="concero",
             description="Run a scenario with ConCERO.")
    argpar.add_argument('scenario', type=str, #nargs=1,
                        help="The file that contains the scenario definition.")
    argpar.add_argument("-s", '--scenarios_set', #nargs=1,
                        help="The file that contains the scenario set definition.")
    argpar.add_argument("-l", '--log_level', type=str,
                        choices=["DEBUG", "INFO", "WARNING","ERROR", "CRITICAL"],
                        default="WARNING",
                        help="The debug level. 'WARNING' by default.")
    argpar.add_argument("-d", "--log_directory", type=str,
                        default=os.getcwd(),
                        help="The directory to store log files."
                        )
    argpar.add_argument("-f", "--fake_run", action="store_true",
                        help="Perform checks only. If this option is provided, the scenario is not " +
                             "run - instead, static checks of the configuration are performed, and as many runtime " +
                             "checks as possible. Success " +
                             "does not guarantee successful execution of the entire scenario.")
    argpar.add_argument("-c", "--check", action="store_true",
                        help="Perform static checks and runtime checks before running the scenario. Success " +
                             "does not guarantee successful execution of the entire scenario.")
    argpar.add_argument("-r", "--restrain_exceptions", action="store_true",
                        help="By default, exceptions are raised if a check is failed. If this option is provided, " +
                             "False is returned instead (and no exceptions are raised).")

    ns = vars(argpar.parse_args(sys.argv[1:]))

    run(**ns)


