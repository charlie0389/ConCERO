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