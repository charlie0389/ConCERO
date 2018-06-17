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
            modify_test(cero, True, ilocs=[1], start_year=2018, end_year=2019, a_kw_arg=True)

        cero = modify_test(cero, True, ilocs=[1], start_year=2018, end_year=2019, a_kw_arg=True,return_something=True)

        self.assertTrue(cero.index.values[0] == "B")
        self.assertTrue(cero.iloc[0, 0] == 100)

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
            modify_test(cero, True, ilocs=[1],
                        # rename="D",
                        a_kw_arg=True, inplace=False, init=[5.0], post=[6.0])

        cero = modify_test(cero, True, ilocs=[1],
                           # rename="D",
                           a_kw_arg=True, inplace=False, return_something=True, init=[5.0], post=[6.0])

        self.assertTrue(cero.index.values[0] == "B")
        self.assertTrue(np.allclose(cero.iloc[0].values, np.array([4.0, 4.0, 5.0])))

    def test_series_dropnans(self):
        """Ensures that NaNs are dropped from a series before a series operation is applied."""

        @libfuncs_wrappers.recursive_op
        def fibonnaci(prev, next_val):
            return prev + next_val

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3], "B": [pd.np.nan, 4, 5], "C": [4, 5, 6]}, orient="index",
                                    dtype=pd.np.float32)
        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019], format="%Y"))
        cero.sort_index(inplace=True)

        cero = fibonnaci(cero, ilocs = [1], init = [0.0]) # Only 'B' row is modified

        self.assertTrue(np.allclose(cero.iloc[0].values[1:], np.array([4.0, 9.0])))
        self.assertTrue(all(x == y for (x, y) in zip(cero.iloc[0].isna().tolist(), [True, False, False])))

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

        ret_cero = interpolate(cero, ilocs=[0])
        self.assertTrue(np.allclose(test_vals, ret_cero.iloc[0].tolist()))

        ret_cero = interpolate(cero, ilocs=[1])
        self.assertTrue(np.allclose(test_vals[1:], ret_cero.iloc[0].tolist()[1:]))
        self.assertTrue(np.isnan(ret_cero.iloc[0, 0]))

        ret_cero = interpolate(cero, ilocs=[2])
        self.assertTrue(np.allclose(test_vals[:-1], ret_cero.iloc[0].tolist()[:-1]))
        self.assertTrue(np.isnan(ret_cero.iloc[0, 4]))

        ret_cero = interpolate(cero, ilocs=[3])
        self.assertTrue(np.allclose(test_vals[1:-1], ret_cero.iloc[0].tolist()[1:-1]))
        self.assertTrue(np.isnan(ret_cero.iloc[0, 0]))
        self.assertTrue(np.isnan(ret_cero.iloc[0, 4]))

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

        cero = mv_avg_3(cero, ilocs=[1], auto_init=1, auto_post=1, inplace=False) # Only 'B' row is modified

        self.assertTrue(np.allclose(cero.iloc[0].values, np.array([10 / 3, 4.0, 14 / 3])))

    def test_no_double_initpost_spec(self):

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

        cero_cp = cero.copy(True)
        with self.assertRaises(ValueError):
            sum_3(cero_cp, init_cols=2017, init_icols=0, inplace=False)  # Checks prevention of double specification
        with self.assertRaises(ValueError):
            sum_3(cero_cp, post_cols=2017, post_icols=0, inplace=False)  # Checks prevention of double specification

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

        cero_cp = cero.copy(True)
        sum_3(cero_cp, init_cols=[2017], post_cols=[2021], inplace=False)
        self.assertTrue(np.allclose(test_vals, cero_cp.values.tolist()))

        cero_cp = cero.copy(True)
        sum_3(cero_cp, init_cols=2017, post_cols=2021, inplace=False)
        self.assertTrue(np.allclose(test_vals, cero_cp.values.tolist()))

    def test_initposticols(self):

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

        cero_cp = cero.copy()
        sum_3(cero_cp, init_icols=[0], post_icols=[-1], inplace=False)
        self.assertTrue(np.allclose(test_vals, cero_cp.values.tolist()))

        cero_cp = cero.copy()
        sum_3(cero_cp, init_icols=0, post_icols=-1, inplace=False)  # Uses integer form of init_cols
        self.assertTrue(np.allclose(test_vals, cero_cp.values.tolist()))

    def test_initpostauto(self):

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

        test_vals = [[4, 6,  9,  12, 14],
                     [16, 15, 15, 18, 20],
                     [13, 17, 20, 23, 23],
                     [28, 31, 33, 25, 15]]

        cero_cp = cero.copy()
        sum_3(cero_cp, auto_init=1, auto_post=1, inplace=False)
        self.assertTrue(np.allclose(test_vals, cero_cp.values.tolist()))

    def test_create_series(self):

        @libfuncs_wrappers.dataframe_op
        def no_op(df):
            return df

        @libfuncs_wrappers.dataframe_op
        def add_series(df):
            df.loc["E"] = pd.Series(data=[7, 10, 12, 7, 8], name="E",
                                      index=pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y")),
                                     dtype=pd.np.float32)
            return df

        @libfuncs_wrappers.dataframe_op
        def add_modify_series(df):
            df.loc["E"] = pd.Series(data=[7, 10, 12, 7, 8], name="E",
                                    index=pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y")),
                                    dtype=pd.np.float32)
            df.loc["D"] = pd.Series(data=[20, 7, 3, 1, 2], name="E",
                                    index=pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y")),
                                    dtype=pd.np.float32)
            return df

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                       "B": [6, 4, 5, 6, 7],
                                       "C": [4, 5, 8, 7, 8],
                                       "D": [9, 10, 12, 11, 2]},
                                      orient="index",
                                      dtype=pd.np.float32)

        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        cero.sort_index(inplace=True)

        df = no_op(cero)

        self.assertTrue(df.equals(cero))

        # Next test
        df2 = add_series(cero)
        self.assertTrue(df.equals(cero)) # Check cero hasn't been modified
        test_df = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                       "B": [6, 4, 5, 6, 7],
                                       "C": [4, 5, 8, 7, 8],
                                       "D": [9, 10, 12, 11, 2],
                                       "E": [7, 10, 12, 7, 8],
                                          },
                                      orient="index",
                                      dtype=pd.np.float32)

        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)
        self.assertTrue(test_df.equals(df2))

        # Next test
        df3 = add_modify_series(cero)
        self.assertTrue(df.equals(cero))  # Check cero hasn't been modified
        test_df = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                          "B": [6, 4, 5, 6, 7],
                                          "C": [4, 5, 8, 7, 8],
                                          "D": [20, 7, 3, 1, 2],
                                          "E": [7, 10, 12, 7, 8],
                                          },
                                         orient="index",
                                         dtype=pd.np.float32)

        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)
        self.assertTrue(test_df.equals(df3))


        # Now conduct tests with rename argument provided....
        test_df = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5]},
                                      orient="index",
                                      dtype=pd.np.float32)
        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)
        df_new = no_op(cero, ilocs=[0])
        df_new.sort_index(inplace=True)
        self.assertTrue(df.equals(cero)) # Check cero hasn't been modified
        self.assertTrue(df_new.equals(test_df))

        # Another test...
        test_df = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                          "B": [6, 4, 5, 6, 7]},
                                         orient="index",
                                         dtype=pd.np.float32)
        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)
        df_new = no_op(cero, ilocs=[0, 1])
        df_new.sort_index(inplace=True)
        self.assertTrue(df.equals(cero))  # Check cero hasn't been modified
        self.assertTrue(df_new.equals(test_df))

        # Another test...
        test_df = pd.DataFrame.from_dict({"B": [6, 4, 5, 6, 7],
                                          "C": [4, 5, 8, 7, 8],
                                          "A": [1, 2, 3, 4, 5],
                                          "D": [9, 10, 12, 11, 2],
                                          },
                                         orient="index",
                                         dtype=pd.np.float32)
        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)
        df_new = no_op(cero)
        df_new.sort_index(inplace=True)
        self.assertTrue(df.equals(cero))  # Check cero hasn't been modified
        self.assertTrue(df_new.equals(test_df))

        # Another test...
        test_df = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                          "B": [6, 4, 5, 6, 7],
                                          "C": [4, 5, 8, 7, 8],
                                          "D": [20, 7, 3, 1, 2],
                                          "E": [7, 10, 12, 7, 8],
                                          },
                                         orient="index",
                                         dtype=pd.np.float32)

        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)
        df_new = add_modify_series(cero)
        df_new.sort_index(inplace=True)
        self.assertTrue(df.equals(cero))  # Check cero hasn't been modified
        self.assertTrue(test_df.equals(df_new))

    def test_series_to_dataframe(self):

        @libfuncs_wrappers.dataframe_op
        def first_series(df):
            return df.iloc[0, :] # Returns a pandas.Series

        test_df = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                          "B": [6, 4, 5, 6, 7],
                                          },
                                         orient="index",
                                         dtype=pd.np.float32)

        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)

        ret = first_series(test_df)

        self.assertTrue(isinstance(ret, pd.DataFrame))
        self.assertEqual(ret.shape, (1, 5))
        self.assertEqual(ret.iloc[0].tolist(), [1, 2, 3, 4, 5])
        self.assertEqual(ret.index.tolist(), ["A"])

if __name__ == '__main__':
    unittest.main()
