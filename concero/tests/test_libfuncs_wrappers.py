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

    # def test_dataframe_op(self):
    #
    #     @libfuncs_wrappers.dataframe_op
    #     def modify_test(cero, an_arg, a_kw_arg=None):
    #         self.assertTrue(an_arg)
    #         self.assertTrue(a_kw_arg)
    #
    #         # Restricted cero for comparison
    #         ceror = pd.DataFrame.from_dict({"A": [2], "C": [5]}, orient="index")
    #         ceror.columns = pd.DatetimeIndex(pd.to_datetime([2018], format="%Y"))
    #         ceror.sort_index(inplace=True)
    #         ceror = ceror.astype(pd.np.float32)
    #
    #         self.assertTrue(cero.equals(ceror))
    #
    #         cero.iloc[0,0] = 3.0
    #
    #     cero = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [4, 5, 6]}, orient="index")
    #     cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
    #     cero.sort_index(inplace=True)
    #     cero = cero.astype(pd.np.float32)
    #
    #     modify_test(cero, True, ilocs=[0,2], start_year=2018, end_year=2019, rename="D", a_kw_arg=True)
    #
    #     self.assertTrue(cero.index.values[0] == "D")
    #     self.assertTrue(cero.iloc[0, 1] == 3.0)

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

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [4, 5, 6]}, orient="index")
        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        cero.sort_index(inplace=True)
        cero = cero.astype(pd.np.float32)

        with self.assertRaises(TypeError):
            modify_test(cero, True, ilocs=[1], start_year=2018, end_year=2019, rename="D", a_kw_arg=True)

        modify_test(cero, True, ilocs=[1], start_year=2018, end_year=2019, rename="D", a_kw_arg=True,
                    return_something=True)

        self.assertTrue(cero.index.values[1] == "D")
        self.assertTrue(cero.iloc[1,1] == 100)

    def test_recursive_op(self):

        @libfuncs_wrappers.recursive_op
        def modify_test(val_a, val_b, val_c, an_arg, a_kw_arg=None, return_something=False):
            self.assertTrue(an_arg == True)
            self.assertTrue(a_kw_arg == True)

            if return_something:
                # By default, this function does not return anything, which should raise an error - this if statement
                # avoids that
                return (val_a + val_b + val_c)/3

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [4, 5, 6]}, orient="index")
        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        cero.sort_index(inplace=True)
        cero = cero.astype(pd.np.float32)

        with self.assertRaises(ValueError):
            modify_test(cero, True, ilocs=[1], rename="D", a_kw_arg=True, inplace=False, init=[5.0], post=[6.0])

        modify_test(cero, True, ilocs=[1], rename="D", a_kw_arg=True, inplace=False, return_something=True, init=[5.0], post=[6.0])

        self.assertTrue(cero.index.values[1] == "D")

        self.assertTrue(np.allclose(cero.iloc[1].values, np.array([4.0, 4.0, 5.0])))

    def test_series_dropnans(self):
        """Ensures that NaNs are dropped from a series before a series operation is applied."""

        @libfuncs_wrappers.recursive_op
        def fibonnaci(prev, next_val):
            return prev + next_val

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [pd.np.nan, 4, 5], "C": [4, 5, 6]}, orient="index",
                                    dtype=pd.np.float32)
        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        cero.sort_index(inplace=True)

        fibonnaci(cero, ilocs = [1], init = [0.0]) # Only 'B' row is modified

        self.assertTrue(np.allclose(cero.iloc[1].values[1:], np.array([4.0, 9.0])))
        self.assertTrue(all(x == y for (x, y) in zip(cero.iloc[1].isna().tolist(), [True, False, False])))

    def test_series_dropnans2(self):

        @libfuncs_wrappers.series_op
        def interpolate(series, **kwargs):
            defaults = {
                "method":"time",
            }
            defaults.update(kwargs)
            return series.interpolate(**defaults)

        cero = pd.DataFrame.from_dict({"A": [1, 2, pd.np.nan, 4, 5],
                                     "B": [pd.np.nan, 2, pd.np.nan, 4, 5],
                                     "C": [1, 2, pd.np.nan, 4, pd.np.nan],
                                     "D": [pd.np.nan, 2, pd.np.nan, 4, pd.np.nan],
                                     },
                                      orient="index",
                                    dtype=pd.np.float32)
        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        cero.sort_index(inplace=True)

        test_vals = [1, 2, 3, 4, 5]

        interpolate(cero, ilocs=[0])
        self.assertTrue(np.allclose(test_vals, cero.iloc[0].tolist()))

        interpolate(cero, ilocs=[1])
        self.assertTrue(np.allclose(test_vals[1:], cero.iloc[1].tolist()[1:]))

        interpolate(cero, ilocs=[2])
        self.assertTrue(np.allclose(test_vals[:-1], cero.iloc[2].tolist()[:-1]))

        interpolate(cero, ilocs=[3])
        self.assertTrue(np.allclose(test_vals[1:-1], cero.iloc[3].tolist()[1:-1]))

        self.assertTrue(np.isnan(cero.iloc[1, 0]))
        self.assertTrue(np.isnan(cero.iloc[3, 0]))
        self.assertTrue(np.isnan(cero.iloc[2, 4]))
        self.assertTrue(np.isnan(cero.iloc[3, 4]))

    def test_series_dropnans3(self):

        @libfuncs_wrappers.series_op
        def interpolate(series, **kwargs):
            defaults = {
                "method":"time",
            }
            defaults.update(kwargs)
            ser = series.interpolate(**defaults)
            return ser

        cero = pd.DataFrame.from_dict({"A": [1, 2, pd.np.nan, 4, 5],
                                     "B": [pd.np.nan, 2, pd.np.nan, 4, 5],
                                     "C": [1, 2, pd.np.nan, 4, pd.np.nan],
                                     "D": [pd.np.nan, 2, pd.np.nan, 4, pd.np.nan],
                                     },
                                      orient="index",
                                    dtype=pd.np.float32)
        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        cero.sort_index(inplace=True)

        test_vals = [[1, 2, 3, 4, 5],
                     [pd.np.nan, 2, 3, 4, 5],
                     [1, 2, 3, 4, pd.np.nan],
                     [pd.np.nan, 2, 3, 4, pd.np.nan]]

        interpolate(cero)
        self.assertTrue(np.allclose(test_vals, cero.values.tolist(), equal_nan=True))

        self.assertTrue(np.isnan(cero.iloc[1, 0]))
        self.assertTrue(np.isnan(cero.iloc[3, 0]))
        self.assertTrue(np.isnan(cero.iloc[2, 4]))
        self.assertTrue(np.isnan(cero.iloc[3, 4]))


    def test_autoinitpost(self):
        """Ensures that NaNs are dropped from a series before a series operation is applied."""

        @libfuncs_wrappers.recursive_op
        def mv_avg_3(first, second, third):
            return (first + second + third)/3

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [3, 4, 5], "C": [4, 5, 6]}, orient="index",
                                    dtype=pd.np.float32)
        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        cero.sort_index(inplace=True)

        mv_avg_3(cero, ilocs=[1], auto_init=1, auto_post=1, inplace=False) # Only 'B' row is modified

        self.assertTrue(np.allclose(cero.iloc[1].values, np.array([10/3, 4.0, 14/3])))

    def test_initpostcols(self):

        @libfuncs_wrappers.recursive_op
        def sum_3(nm1, n, n1):
            return (nm1 + n + n1)

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                       "B": [6, 4, 5, 6, 7],
                                       "C": [4, 5, 8, 7, 8],
                                       "D": [9, 10, 12, 11, 2],
                                     }, orient="index",
                                    dtype=pd.np.float32)

        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        cero.sort_index(inplace=True)

        test_vals = [[1, 6,  9,  12, 5],
                     [6, 15, 15, 18, 7],
                     [4, 17, 20, 23, 8],
                     [9, 31, 33, 25, 2]]

        sum_3(cero, init_cols=[2017], post_cols=[2021], inplace=False)
        self.assertTrue(np.allclose(test_vals, cero.values.tolist()))

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                       "B": [6, 4, 5, 6, 7],
                                       "C": [4, 5, 8, 7, 8],
                                       "D": [9, 10, 12, 11, 2],
                                       }, orient="index",
                                      dtype=pd.np.float32)

        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        cero.sort_index(inplace=True)

        test_vals = [[1, 6, 9, 12, 5],
                     [6, 15, 15, 18, 7],
                     [4, 17, 20, 23, 8],
                     [9, 31, 33, 25, 2]]

        sum_3(cero, init_cols=1, post_cols=1, inplace=False) # Uses integer form of init_cols
        self.assertTrue(np.allclose(test_vals, cero.values.tolist()))

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                       "B": [6, 4, 5, 6, 7],
                                       "C": [4, 5, 8, 7, 8],
                                       "D": [9, 10, 12, 11, 2],
                                       }, orient="index",
                                      dtype=pd.np.float32)

        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        cero.sort_index(inplace=True)

        test_vals = [[1, 6,  13, 22, 5],
                     [6, 15, 26, 39, 7],
                     [4, 17, 32, 47, 8],
                     [9, 31, 54, 67, 2]]

        sum_3(cero, init_cols=1, post_cols=1)  # Uses inplace form
        self.assertTrue(np.allclose(test_vals, cero.values.tolist()))

    # def test_create_series(self):
    #
    #     @libfuncs_wrappers.series_op
    #     def no_op(df):
    #         return
    #
    #     cero = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
    #                                    "B": [6, 4, 5, 6, 7],
    #                                    "C": [4, 5, 8, 7, 8],
    #                                    "D": [9, 10, 12, 11, 2]},
    #                                   orient="index",
    #                                   dtype=pd.np.float32)
    #
    #     cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
    #     cero.sort_index(inplace=True)
    #
    #
    #
    #     self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
