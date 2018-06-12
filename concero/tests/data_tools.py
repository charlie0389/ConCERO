#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
Created on Fri Dec 22 09:06:22 2017

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
import os
import pickle
import yaml
import unittest

import pandas as pd

import concero.conf as conf
if getattr(conf, "harpy_installed", False):
    import harpy

class DataTools(object):

    @staticmethod
    def get_test_data(filename, *args, header_name: str = None, **kwargs):
        filename = conf.find_file(filename)
        ext = os.path.splitext(filename)[1][1:]

        if ext == 'pickle':
            lib = pickle
            with open(filename, 'rb') as inf:
                test_data = lib.load(inf)

            if isinstance(test_data, pd.DataFrame):
                test_data = test_data.astype(pd.np.float32, copy=False)
                # dataframe needs to be of same datatype for equals comparison to be true

        elif ext == 'yaml':
            lib = yaml
            with open(filename, 'rb') as inf:
                test_data = lib.load(inf)
        elif ext == 'gdx':
            pass
        elif ext in ["har", "shk"]:
            har = harpy.HarFileObj.loadFromDisk(filename=filename)
            if header_name is not None:
                test_data = har.getHeaderArrayObj(header_name)
            else:
                test_data = har
        elif ext in ["png"]:
            with open(filename, "rb") as f:
                return f.read()

        return test_data

class DefaultTestCase(unittest.TestCase):

    def setUp(self):
        # conf.set_log_level("DEBUG")
        # conf.add_search_path(os.path.join(os.path.dirname(__file__), ""))
        pass

    def tearDown(self):
        # conf.rm_search_path()
        pass
