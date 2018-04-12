"""
Created on Apr 04 15:35:17 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

script_run = True if __name__ == "__main__" else False

import os
import unittest

import numpy as np
import pandas as pd

from ConCERO.tests.data_tools import DataTools, DefaultTestCase
from ConCERO.cero import CERO
from ConCERO.from_cero import FromCERO


class TestFromCERO(DefaultTestCase):
    '''Tests CERO methods.'''
    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_sets_and_mapping(self):

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3], "D": [4], "E": [5], "F": [6], }, orient='index',
                                    dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))
        self.assertTrue(CERO.is_cero(cero))

        fc = FromCERO(TestFromCERO._dd + "test_fromcero_mapping.yaml")
        fc.exec_procedures(cero)

        df1 = pd.read_csv("test_fromcero_mapping1.csv", index_col=0)
        test_list = [1, 2, 3]
        df1_vals = [x[0] for x in df1.values.tolist()]
        self.assertTrue(all([np.isclose(x, y) for (x, y) in zip(test_list, df1_vals)]))
        test_list = ["A", "B", "C"]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df1.index.tolist())]))

        df2 = pd.read_csv("test_fromcero_mapping2.csv", index_col=0)
        test_list = [4, 5, 6]
        df2_vals = [x[0] for x in df2.values.tolist()]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df2_vals)]))
        test_list = ["G", "H", "I"]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df2.index.tolist())]))

        os.remove("test_fromcero_mapping1.csv")
        os.remove("test_fromcero_mapping2.csv")

    # def test_csv_out(self):
    #
    #     cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3], "D": [4], "E": [5], "F": [6], }, orient='index',
    #                                   dtype=pd.np.float32)
    #     cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))
    #     self.assertTrue(CERO.is_cero(cero))
    #
    #     fc = FromCERO(TestFromCERO._dd + "test_fromcero_mapping.yaml")
    #     fc.exec_procedures(cero)



if script_run:
    unittest.main()
