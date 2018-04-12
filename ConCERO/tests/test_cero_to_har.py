"""
Created on Jan 23 08:29:29 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
script_run = True if __name__ == "__main__" else False
__name__ = "ConCERO.tests.test_cero_to_har"

import os
import unittest
import numpy as np
import shutil

from ConCERO.from_cero import FromCERO
from ConCERO.tests.data_tools import DataTools


class TestCERO2HAR(unittest.TestCase):
    '''Test the CERO to HAR conversion.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_cero2har(self):

        output_har = r"test_har_out.har"
        shutil.copy2(TestCERO2HAR._dd + "Mdatnew7.har", output_har)

        # CERO path
        dd = os.path.dirname(__file__) + os.sep + "data" + os.sep
        pickled_cero = dd + r'test_cero_to_har_initdata.pickle'

        df = DataTools.get_test_data(pickled_cero)
        h2c = FromCERO(dd + r'test_cero_to_har.yaml')
        h2c.exec_procedures(df)

        header = DataTools.get_test_data(output_har, header_name="MAR1")
        self.assertTrue(np.isclose(header["array"][0, 0, 0, 0, 2, 0], 2.44571))
        self.assertTrue(np.isclose(header["array"][0, 0, 0, 1, 2, 0], 0.637938))
        self.assertTrue(np.isclose(header["array"][0, 0, 2, 0, 2, 0], 0.381556))

        # Tidy up
        os.remove(output_har)
        os.remove("output.csv")


if script_run:
    unittest.main()
