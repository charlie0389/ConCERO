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
Created on Feb 06 10:56:13 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import os
import unittest
import shutil

import concero.conf
import concero.main
import concero.scenario as sn
from concero.tests.data_tools import DefaultTestCase


class TestMain(DefaultTestCase):
    '''Tests Scenario-related methods.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_normal_run(self):

        src = concero.conf.find_file("dummy_model.py")
        shutil.copy2(src, "dummy_model_run.py")

        scen_file = os.path.abspath(TestMain._dd + "test_scenarios.yaml")

        concero.main.run(scen_file)

        # Clean up...
        os.remove('test_scen_outputs.har')
        os.remove('test_model_input.har')
        os.remove('test_model_output.har')
        os.remove('A1_001_step_00.xlsx')
        os.remove("dummy_model_run.py")

    def test_fake_run(self):
        scen_file = os.path.abspath(TestMain._dd + "test_scenarios.yaml")

        concero.main.run(scen_file, fake_run=True)

        concero.main.run(scen_file, fake_run=True)

        # TODO: Come up with more thorough way of checking the scenario hasn't run

    def test_check(self):
        scen_file = os.path.abspath(TestMain._dd + "test_scenarios.yaml")

        concero.main.run(scen_file, fake_run=True)

        concero.main.run(scen_file, check=True)

        # TODO: Come up with more thorough way of checking that checks have occured

if __name__ == '__main__':
    unittest.main()
