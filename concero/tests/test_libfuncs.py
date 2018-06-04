"""
Created on Feb 07 18:06:25 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import unittest
import os

import pandas as pd
import numpy as np

import concero.libfuncs as libfuncs
from concero.cero import CERO
from concero.to_cero import ToCERO
from concero.tests.data_tools import DefaultTestCase


class TestLibfuncs(DefaultTestCase):
    '''Tests libfuncs methods.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_libfuncs(self):
        '''Tests a scenario run.'''

        self.assertIsNotNone(getattr(libfuncs, "merge"))
        self.assertIsNotNone(getattr(libfuncs, "iter_and_norm"))

    def test_fillna(self):
        df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [6, 7, 8]}, orient="index")
        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        df.sort_index(inplace=True)
        df.iloc[1, 1] = pd.np.nan
        df = df.astype(pd.np.float32)
        self.assertTrue(CERO.is_cero(df))

        libfuncs.fillna(df, value=0.0)
        self.assertTrue(df.iloc[1, 1] == 0.0)

        df.iloc[1, 1] = pd.np.nan
        libfuncs.fillna(df, method="bfill")
        self.assertTrue(df.iloc[1, 1] == 5.0)

        df.iloc[1, 1] = pd.np.nan
        libfuncs.fillna(df)
        self.assertTrue(df.iloc[1, 1] == 3.0)

        self.assertTrue(CERO.is_cero(df))

    def test_apply_func(self):
        df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [6, 7, 8]},
                                    orient="index",
                                    dtype=pd.np.float32)
        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        df.sort_index(inplace=True)
        self.assertTrue(CERO.is_cero(df))

        libfuncs.apply_func(df, numpy_func="square")

        test_df = pd.DataFrame.from_dict({"A": [1, 4, 9], "B": [9, 16, 25], "C": [36, 49, 64]},
                                    orient="index",
                                    dtype=pd.np.float32)
        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        test_df.sort_index(inplace=True)

        self.assertTrue(df.equals(test_df))

    def test_groupby_and_aggregate(self):
        """ Dependent on ToCERO being functional.

        :return:
        """

        tc = ToCERO({"files": [{"file": TestLibfuncs._dd + "test_groupby_and_aggregate.xlsx",
                                "sheet": "groupby",
                                "index_col": [0,1]}]})

        cero = tc.create_cero()
        cero = libfuncs.groupby(cero, key=0, match="a", agg="sum")
        test_list = ["a", ("a", "c"), ("a", "d"), ("b", "b"), ("c", "b")]
        test_vals = [6, 2, 3, 4, 5]
        self.assertTrue(
        all([np.isclose(x, y) for (x, y) in zip(test_vals, cero[pd.datetime.strptime("2018", "%Y")].tolist())]))
        self.assertTrue(all([x==y for (x,y)  in zip(test_list, cero.index.tolist())]))

        cero = tc.create_cero()
        cero = libfuncs.groupby(cero, key=1, match="b", agg="mean")
        test_list = ["b", ("a", "c"), ("a", "d"), ("b", "b"), ("c", "b")]
        test_vals = [3.3333333333, 2, 3, 4, 5]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, cero.index.tolist())]))
        self.assertTrue(
            all([np.isclose(x, y) for (x, y) in zip(test_vals, cero[pd.datetime.strptime("2018", "%Y")].tolist())]))

        cero = tc.create_cero()
        cero = libfuncs.groupby(cero, key=0, agg="count")
        test_list = ["a", ("a", "c"), ("a", "d"), "b", "c"]
        test_vals = [3, 2, 3, 1, 1]
        self.assertTrue(
            all([np.isclose(x, y) for (x, y) in zip(test_vals, cero[pd.datetime.strptime("2018", "%Y")].tolist())]))
        self.assertTrue(all([x == y for (x, y) in zip(test_list, cero.index.tolist())]))

        cero = tc.create_cero()
        cero = libfuncs.groupby(cero, key=0, agg="count")
        test_list = ["a", ("a", "c"), ("a", "d"), "b", "c"]
        test_vals = [3, 2, 3, 1, 1]
        self.assertTrue(
            all([np.isclose(x, y) for (x, y) in zip(test_vals, cero[pd.datetime.strptime("2018", "%Y")].tolist())]))
        self.assertTrue(all([x == y for (x, y) in zip(test_list, cero.index.tolist())]))

        tc = ToCERO({"files": [{"file": TestLibfuncs._dd + "test_groupby_and_aggregate.xlsx",
                                "sheet": "groupby_2",
                                "index_col": [0, 1, 2]}]})

        cero = tc.create_cero()
        cero = libfuncs.groupby(cero, key=[0, 1], agg="count")
        test_list = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'b'),
                     ('c', 'b'), ('a', 'b', '2'), ('a', 'c', '2'), ('a', 'd', '3'), ('a', 'c', '3')]
        test_vals = [2, 3, 2, 1, 1, 6, 7, 8, 9]
        self.assertTrue(
            all([np.isclose(x, y) for (x, y) in zip(test_vals, cero[pd.datetime.strptime("2018", "%Y")].tolist())]))
        self.assertTrue(all([x == y for (x, y) in zip(test_list, cero.index.tolist())]))

    def test_mult(self):
        df = pd.DataFrame(data=[pd.Series(data=[1, 2, 3], index=["a", "b", "c"])],
                          index=["A"],
                          dtype=pd.np.float32)
        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))

        res = libfuncs.mult(df, factor=2)
        test_df = df*2

        self.assertTrue(res.equals(test_df))

if __name__ == '__main__':
    unittest.main()
