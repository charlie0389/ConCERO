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