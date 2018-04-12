"""
Created on Apr 09 10:41:37 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import unittest
import shutil
import sys

from ConCERO.to_cero import ToCERO
from ConCERO.tests.data_tools import DataTools, DefaultTestCase


class TestToCERO_FileObj(DefaultTestCase):

    _dd = os.path.join(os.path.dirname(__file__),"data","")

    def test_load_config(self):

        conf = "non_existent_conf_file.yaml"

        with self.assertRaises(FileNotFoundError):
            ToCERO._FileObj.load_config(conf)

        parent = {'search_paths': [TestToCERO_FileObj._dd]}
        conf = "test__fileobj_load_config.yaml"

        fo = ToCERO._FileObj.load_config(conf, parent=parent)

        conf = {"file": os.path.abspath(TestToCERO_FileObj._dd + "test_csv.csv")}

        fo = ToCERO._FileObj.load_config(conf)

        self.assertTrue("file" in fo)
        self.assertTrue(fo["file"]) # Checks string is non-empty
        self.assertTrue(fo["type"] == "csv")
        self.assertTrue(fo["search_paths"] == [os.path.abspath(".")])

    def test_is_valid(self):

        conf = {"No file key...": None}

        with self.assertRaises(TypeError):
            ToCERO._FileObj.is_valid(conf)

        self.assertFalse(ToCERO._FileObj.is_valid(conf, raise_exception=False))

        conf = {"file": None} # Invalid value for key "file"

        with self.assertRaises(TypeError):
            ToCERO._FileObj.is_valid(conf)

        self.assertFalse(ToCERO._FileObj.is_valid(conf, raise_exception=False))

        conf = {"file": "a file name"}

        self.assertTrue(ToCERO._FileObj.is_valid(conf))

    @unittest.skipIf(sys.platform.startswith("win"), " Impossible to disable read with os.chmod() on windows.")
    def test_run_checks(self):
        conf = {"file": "not_a_valid_file.file", "search_paths": [os.path.abspath(".")]}

        with self.assertRaises(FileNotFoundError):
            ToCERO._FileObj.run_checks(conf)

        self.assertFalse(ToCERO._FileObj.run_checks(conf, raise_exception=False))

        conf = {"file": "test_csv_noread.csv", "search_paths": [os.path.abspath(".")]}

        try:

            shutil.copy2(TestToCERO_FileObj._dd + "test_csv.csv", os.path.join(os.path.abspath("."), "test_csv_noread.csv"))
            os.chmod("test_csv_noread.csv", 0o000)

            with self.assertRaises(PermissionError):
                ToCERO._FileObj.run_checks(conf)

            self.assertFalse(ToCERO._FileObj.run_checks(conf, raise_exception=False))

        finally:
            os.remove("test_csv_noread.csv")

        conf = {"file": TestToCERO_FileObj._dd + "test_csv.csv", "search_paths": [os.path.abspath(".")]}

        self.assertTrue(ToCERO._FileObj.run_checks(conf))


if __name__ == "__main__":
    unittest.main()