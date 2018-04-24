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
from concero.to_cero import ToCERO
from concero.format_convert_tools import read_yaml
import concero.conf as cfg


class TestFromCERO_Procedure(DefaultTestCase):
    '''Tests CERO methods.'''

    def test_load(self):

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3], "D": [4], "E": [5], "F": [6], }, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

        fc = FromCERO(cfg.d_td + "test_fromcero_procedureload.yaml")
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

        fc = FromCERO(cfg.d_td + "test_procedure_export_csv.yaml")
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

        proc = FromCERO._Procedure(read_yaml(cfg.d_td + "test_procedure_export_xlsx.yaml"))
        proc.exec_ops(cero)

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

        fc = FromCERO(cfg.d_td + "test_procedure_autoexport.yaml")
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
        """
        Tests the behaviour of the "outputs" argument is correct.
        """

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3]}, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

        proc = FromCERO._Procedure({"name": "test_output_cero",
                                    "file": "test_output_cero.csv",
                                    "inputs": ["A", "B", "C"],
                                    "ref_dir": ".",
                                    "outputs": ["A"]})

        """Because single item in outputs, error may be raised (but shouldn't) on attempting to export a Pandas.Series object instead of a Pandas.DataFrame object."""
        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."),"test_output_cero.csv")}]})
        df = tc.create_cero()

        self.assertTrue(cero.loc[["A"]].equals(df))

        # Another test...
        proc = FromCERO._Procedure({"name": "test_output_cero",
                                    "file": "test_output_cero2.csv",
                                    "inputs": ["A", "B", "C"],
                                    "ref_dir": ".",
                                    "outputs": True})

        """Because single item in outputs, error may be raised (but shouldn't) on attempting to export a Pandas.Series object instead of a Pandas.DataFrame object."""
        proc.exec_ops(cero)
        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), "test_output_cero2.csv")}]})
        df = tc.create_cero()
        self.assertTrue(cero.equals(df))

        # Another test...
        proc = FromCERO._Procedure({"name": "test_output_cero",
                                    "file": "test_output_cero3.csv",
                                    "inputs": ["A", "B", "C"],
                                    "ref_dir": ".",
                                    "outputs": None})

        """Because single item in outputs, error may be raised (but shouldn't) on attempting to export a Pandas.Series object instead of a Pandas.DataFrame object."""
        proc.exec_ops(cero)
        self.assertFalse(os.path.isfile("test_output_cero3.csv"))

        # Another test...
        proc = FromCERO._Procedure({"name": "test_output_cero",
                                    "file": "test_output_cero4.csv",
                                    "inputs": ["A", "B", "C"],
                                    "ref_dir": ".",
                                    "outputs": False})

        """Because single item in outputs, error may be raised (but shouldn't) on attempting to export a Pandas.Series object instead of a Pandas.DataFrame object."""
        proc.exec_ops(cero)
        self.assertFalse(os.path.isfile("test_output_cero4.csv"))


        # Another test...
        proc = FromCERO._Procedure({"name": "test_output_cero",
                                    "file": "test_output_cero5.csv",
                                    "inputs": ["A", "B", "C"],
                                    "ref_dir": "."})

        """Because single item in outputs, error may be raised (but shouldn't) on attempting to export a Pandas.Series object instead of a Pandas.DataFrame object."""
        proc.exec_ops(cero)
        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), "test_output_cero2.csv")}]})
        df = tc.create_cero()
        self.assertTrue(cero.equals(df))

        os.remove("test_output_cero.csv")
        os.remove("test_output_cero2.csv")
        os.remove("test_output_cero5.csv")

    def test_load_sets_from_file(self):
        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3]}, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

        proc = FromCERO._Procedure({"sets": {"a_set": cfg.d_td + "test_set.yaml"},
                                    "ref_dir": ".",
                                    "name": "test_set",
                                    "inputs": ["a_set"],
                                    "file": "test_sets.csv"})
        proc.exec_ops(cero)
        new_df = pd.read_csv("test_sets.csv", index_col=0)

        test_labels = ["A", "B"]
        test_vals = [[1], [2]]

        self.assertTrue(new_df.index.tolist() == test_labels)
        self.assertTrue(new_df.values.tolist() == test_vals)

        os.remove("test_sets.csv")

    def test_exec_ops(self):

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3]}, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

        proc = FromCERO._Procedure({"name": "test_output_cero",
                                    "file": "test_output_cero5.csv",
                                    "inputs": ["A", "B", "C"],
                                    "operations": [{"func": "merge_new"}],
                                    "ref_dir": "."})

    def test_stitch_time(self):

        init = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3],
                                       }, orient='index',
                                      dtype=pd.np.float32)
        init.sort_index(inplace=True)
        init.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

        cero = pd.DataFrame.from_dict({"D": [100, 200], "E": [50, 0], "F": [-50, 200]},
                                      orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2019, 2020], format="%Y"))

        cero = CERO.combine_ceros([init, cero])

        test_df = pd.DataFrame.from_dict({"A": [1, 2, 6], "B": [2, 3, 3], "C": [3, 1.5, 4.5],
                                          "D": [pd.np.nan, 100, 200], "E": [pd.np.nan, 50, 0], "F": [pd.np.nan, -50, 200]
                                          },
                                      orient='index',
                                      dtype=pd.np.float32)
        test_df.sort_index(inplace=True)
        test_df.columns = pd.DatetimeIndex(data=pd.to_datetime([2018, 2019, 2020], format="%Y"))

        proc = FromCERO._Procedure({"name": "test_stitch_time",
                                    "file": "test_stitch_time.csv",
                                    "sets": {"a_set": ["A", "B", "C"],
                                             "b_set": ["D", "E", "F"]},
                                    "inputs": ["a_set", "b_set"],
                                    "operations": [{"func": "nop",
                                                    "rename": {"b_set": "a_set"},
                                                    "sets": {"a_set": ["A", "B", "C"],
                                                    "b_set": ["D", "E", "F"]},
                                                    },
                                                   {"func": "pc_change",
                                                    "arrays": ["a_set"],
                                                    "init_cols": [2018],
                                                    },
                                                   ],
                                    "ref_dir": "."})
        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), "test_stitch_time.csv")}]})
        df = tc.create_cero()

        self.assertTrue(df.equals(test_df))


if script_run:
    unittest.main()
