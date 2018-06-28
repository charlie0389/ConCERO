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
Created on Apr 09 11:19:00 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
script_run = True if __name__ == "__main__" else False

import os
import unittest
import shutil

import numpy as np
import pandas as pd

from concero.tests.data_tools import DefaultTestCase
from concero.cero import CERO
from concero.from_cero import FromCERO
from concero.to_cero import ToCERO
from concero.format_convert_tools import read_yaml
import concero.libfuncs as libfuncs
import concero.conf as cfg


class TestFromCERO_Procedure(DefaultTestCase):
    '''Tests CERO methods.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

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

    def test_load2(self):

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3], "D": [4], "E": [5], "F": [6], }, orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

        fc = FromCERO(cfg.d_td + "test_fromcero_procedureload2.yaml")
        self.assertEqual(fc["procedures"][0]["name"], "Unnamed_proc_0")
        fc.exec_procedures(cero)

        df1 = pd.read_csv("procedureload2.csv", index_col=0)
        test_list = [1, 2, 3]
        df1_vals = [x[0] for x in df1.values.tolist()]
        self.assertTrue(all([np.isclose(x, y) for (x, y) in zip(test_list, df1_vals)]))
        test_list = ["A", "B", "C"]
        self.assertTrue(all([x == y for (x, y) in zip(test_list, df1.index.tolist())]))

        os.remove("procedureload2.csv")

    def test_is_valid(self):

        proc = {"operations": "bad_ops_format"}

        with self.assertRaises(KeyError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": "bad_ops_format", "name": "test_proc"}

        with self.assertRaises(TypeError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": ["bad_op_type"], "name": "no_libfuncs_defined"}

        with self.assertRaises(TypeError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": ["bad_op_type"], "name": "bad_libfuncs_type", "libfuncs": True}

        with self.assertRaises(TypeError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": ["bad_op_type"], "name": "test_proc", "libfuncs": [libfuncs]}

        with self.assertRaises(TypeError):
            FromCERO._Procedure.is_valid(proc)
        self.assertFalse(FromCERO._Procedure.is_valid(proc, raise_exception=False))

        proc = {"operations": [{"func": "replace_har_header_in_file"}], "name": "test_proc", "libfuncs": [libfuncs]}

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
        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3]},
                                      orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

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
                                    "operations": [{"func": "merge"}],
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
                                    "operations": [{"func": "noop",
                                                    "rename": {"b_set": "a_set"}},
                                                   {"func": "pc_change",
                                                    "arrays": ["a_set"],
                                                    "init_cols": [2018]}],
                                    "ref_dir": "."})
        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), "test_stitch_time.csv")}]})
        df = tc.create_cero()

        self.assertTrue(df.equals(test_df))

        os.remove("test_stitch_time.csv")

        proc = FromCERO._Procedure({"name": "test_stitch_time",
                                    "file": "test_stitch_time2.csv",
                                    "sets": {"a_set": ["A", "B", "C"],
                                             "b_set": ["D", "E", "F"]},
                                    "inputs": ["a_set", "b_set"],
                                    "operations": [{"func": "noop",
                                                    "rename": {"b_set": "a_set"}},
                                                   {"func": "pc_change",
                                                    "arrays": ["a_set"],
                                                    "init_cols": 2018}],
                                    "ref_dir": "."})
        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), "test_stitch_time2.csv")}]})
        df = tc.create_cero()

        self.assertTrue(df.equals(test_df))

        os.remove("test_stitch_time2.csv")

        out_file = "test_stitch_time3.csv"
        proc = FromCERO._Procedure({"name": "test_stitch_time",
                                    "file": out_file,
                                    "sets": {"a_set": ["A", "B", "C"],
                                             "b_set": ["D", "E", "F"]},
                                    "inputs": ["a_set", "b_set"],
                                    "operations": [{"func": "noop",
                                                    "rename": {"b_set": "a_set"}},
                                                   {"func": "pc_change",
                                                    "arrays": ["a_set"],
                                                    "init_icols": 0}],
                                    "ref_dir": "."})
        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), out_file)}]})
        df = tc.create_cero()

        self.assertTrue(df.equals(test_df))

        os.remove(out_file)

        out_file = "test_stitch_time4.csv"
        proc = FromCERO._Procedure({"name": "test_stitch_time",
                                    "file": out_file,
                                    "sets": {"a_set": ["A", "B", "C"],
                                             "b_set": ["D", "E", "F"]},
                                    "inputs": ["a_set", "b_set"],
                                    "operations": [{"func": "noop",
                                                    "rename": {"b_set": "a_set"}},
                                                   {"func": "pc_change",
                                                    "arrays": ["a_set"],
                                                    "init_icols": [0]}],
                                    "ref_dir": "."})
        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), out_file)}]})
        df = tc.create_cero()

        self.assertTrue(df.equals(test_df))

        os.remove(out_file)

        out_file = "test_stitch_time5.csv"
        proc = FromCERO._Procedure({"name": "test_stitch_time",
                                    "file": out_file,
                                    "sets": {"a_set": ["A", "B", "C"],
                                             "b_set": ["D", "E", "F"]},
                                    "inputs": ["a_set", "b_set"],
                                    "operations": [{"func": "noop",
                                                    "rename": {"b_set": "a_set"}},
                                                   {"func": "pc_change",
                                                    "arrays": ["a_set"],
                                                    "init_icols": [-3]}],
                                    "ref_dir": "."})
        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), out_file)}]})
        df = tc.create_cero()

        self.assertTrue(df.equals(test_df))

        os.remove(out_file)

    def test_rename(self):

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                       "B": [6, 4, 5, 6, 7],
                                       "C": [4, 5, 8, 7, 8],
                                       "D": [9, 10, 12, 11, 2]},
                                      orient="index",
                                      dtype=pd.np.float32)

        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        cero.sort_index(inplace=True)

        proc = FromCERO._Procedure({"name": "test_proc",
                                    "inputs": ["A", "B", "C", "D"]})
        proc.inputs = cero.copy()
        df = proc._exec_op({"func": "noop"})

        self.assertTrue(df.equals(cero))

        test_df = pd.DataFrame.from_dict({"Z": [6, 4, 5, 6, 7]},
                                            orient="index",
                                            dtype=pd.np.float32)
        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)

        proc = FromCERO._Procedure({"name": "test_proc",
                                    "inputs": ["B"]})
        proc._set_inputs(cero)
        df_new = proc._exec_op({"func": "noop", "rename": "Z"})

        self.assertTrue(df.equals(cero))  # Check cero hasn't been modified
        self.assertTrue(df_new.equals(test_df))

        # Another test...
        test_df = pd.DataFrame.from_dict({"Z": [6, 4, 5, 6, 7],
                                          "Y": [4, 5, 8, 7, 8]},
                                         orient="index",
                                         dtype=pd.np.float32)
        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)

        proc = FromCERO._Procedure({"name": "test_proc",
                                    "inputs": ["B", "C"]})
        proc._set_inputs(cero)
        df_new = proc._exec_op({"func": "noop", "rename": ["Z", "Y"]})

        self.assertTrue(df.equals(cero))  # Check cero hasn't been modified
        self.assertTrue(df_new.equals(test_df.loc[df_new.index.tolist()]))

        # Another test...
        test_df = pd.DataFrame.from_dict({"X": [6, 4, 5, 6, 7],
                                          "Z": [4, 5, 8, 7, 8]},
                                         orient="index",
                                         dtype=pd.np.float32)
        test_df.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        test_df.sort_index(inplace=True)

        proc = FromCERO._Procedure({"name": "test_proc",
                                    "inputs": ["B", "C"]})
        proc._set_inputs(cero)
        df_new = proc._exec_op({"func": "noop", "rename": {"C":"Z", "B":"X"}})

        self.assertTrue(df.equals(cero))  # Check cero hasn't been modified
        self.assertTrue(df_new.equals(test_df.loc[df_new.index.tolist()]))

    def test_load_set_inputs(self):

        cero = pd.DataFrame.from_dict({"A": [1, 2, 3, 4, 5],
                                       "B": [6, 4, 5, 6, 7],
                                       "C": [4, 5, 8, 7, 8],
                                       "D": [9, 10, 12, 11, 2]},
                                      orient="index",
                                      dtype=pd.np.float32)

        cero.columns = pd.DatetimeIndex(pd.to_datetime([2017, 2018, 2019, 2020, 2021], format="%Y"))
        cero.sort_index(inplace=True)

        proc = FromCERO._Procedure({"name": "test_proc",
                             "sets": {"a_set": ["A", "B", "C", "D"]},
                             "inputs": ["a_set"],
                             "operations": [{"func": "noop",
                                             "arrays": ["a_set"]}],
                             "file": "test_load_set_inputs.csv",
                             })
        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), "test_load_set_inputs.csv")}]})
        df = tc.create_cero()

        self.assertTrue(df.equals(cero))

        os.remove("test_load_set_inputs.csv")

    def test_local_libfuncs(self):

        shutil.copy2(TestFromCERO_Procedure._dd + "test_local_libfuncs.py", os.getcwd())

        cero = pd.DataFrame.from_dict({"A": [1], "B": [2], "C": [3]},
                                      orient='index',
                                      dtype=pd.np.float32)
        cero.sort_index(inplace=True)
        cero.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

        test_df = pd.DataFrame.from_dict({"A": [2], "B": [4], "C": [6]},
                                      orient='index',
                                      dtype=pd.np.float32)
        test_df.sort_index(inplace=True)
        test_df.columns = pd.DatetimeIndex(data=pd.to_datetime([2018], format="%Y"))

        proc = FromCERO._Procedure({"libfuncs": "test_local_libfuncs.py",
                             "ref_dir": ".",
                             "name": "test_set",
                             "inputs": ["A", "B", "C"],
                             "operations": [{"func": "test_local_recursive_op"}],
                             "file": "test_local_libfuncs.csv"})

        proc.exec_ops(cero)

        tc = ToCERO({"files": [{"file": os.path.join(os.path.abspath("."), "test_local_libfuncs.csv")}]})
        df = tc.create_cero()

        self.assertTrue(df.equals(test_df))

        os.remove("test_local_libfuncs.py")
        os.remove("test_local_libfuncs.csv")

if script_run:
    unittest.main()
