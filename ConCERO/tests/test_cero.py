script_run = True if __name__ == "__main__" else False

import os
import unittest

import pandas as pd

from ConCERO.tests.data_tools import DataTools, DefaultTestCase
from ConCERO.cero import CERO
from ConCERO.to_cero import ToCERO


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



if script_run:
    unittest.main()
