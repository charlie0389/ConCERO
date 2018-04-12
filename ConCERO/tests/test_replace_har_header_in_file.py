script_run = True if __name__ == "__main__" else False
# __name__ = "ConCERO.tests.test_replace_har_header_in_file"

import unittest
import os
import shutil

from ConCERO.from_cero import FromCERO
from ConCERO.tests.data_tools import DataTools

class TestHARHeaderReplace(unittest.TestCase):
    """Tests header replacement functionality.
    """

    # def setUp(self):
    #     self._old_dir = os.getcwd()
    #     os.chdir(os.path.dirname(__file__))
    #
    # def tearDown(self):
    #     os.chdir(self._old_dir)

    def test_replace_har_header_in_file(self):

        dd = os.path.join(os.path.dirname(__file__), "data", "")
        shutil.copy2(dd + "test_Forenew7.shk", "test_Forenew7.shk")

        # CERO path
        df = DataTools.get_test_data(dd + "test_replace_har_header_in_file.pickle")
        fc = FromCERO(dd + "test_replace_har_header_in_file.yaml")
        fc.exec_procedures(df)

        test_har = DataTools.get_test_data("test_Forenew7.shk")

        tn = test_har.getHeaderArrayNames()
        gn = DataTools.get_test_data("Forenew7.shk").getHeaderArrayNames()

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