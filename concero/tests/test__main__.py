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
Created on Jun 15 10:40:59 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import unittest
import shutil

import concero.conf
import concero.__main__
from concero.tests.data_tools import DefaultTestCase


class Test_Main_(DefaultTestCase):
    '''Tests __main__ methods.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_convert(self):

        concero.__main__.launch(args=["convert", Test_Main_._dd + "test_import_data.yaml", Test_Main_._dd + "test_export_data.yaml"])

        self.assertTrue(os.path.isfile("test_export_data.xlsx"))

        # Clean up...
        os.remove('test_export_data.xlsx')

    def test_convert2(self):

        concero.__main__.launch(args=["co", Test_Main_._dd + "test_import_data.yaml", Test_Main_._dd + "test_export_data.yaml"])

        self.assertTrue(os.path.isfile("test_export_data.xlsx"))

        # Clean up...
        os.remove('test_export_data.xlsx')

    def test_run(self):

        concero.__main__.launch(
            args=["run", Test_Main_._dd + "test_scenario_without_models.yaml"])

        self.assertTrue(os.path.isfile("test_export_data.xlsx"))

        os.remove('test_export_data.xlsx')

    # def test_log_directory(self):
    #
    #     #TODO: Complete this test for changing log directory
    #
    #     ld = "_test_log_dir"
    #
    #     src = concero.conf.find_file("dummy_model.py")
    #     shutil.copy2(src, "dummy_model_run.py")
    #
    #     scen_file = os.path.abspath(Test_Main_._dd + "test_scenarios.yaml")
    #
    #     ld = os.path.join(os.path.abspath(os.getcwd()), ld)
    #     concero.__main__.launch(["run", "--log_directory", ld, scen_file])
    #
    #     # Check log files have been generated
    #     def_log_dir = "ConCERO_logs"
    #     for log_file in ["concero.from_cero.log", "concero.libfuncs_wrappers.log", "concero.model.log", "concero.modfuncs.log", \
    #             "concero.scenario.log", "concero.to_cero.log"]:
    #         try:
    #             self.assertTrue(os.path.exists(os.path.join(ld, def_log_dir, log_file)))
    #         except AssertionError as e:
    #             print("ERROR: File \t\t'%s' does not exist." % os.path.join(ld, def_log_dir, log_file))
    #             print("Log directory is: \t'%s'" % concero.conf.get_logd())
    #             print("concero.name: ", concero.name)
    #             raise e
    #
    #     # Clean up...
    #     os.remove('test_scen_outputs.har')
    #     os.remove('test_model_input.har')
    #     os.remove('test_model_output.har')
    #     os.remove('A1_001_step_00.xlsx')
    #     os.remove("dummy_model_run.py")
    #     os.remove(ld)

if __name__ == '__main__':
    unittest.main()
