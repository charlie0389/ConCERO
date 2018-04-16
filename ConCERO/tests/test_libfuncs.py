"""
Created on Feb 07 18:06:25 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import unittest

import pandas as pd

import ConCERO.libfuncs as libfuncs
from ConCERO.cero import CERO
from ConCERO.tests.data_tools import DefaultTestCase


class TestLibfuncs(DefaultTestCase):
    '''Tests libfuncs methods.'''

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

if __name__ == '__main__':
    unittest.main()
