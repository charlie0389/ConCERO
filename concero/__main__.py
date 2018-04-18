"""
Created on Apr 18 13:28:44 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import sys
import os
import argparse as ap

import concero.main

def launch(args=None):

    if args is None:
        args = sys.argv[1:]

    argpar = ap.ArgumentParser(prog="concero",
                               description="Run a scenario with ConCERO.")
    argpar.add_argument('scenario', type=str,  # nargs=1,
                        help="The file that contains the scenario definition.")
    argpar.add_argument("-s", '--scenarios_set',  # nargs=1,
                        help="The file that contains the scenario set definition.")
    argpar.add_argument("-l", '--log_level', type=str,
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
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

    ns = vars(argpar.parse_args(args))

    concero.main.run(**ns)

if __name__ == "__main__":
    launch()