"""
Created on Mar 01 08:44:26 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import unittest

import pandas as pd
import numpy as np

import concero.libfuncs as libfuncs
from concero.cero import CERO
import concero.libfuncs_wrappers as libfuncs_wrappers
from concero.tests.data_tools import DefaultTestCase


class TestLibfuncsWrappers(DefaultTestCase):
    '''Tests libfuncs methods.'''

    def test_dataframe_op(self):

        @libfuncs_wrappers.dataframe_op
        def modify_test(df, an_arg, a_kw_arg=None):
            self.assertTrue(an_arg)
            self.assertTrue(a_kw_arg)

            # Restricted df for comparison
            dfr = pd.DataFrame.from_dict({"A": [2], "C": [5]}, orient="index")
            dfr.columns = pd.DatetimeIndex(pd.to_datetime([2018], format="%Y"))
            dfr.sort_index(inplace=True)
            dfr = dfr.astype(pd.np.float32)

            self.assertTrue(df.equals(dfr))

            df.iloc[0,0] = 3.0

        df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [4, 5, 6]}, orient="index")
        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        df.sort_index(inplace=True)
        df = df.astype(pd.np.float32)

        self.assertTrue(CERO.is_cero(df))

        modify_test(df, True, ilocs=[0,2], start_year=2018, end_year=2019, rename="D", a_kw_arg=True)

        self.assertTrue(df.index.values[0] == "D")
        self.assertTrue(df.iloc[0, 1] == 3.0)

    def test_series_op(self):

        @libfuncs_wrappers.series_op
        def modify_test(series, an_arg, a_kw_arg=None, return_something=False):
            self.assertTrue(an_arg)
            self.assertTrue(a_kw_arg)

            # pandas.Series for comparison
            sr = pd.Series(data=[4.0], dtype=pd.np.float32, index= pd.DatetimeIndex(pd.to_datetime([2018], format="%Y")))

            self.assertTrue(series.equals(sr))

            sr[0] = 100.0

            if return_something:
                # By default, this function does not return anything, which should raise an error - this if statement
                # avoids that
                return sr

        df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [4, 5, 6]}, orient="index")
        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        df.sort_index(inplace=True)
        df = df.astype(pd.np.float32)

        self.assertTrue(CERO.is_cero(df))

        with self.assertRaises(TypeError):
            modify_test(df, True, ilocs=[1], start_year=2018, end_year=2019, rename="D", a_kw_arg=True)

        modify_test(df, True, ilocs=[1], start_year=2018, end_year=2019, rename="D", a_kw_arg=True,
                    return_something=True)

        self.assertTrue(df.index.values[1] == "D")
        self.assertTrue(df.iloc[1,1] == 100)

    def test_recursive_op(self):

        @libfuncs_wrappers.recursive_op
        def modify_test(val_a, val_b, val_c, an_arg, a_kw_arg=None, return_something=False):
            self.assertTrue(an_arg == True)
            self.assertTrue(a_kw_arg == True)

            if return_something:
                # By default, this function does not return anything, which should raise an error - this if statement
                # avoids that
                return (val_a + val_b + val_c)/3

        df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [4, 5, 6]}, orient="index")
        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        df.sort_index(inplace=True)
        df = df.astype(pd.np.float32)

        self.assertTrue(CERO.is_cero(df))

        with self.assertRaises(ValueError):
            modify_test(df, True, ilocs=[1], rename="D", a_kw_arg=True, inplace=False, init=[5.0], post=[6.0])

        modify_test(df, True, ilocs=[1], rename="D", a_kw_arg=True, inplace=False, return_something=True, init=[5.0], post=[6.0])

        self.assertTrue(df.index.values[1] == "D")

        self.assertTrue(np.allclose(df.iloc[1].values, np.array([4.0, 4.0, 5.0])))

    def test_series_dropnans(self):
        """Ensures that NaNs are dropped from a series before a series operation is applied."""

        @libfuncs_wrappers.recursive_op
        def fibonnaci(prev, next_val):
            return prev + next_val

        df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [pd.np.nan, 4, 5], "C": [4, 5, 6]}, orient="index",
                                    dtype=pd.np.float32)
        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        df.sort_index(inplace=True)
        self.assertTrue(CERO.is_cero(df))

        fibonnaci(df, ilocs = [1], init = [0.0]) # Only 'B' row is modified

        self.assertTrue(np.allclose(df.iloc[1].values[1:], np.array([4.0, 9.0])))
        self.assertTrue(all(x == y for (x, y) in zip(df.iloc[1].isna().tolist(), [True, False, False])))

    def test_autoinitpost(self):
        """Ensures that NaNs are dropped from a series before a series operation is applied."""

        @libfuncs_wrappers.recursive_op
        def mv_avg_3(first, second, third):
            return (first + second + third)/3

        df = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [4, 5, 6]}, orient="index",
                                    dtype=pd.np.float32)
        df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        df.sort_index(inplace=True)
        self.assertTrue(CERO.is_cero(df))

        mv_avg_3(df, ilocs=[1], auto_init=1, auto_post=1, inplace=False) # Only 'B' row is modified

        self.assertTrue(np.allclose(df.iloc[1].values, np.array([10/3, 4.0, 14/3])))


if __name__ == '__main__':
    unittest.main()
