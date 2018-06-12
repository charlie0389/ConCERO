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
Created on Jan 23 08:29:29 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
script_run = True if __name__ == "__main__" else False
__name__ = "concero.tests.test_cero_to_har"

import os
import unittest
import numpy as np
import shutil

import harpy

from concero.from_cero import FromCERO
from concero.tests.data_tools import DataTools


class TestCERO2HAR(unittest.TestCase):
    '''Test the CERO to HAR conversion.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_cero2har(self):

        output_har = r"test_har_out.har"
        shutil.copy2(TestCERO2HAR._dd + "Mdatnew7.har", output_har)

        # CERO path
        pickled_cero = TestCERO2HAR._dd + r'test_cero_to_har_initdata.pickle'

        df = DataTools.get_test_data(pickled_cero)
        h2c = FromCERO(TestCERO2HAR._dd + r'test_cero_to_har.yaml')
        h2c.exec_procedures(df)

        hf = harpy.HarFileObj.loadFromDisk(output_har)
        header = hf.getHeaderArrayObj(ha_name="MAR1")
        self.assertTrue(np.isclose(header["array"][0, 0, 0, 0, 0, 0], 2.44571))
        self.assertTrue(np.isclose(header["array"][0, 0, 0, 1, 0, 0], 0.637938))
        self.assertTrue(np.isclose(header["array"][0, 0, 2, 0, 0, 0], 0.381556))

        # Tidy up
        os.remove(output_har)


if script_run:
    unittest.main()
