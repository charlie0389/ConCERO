"""
Created on Apr 09 11:19:00 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
script_run = True if __name__ == "__main__" else False

import os
import unittest

import numpy as np
import pandas as pd

from concero.tests.data_tools import DefaultTestCase
from concero.cero import CERO
from concero.from_cero import FromCERO


class TestFromCERO_Procedure(DefaultTestCase):
    '''Tests CERO methods.'''
    _dd = os.path.join(os.path.dirname(__file__), "data", "")


    def test_load(self):

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3], "D": [4], "E": [5], "F": [6], }, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))
        self.assertTrue(CERO.is_cero(cero))

        fc = FromCERO(TestFromCERO_Procedure._dd + "test_fromcero_procedureload.yaml")
        fc.exec_procedures(cero)

        df1 = pd.read_csv("procedureload.csv", index_col=0)
        test_list = [1, 2, 3]
        df1_vals = [x[0] for x in df1.values.tolist()]
        self.assertTrue(all([np.isclose(x, y) for (x, y) in zip(test_list, df1_vals)]))
        test_list = ["A", "B", "C"]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df1.index.tolist())]))

        os.remove("procedureload.csv")

    def test_is_valid(self):

        proc = {"operations": "bad_ops_format"}

        with self.assertRaises(KeyError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": "bad_ops_format", "name": "test_proc"}

        with self.assertRaises(TypeError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": ["bad_op_type"], "name": "test_proc"}

        with self.assertRaises(TypeError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": [{"func_is_unspecified": None}], "name": "test_proc"}

        with self.assertRaises(KeyError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": [{"func": "bad_name"}], "name": "test_proc"} # Good op name, but no 'func' keyword

        with self.assertRaises(AttributeError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": [{"func": "replace_har_header_in_file"}], "name": "test_proc"}

        self.assertTrue(FromCERO._Procedure.is_valid(proc))

    def test_export_to_csv(self):

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3], "D": [4], "E": [5], "F": [6], }, orient='index',
                                      dtype=pd.np.float32)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))
        cero.sort_index(inplace=True)
        self.assertTrue(CERO.is_cero(cero))

        fc = FromCERO(TestFromCERO_Procedure._dd + "test_procedure_export_csv.yaml")
        fc.exec_procedures(cero)

        df1 = pd.read_csv("csv_export.csv", index_col=0)
        test_list = [1, 2, 3]
        df1_vals = [x[0] for x in df1.values.tolist()]
        self.assertTrue(all([np.isclose(x, y) for (x, y) in zip(test_list, df1_vals)]))
        test_list = ["A", "B", "C"]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df1.index.tolist())]))

        os.remove("csv_export.csv")

    def test_export_to_xlsx(self):

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3], "D": [4], "E": [5], "F": [6], }, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))
        self.assertTrue(CERO.is_cero(cero))

        fc = FromCERO(TestFromCERO_Procedure._dd + "test_procedure_export_xlsx.yaml")
        fc.exec_procedures(cero)

        df1 = pd.read_excel("xlsx_export.xlsx", index_col=0)
        test_list = [1, 2, 3]
        df1_vals = [x[0] for x in df1.values.tolist()]
        self.assertTrue(all([np.isclose(x, y) for (x, y) in zip(test_list, df1_vals)]))
        test_list = ["A", "B", "C"]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df1.index.tolist())]))

        os.remove("xlsx_export.xlsx")

    def test_auto_export(self):
        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3]}, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))
        self.assertTrue(CERO.is_cero(cero))

        fc = FromCERO(TestFromCERO_Procedure._dd + "test_procedure_autoexport.yaml")
        fc.exec_procedures(cero)

        df1 = pd.read_csv("auto_csv_export.csv", index_col=0)
        test_list = [1, 2, 3]
        df1_vals = [x[0] for x in df1.values.tolist()]
        self.assertTrue(all([np.isclose(x, y) for (x, y) in zip(test_list, df1_vals)]))
        test_list = ["A", "B", "C"]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df1.index.tolist())]))

        df1 = pd.read_excel("auto_xlsx_export.xlsx", index_col=0)
        test_list = [1, 2, 3]
        df1_vals = [x[0] for x in df1.values.tolist()]
        self.assertTrue(all([np.isclose(x, y) for (x, y) in zip(test_list, df1_vals)]))
        test_list = ["A", "B", "C"]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df1.index.tolist())]))

        os.remove("auto_csv_export.csv")
        os.remove("auto_xlsx_export.xlsx")

    def test_output_cero(self):
        cero = pd.DataFrame.from_dict({("A", "1"): [1], ("B", "2"): [2], ("C", "3"): [3]}, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))
        self.assertTrue(CERO.is_cero(cero))

        proc = FromCERO._Procedure({"name": "test_output_cero",
                                    "file": "test_output_cero.csv",
                                    "ref_dir": ".",
                                    "outputs": [("A", 1)]})

        """Because single item in outputs, error may be raised (but shouldn't) on attempting to export a Pandas.Series object instead of a Pandas.DataFrame object."""
        proc.exec_ops(cero)

        df = pd.read_csv("test_output_cero.csv", index_col=0)
        self.assertTrue(df.shape[0] == 1)

        os.remove("test_output_cero.csv")


if script_run:
    unittest.main()
