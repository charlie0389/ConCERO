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
Created on Mar 20 13:47:50 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import unittest

import numpy as np

from concero.cero import CERO
from concero.to_cero import ToCERO
from concero.tests.data_tools import DataTools, DefaultTestCase


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

    def test_stitch_time(self):

        tc = ToCERO(TestToCERO._dd + "test_time_stitch.yaml")
        cero = tc.create_cero()

        fc =ToCERO({"files": [{"file": TestToCERO._dd + "test_time_stitch.xlsx", "sheet": "data_final"}]})
        fin_cero = fc.create_cero()

        self.assertTrue(cero.equals(fin_cero))


    # TODO: Write test for time_regex
    # TODO: Write test for time_fmt


if __name__ == "__main__":
    unittest.main()