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

import os
import unittest
import numpy as np

import pandas as pd

from concero.tests.data_tools import DataTools, DefaultTestCase
from concero.cero import CERO
from concero.to_cero import ToCERO


class TestCERO(DefaultTestCase):
    '''Tests CERO methods.'''
    _dd = os.path.dirname(__file__) + os.sep + "data" + os.sep

    def test_idxconflict(self):
        cero = DataTools.get_test_data(TestCERO._dd + "test_cero.pickle")

        with self.assertRaises(CERO.CEROIndexConflict):
            CERO.combine_ceros([cero, cero], overwrite=False, verify_cero=True)

    def test_is_cero(self):
        """Tests the validation method by feeding it deliberately False data."""

        df = None

        with self.assertRaises(CERO.InvalidCERO, msg=CERO._msg_inv_type):
            CERO.is_cero(df)

        df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [4, 5, 6]}, orient="index", dtype=int)
        df.index = pd.MultiIndex.from_tuples([("A", 1), ("A", 2)])
        # ^^ ``df`` is not even close to being a CERO...

        with self.assertRaises(CERO.InvalidCERO, msg=CERO._msg_bad_idx):
            CERO.is_cero(df)

        df.index = pd.Index(["A", "A"])

        with self.assertRaises(CERO.InvalidCERO, msg=CERO._msg_bad_col):
            CERO.is_cero(df)

        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2017, 2019], format="%Y"))

        with self.assertRaises(CERO.InvalidCERO, msg=CERO._msg_idx_nunique):
            CERO.is_cero(df)

        df.index = pd.Index(["A", "B"])

        with self.assertRaises(CERO.InvalidCERO, msg=CERO._msg_col_nunique):
            CERO.is_cero(df)

        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))

        with self.assertRaises(CERO.InvalidCERO, msg=CERO._msg_val_type):
            CERO.is_cero(df)

        df = df.astype(pd.np.float32, copy=False)

        self.assertTrue(CERO.is_cero(df))

    def test_create_empty(self):

        empty_cero = CERO.create_empty()
        self.assertTrue(CERO.is_cero(empty_cero))

    def test_name_map(self):

        def init_df():
            df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [6, 7, 8]}, orient="index")
            df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
            df.sort_index(inplace=True)
            df = df.astype(pd.np.float32)
            self.assertTrue(CERO.is_cero(df))
            return df

        df = init_df()
        mapping = dict([("A","D"), ("B","E"), ("C","F")])

        res = CERO.rename_index_values(df, mapping)

        test_names = ["D", "E", "F"]

        self.assertIsNone(res)
        self.assertTrue(all([x == y for (x, y) in zip(df.index.tolist(), test_names)]))

        # Test 2

        df = init_df()
        mapping = dict([("B", "E"), ("C", "F")])

        res = CERO.rename_index_values(df, mapping)

        test_names = ["A", "E", "F"]

        self.assertIsNone(res)
        self.assertTrue(all([x == y for (x, y) in zip(df.index.tolist(), test_names)]))

        # Test 3

        df = init_df()
        mapping = dict([("A", "D"), ("B", "E"), ("C", "F")])

        res = CERO.rename_index_values(df, mapping, inplace=False)

        test_names = ["D", "E", "F"]
        test_names_df = ["A", "B", "C"]

        self.assertTrue(all([x == y for (x, y) in zip(res.index.tolist(), test_names)]))
        self.assertTrue(all([x == y for (x, y) in zip(df.index.tolist(), test_names_df)]))

        # Test 4

        df = init_df()
        mapping = dict([("B", "E"), ("C", "F")])

        res = CERO.rename_index_values(df, mapping, inplace=False)

        test_names = ["A", "E", "F"]
        test_names_df = ["A", "B", "C"]

        self.assertTrue(all([x == y for (x, y) in zip(res.index.tolist(), test_names)]))
        self.assertTrue(all([x == y for (x, y) in zip(df.index.tolist(), test_names_df)]))

    def test_csv_complex(self):

        test_df = pd.DataFrame(data=np.array([[3.78981,2.73377], [2.22027,3.99257]]), index=[("a", "b"), "c"],
                               dtype=pd.np.float32)
        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018], format="%Y"))

        cero = CERO.read_csv(TestCERO._dd + "test_csv_complex.csv")

        self.assertTrue(test_df.equals(cero))



if script_run:
    unittest.main()
