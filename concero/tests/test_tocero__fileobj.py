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
Created on Apr 09 10:41:37 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import unittest
import shutil
import sys
import pickle

import pandas as pd

import concero.conf
from concero.to_cero import ToCERO
from concero.cero import CERO
from concero.tests.data_tools import DataTools, DefaultTestCase


class TestToCERO_FileObj(DefaultTestCase):

    _dd = os.path.join(os.path.dirname(__file__),"data","")

    def test_load_config(self):

        conf = "non_existent_conf_file.yaml"

        with self.assertRaises(FileNotFoundError):
            ToCERO._FileObj.load_config(conf)

        parent = {'search_paths': [TestToCERO_FileObj._dd]}
        conf = "test__fileobj_load_config.yaml"

        fo = ToCERO._FileObj.load_config(conf, parent=parent)

        conf = {"file": os.path.abspath(TestToCERO_FileObj._dd + "test_csv.csv")}

        fo = ToCERO._FileObj.load_config(conf)

        self.assertTrue("file" in fo)
        self.assertTrue(fo["file"]) # Checks string is non-empty
        self.assertTrue(fo["type"] == "csv")
        self.assertTrue(fo["search_paths"] == [os.path.abspath(".")])

    def test_is_valid(self):

        conf = {"No file key...": None}

        with self.assertRaises(TypeError):
            ToCERO._FileObj.is_valid(conf)

        self.assertFalse(ToCERO._FileObj.is_valid(conf, raise_exception=False))

        conf = {"file": None} # Invalid value for key "file"

        with self.assertRaises(TypeError):
            ToCERO._FileObj.is_valid(conf)

        self.assertFalse(ToCERO._FileObj.is_valid(conf, raise_exception=False))

        conf = {"file": "a file name"}

        self.assertTrue(ToCERO._FileObj.is_valid(conf))

    @unittest.skipIf(sys.platform.startswith("win"), " Impossible to disable read with os.chmod() on windows.")
    def test_run_checks(self):
        conf = {"file": "not_a_valid_file.file", "search_paths": [os.path.abspath(".")]}

        with self.assertRaises(FileNotFoundError):
            ToCERO._FileObj.run_checks(conf)

        self.assertFalse(ToCERO._FileObj.run_checks(conf, raise_exception=False))

        conf = {"file": "test_csv_noread.csv", "search_paths": [os.path.abspath(".")]}

        try:

            shutil.copy2(TestToCERO_FileObj._dd + "test_csv.csv", os.path.join(os.path.abspath("."), "test_csv_noread.csv"))
            os.chmod("test_csv_noread.csv", 0o000)

            with self.assertRaises(PermissionError):
                ToCERO._FileObj.run_checks(conf)

            self.assertFalse(ToCERO._FileObj.run_checks(conf, raise_exception=False))

        finally:
            os.remove("test_csv_noread.csv")

        conf = {"file": TestToCERO_FileObj._dd + "test_csv.csv", "search_paths": [os.path.abspath(".")]}

        self.assertTrue(ToCERO._FileObj.run_checks(conf))

    def test_har_repetitive_sets(self):

        fo = ToCERO._FileObj({"file": "test.har",
                "search_paths": TestToCERO_FileObj._dd,
                "head_arrs": [{"name": "ARR7", "default_year": 2018}]})
        cero = fo.import_file_as_cero()

        df = DataTools.get_test_data(TestToCERO_FileObj._dd + "test_har_repetitive_sets.pickle")

        self.assertTrue(cero.equals(df))

    def test__import_vd(self):

        fo = {"file": TestToCERO_FileObj._dd + "test__import_vd.VD",
              "date_col": 3,
              "val_col": 8}

        fo = ToCERO._FileObj(fo)
        df = fo._import_vd()
        df.columns.set_names([None], inplace=True)
        df = df.astype(pd.np.float32)

        test_df = pd.DataFrame.from_dict({("VAR_Act", "-", "FT_COMELC", "ACT", "2015", "PD", "-"):
                                              [0.740833333333336, 0.740833333333336, 0.8005115537522, 0.829127920241238]},
                                         orient="index",
                                    dtype=pd.np.float32)
        test_df.columns = pd.Index([2015, 2016, 2020, 2025])
        test_df.sort_index(inplace=True)

        self.assertTrue(test_df.equals(df))

        fo = {"file": TestToCERO_FileObj._dd + "test__import_vd.VD",
              "date_col": 3,
              "val_col": 8,
              "default_year": 2018}

        fo = ToCERO._FileObj(fo)
        df = fo._import_vd()
        df.columns.set_names([None], inplace=True)
        df = df.astype(pd.np.float32)
        df.sort_index(inplace=True)

        test_df = pd.DataFrame(data=[[0.740833333333336, 0.740833333333336, pd.np.nan, 0.8005115537522,
                                               0.829127920241238],
                                     [pd.np.nan, pd.np.nan, 1.39891653080538, pd.np.nan, pd.np.nan],
                                     [pd.np.nan, pd.np.nan, 19.6047685777802, pd.np.nan, pd.np.nan],
                                     [pd.np.nan, pd.np.nan, 31516.8951973493, pd.np.nan, pd.np.nan],
                                     ],
                               columns=[2015, 2016, 2018, 2020, 2025],
                               dtype=pd.np.float32)
        test_df.index = CERO.create_cero_index([("VAR_Act", "-", "FT_COMELC", "ACT", "2015", "PD", "-"),
                                                ("Cost_Salv", "-", "EN_WinONS-26", "ADE", "2040", "-", "-"),
                                                ("Cost_NPV", "-", "EE_StmTurb009", "CQ", "-", "-", "ACT"),
                                                ("Reg_irec", "-", "-", "WA", "-", "-", "-"),
                                                ])
        test_df.sort_index(inplace=True)
        self.assertTrue(test_df.equals(df))

    @unittest.skipIf(not concero.conf.gdxpds_installed, "gdxpds not installed")
    def test__import_gdx(self):

        fo = {"file": TestToCERO_FileObj._dd + "test__import_gdx.gdx",
              "symbols": {"name": "L_EXPORT", "date_col": 2}}
        fo = ToCERO._FileObj(fo)
        df = fo._import_gdx()

        with open(TestToCERO_FileObj._dd + "test__import_gdx.pickle", "rb") as f:
            test_df = pickle.load(f)

        self.assertTrue(df.equals(test_df))

    @unittest.skipIf(not concero.conf.gdxpds_installed, "gdxpds not installed")
    def test_gtape2cero(self):

        dd = os.path.join(os.path.dirname(__file__), "data", "")

        g2c = ToCERO(dd + r'test_gtape_to_cero.yaml')
        cero = g2c.create_cero()
        df = DataTools.get_test_data(dd + r'test_gtape_to_cero_finaldata.pickle')

        self.assertTrue(cero.equals(df))


if __name__ == "__main__":
    unittest.main()