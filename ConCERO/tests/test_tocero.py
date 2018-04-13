"""
Created on Mar 20 13:47:50 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import unittest

import numpy as np

from ConCERO.cero import CERO
from ConCERO.to_cero import ToCERO
from ConCERO.tests.data_tools import DataTools, DefaultTestCase


class TestToCERO(DefaultTestCase):
    '''Test the VURM to CERO conversion class.'''

    _dd = os.path.join(os.path.dirname(__file__),"data","")

    def test_multiindex_xlsx(self):

        to_cero = ToCERO(conf=(TestToCERO._dd + r'test_multiindex_xlsx.yaml'))
        cero = to_cero.create_cero()
        self.assertTrue(CERO.is_cero(cero))

    def test_empty_xlsx(self):

        to_cero = ToCERO(conf=(TestToCERO._dd + r"test_empty_xlsx.yaml"))
        cero = to_cero.create_cero()
        with self.assertRaises(CERO.EmptyCERO):
            self.assertTrue(CERO.is_cero(cero, empty_ok=False))
        self.assertTrue(CERO.is_cero(cero))

    def test_nrows(self):
        to_cero = ToCERO(conf=(TestToCERO._dd + r"test_nrows_1.yaml"))
        cero = to_cero.create_cero()

        self.assertTrue(np.allclose(cero.values[0], [0.00551917898595782, 0.00551917898595782]))

    def test_nrows_skiprows(self):
        to_cero = ToCERO(conf=(TestToCERO._dd + r"test_nrows_2.yaml"))
        cero = to_cero.create_cero()

        self.assertTrue(np.allclose(cero.values[0], [0.00551917898595782, 0.00551917898595782]))

    def test_nrows_empty(self):
        to_cero = ToCERO(conf=(TestToCERO._dd + r"test_nrows_3.yaml"))
        cero = to_cero.create_cero()

        self.assertTrue(np.all(np.isnan(cero.values[0])))

    def test_rename(self):

        to_cero = ToCERO(conf=(TestToCERO._dd + r"test_rename.yaml"))
        cero = to_cero.create_cero()

        CERO.is_cero(cero)

        test_idx = [("2", "PROFESSIONALS"), "MANAGERS"] # Rename operation always moves series to the end

        self.assertTrue(all([x==y for (x, y) in zip(test_idx, cero.index.tolist())]))

    def test_rename_2(self):

        to_cero = ToCERO(conf=(TestToCERO._dd + r"test_rename_2.yaml"))
        cero = to_cero.create_cero()

        CERO.is_cero(cero)

        test_idx = ["PROFESSIONALS", ("1", "MANAGERS")] # Rename operation always moves series to the end

        self.assertTrue(all([x == y for (x, y) in zip(test_idx, cero.index.tolist())]))

    def test_is_valid(self):

        with self.assertRaises(TypeError):
            ToCERO.is_valid({"files": 1})

        self.assertFalse(ToCERO.is_valid({"files": 1}, raise_exception=False))

        with self.assertRaises(TypeError):
            ToCERO.is_valid({"files": "not a list"})

        self.assertFalse(ToCERO.is_valid({"files": "not a list"}, raise_exception=False))

        with self.assertRaises(TypeError):
            ToCERO.is_valid({"files": {"file": "not_a__FileObj object."}})

        self.assertFalse(ToCERO.is_valid({"files": {"file": "not_a__FileObj object."}}, raise_exception=False))

        self.assertTrue({"files": {"file": "Mdatnew7.har"}})

    def test_run_checks(self):

        with self.assertRaises(FileNotFoundError):
            ToCERO.run_checks({"files": [{"file": "not_a__FileObj object.", "search_paths": [TestToCERO._dd]}]})

        self.assertFalse(ToCERO.run_checks({"files": [{"file": "not_a__FileObj object.",
                                                       "search_paths": [TestToCERO._dd]}]},
                                           raise_exception=False))

        self.assertTrue(ToCERO.run_checks({"files": [{"file": "test_csv.csv",
                                                     "search_paths": [TestToCERO._dd]}]}))

    def test_complex_xlsx(self):

        to_cero = ToCERO(conf=(TestToCERO._dd + r'test_complex_xlsx_import.yaml'))
        cero = to_cero.create_cero()

        df = DataTools.get_test_data(TestToCERO._dd + "test_complex_xlsx_result.pickle")

        self.assertTrue(CERO.is_cero(cero))
        self.assertTrue(cero.equals(df))


    # TODO: Write test for time_regex
    # TODO: Write test for time_fmt


if __name__ == "__main__":
    unittest.main()