"""
Created on Feb 06 10:56:13 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import os
import unittest
import shutil

import numpy as np

import ConCERO.conf
import ConCERO.scenario as sn
from ConCERO.tests.data_tools import DataTools, DefaultTestCase


class TestScenario(DefaultTestCase):
    '''Tests Scenario-related methods.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_scenario_run(self):
        '''Tests a scenario run.'''

        src = ConCERO.conf.find_file("dummy_model.py")
        shutil.copy2(src, "dummy_model_run.py")

        ssf = TestScenario._dd + "test_scenario_set.yaml"
        ss = sn.ScenariosSet(scen_defs=ssf)

        # Load Scenario(s)
        scen_file = TestScenario._dd + "test_scenarios.yaml"
        scens = sn.Scenario.load_scenario(scen_file, scenarios_set=ss)

        # Run the scenario
        scens.run()

        har = DataTools.get_test_data('test_scen_outputs.har')

        self.assertEqual(har.getHeaderArrayNames(), ["CAPS"])

        caps = har.getHeaderArrayObj("CAPS")

        self.assertEqual([s["name"] for s in caps["sets"]], ["IND_TYPE", "REGIONS", "TIME"])
        # self.assertEqual(caps.SetNames, ["IND_TYPE", "REGIONS", "TIME"])

        ct_lst = ["SheepCattle", "DairyCattle", "OtherAnimals"]
        self.assertEqual(caps.getSet("IND_TYPE")["dim_desc"], ct_lst)
        # self.assertEqual(caps.SetElements["IND_TYPE"], ct_lst)

        rg_lst = ["NSW", "VIC"]
        self.assertEqual(caps.getSet("REGIONS")["dim_desc"], rg_lst)
        # self.assertEqual(caps.SetElements["REGIONS"], rg_lst)

        self.assertEqual(caps.getSet("TIME")["dim_desc"], ["Y2017"])
        # self.assertEqual(caps.SetElements["TIME"], ["Y2017"])

        self.assertTrue(np.isclose(5557.53515625, caps["array"][0, 0, 0]))
        self.assertTrue(np.isclose(6572.65625000, caps["array"][0, 1, 0]))
        self.assertTrue(np.isclose(1025.20568848, caps["array"][1, 0, 0]))
        self.assertTrue(np.isclose(5799.52001953, caps["array"][1, 1, 0]))

        # Clean up...
        os.remove('test_scen_outputs.har')
        os.remove('test_model_input.har')
        os.remove('test_model_output.har')
        os.remove('A1_P_IMRLELSLWEC_PXRLDLLLHLR_GHPETMAMEFB_GOTOSOHOCOG_IPPMMHGHWXCX_001_step_00.xlsx')
        os.remove("dummy_model_run.py")


if __name__ == '__main__':
    unittest.main()
