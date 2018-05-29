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
