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

import numpy as np
import harpy

import concero.conf
import concero.scenario as sn
from concero.tests.data_tools import DefaultTestCase


class TestScenario(DefaultTestCase):
    '''Tests Scenario-related methods.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_scenario_run(self):
        '''Tests a scenario run.'''

        src = concero.conf.find_file("dummy_model.py")
        shutil.copy2(src, "dummy_model_run.py")

        # Load Scenario(s)
        scen_file = TestScenario._dd + "test_scenarios.yaml"
        scens = sn.Scenario.load_scenario(scen_file)

        # Run the scenario
        scens.run()

        har = harpy.HarFileObj.loadFromDisk(filename='test_scen_outputs.har')

        self.assertEqual(har.getHeaderArrayNames(), ["CAPS"])

        caps = har.getHeaderArrayObj("CAPS")

        self.assertEqual([s["name"] for s in caps["sets"]], ["IND_TYPE", "REGIONS", "TIME"])

        ct_lst = ["SheepCattle", "DairyCattle", "OtherAnimals"]
        self.assertEqual(caps.getSet("IND_TYPE")["dim_desc"], ct_lst)

        rg_lst = ["NSW", "VIC"]
        self.assertEqual(caps.getSet("REGIONS")["dim_desc"], rg_lst)

        self.assertEqual(caps.getSet("TIME")["dim_desc"], ["Y2017"])

        self.assertTrue(np.isclose(5557.53515625, caps["array"][0, 0, 0]))
        self.assertTrue(np.isclose(6572.65625000, caps["array"][0, 1, 0]))
        self.assertTrue(np.isclose(1025.20568848, caps["array"][1, 0, 0]))
        self.assertTrue(np.isclose(5799.52001953, caps["array"][1, 1, 0]))

        # Clean up...
        os.remove('test_scen_outputs.har')
        os.remove('test_model_input.har')
        os.remove('test_model_output.har')
        os.remove('A1_001_step_00.xlsx')
        os.remove("dummy_model_run.py")

    def test_scenario_without_conf(self):

        src = concero.conf.find_file("scenario_without_conf.py")
        shutil.copy2(src, "scenario_without_conf.py")

        # Load Scenario(s)
        scens = {"name": "test_scenario_without_conf",
                 "run_no": 1,
                 "export_mod_xlsx": False,
                 "export_int_xlsx": False,
                 "models": [{"name": "test_model",
                             "cmds": "python scenario_without_conf.py",
                             "export_mod_xlsx": False}]}
        scens = sn.Scenario.load_scenario(scens)

        # Run the scenario
        scens.run()

        try:
            open("scenario_without_conf.txt")
        except FileNotFoundError:
            self.fail("File that should of been generated, hasn't.")

        os.remove("scenario_without_conf.txt")
        os.remove("scenario_without_conf.py")


if __name__ == '__main__':
    unittest.main()
