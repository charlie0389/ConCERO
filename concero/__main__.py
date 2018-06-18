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
from collections import OrderedDict

import concero
import concero.main

def launch(args=None):

    def run_cmd(**ns):
        concero.main.run(**ns)
    def convert_cmd(**ns):
        tc = concero.ToCERO(ns["import_def"])  # creates the import object (a.k.a. a ``ToCERO`` object)
        cero = tc.create_cero()  # creates a common object (a.k.a. a 'CERO')
        fc = concero.FromCERO(ns["export_def"])  # creates the export object (a.k.a. a ``FromCERO`` object)
        fc.exec_procedures(cero)  # execute the procedures defined in ``export_data.yaml`` on ``cero``
    def version():
        with open(os.path.join(os.path.dirname(__file__), '..', 'VERSION')) as version_file:
            version = version_file.read().strip()
        return "ConCERO v%s" % version

    class _HelpAction(ap._HelpAction):

        def __call__(self, parser, namespace, values, option_string=None):
            parser.print_help()

            # retrieve subparsers from parser
            subparsers_actions = [
                action for action in parser._actions
                if isinstance(action, ap._SubParsersAction)]

            # there will probably only be one subparser_action,
            # but better save than sorry
            for subparsers_action in subparsers_actions:

                cp = OrderedDict()
                # cp ensures no duplicates because of aliases...
                for choice, subparser in subparsers_action.choices.items():
                    choices = cp.setdefault(subparser, [])
                    choices.append(choice)
                    cp[subparser] = choices

                # get all subparsers and print help
                for subparser, choices in cp.items():
                    print("Subcommand: %s" % "|".join(choices))
                    print(subparser.format_help())

            parser.exit()

    if args is None:
        args = sys.argv[1:]

    argp = ap.ArgumentParser(prog="concero",
                             add_help=False,
                             description="A program to automate data format conversion and run (economic) models.")
    argp.add_argument("-h", "--help", action=_HelpAction, help="show this help message and exit")
    argp.add_argument("-v", "--version", action='version', help="Display the version string.", version=version())

    sp = argp.add_subparsers()

    # run command

    argpar = sp.add_parser("run", description="Run a ConCERO scenario.")
    argpar.set_defaults(func=run_cmd)

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

    # convert command

    conpar = sp.add_parser("convert", description="Perform data format conversion.", aliases=["co"])
    conpar.set_defaults(func=convert_cmd)
    conpar.add_argument("import_def", type=str, help="YAML file that defines the import of data from one or more files into a CERO.")
    conpar.add_argument("export_def", type=str, help="YAML file that defines the export of data from a CERO into one or more files.")

    ns = vars(argp.parse_args(args))

    if ns == {}:
        raise RuntimeError("Invalid ConCERO command - please execute 'concero --help' for a description of valid options.")

    ns["func"](**ns)

if __name__ == "__main__":
    launch()