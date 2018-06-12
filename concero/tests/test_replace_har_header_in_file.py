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

script_run = True if __name__ == "__main__" else False

import unittest
import os
import shutil

import harpy

from concero.from_cero import FromCERO
from concero.tests.data_tools import DataTools

class TestHARHeaderReplace(unittest.TestCase):
    """Tests header replacement functionality.
    """

    def test_replace_har_header_in_file(self):

        dd = os.path.join(os.path.dirname(__file__), "data", "")
        shutil.copy2(dd + "test_Forenew7.shk", "test_Forenew7.shk")

        # CERO path
        df = DataTools.get_test_data(dd + "test_replace_har_header_in_file.pickle")
        fc = FromCERO(dd + "test_replace_har_header_in_file.yaml")
        fc.exec_procedures(df)

        test_har = DataTools.get_test_data("test_Forenew7.shk")
        tn = test_har.getHeaderArrayNames()

        gn = harpy.HarFileObj.loadFromDisk(filename="Forenew7.shk").getHeaderArrayNames()

        try:
            self.assertTrue(all([x == y for x, y  in zip(tn, gn)]))
        except AssertionError as e:
            print("Test data headers: ", tn)
            print("Generated data headers: ", gn)
            raise e

        os.remove("test_Forenew7.shk")  # Tidy up
        os.remove("Forenew7.shk") # Tidy up

if script_run:
    unittest.main()