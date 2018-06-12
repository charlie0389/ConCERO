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
Created on Wed Jan 17 08:45:46 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""

import sys
import os
import unittest

import numpy as np

sys.path.append(os.path.relpath('../'))
from concero.from_cero import FromCERO
from concero.tests.data_tools import DataTools, DefaultTestCase


class TestCERO2AusTIMES(DefaultTestCase):
    '''Test the CERO to AusTIMES conversion class.'''

    def test_cero2austimes(self):
        '''Tests CERO2AusTIMES conversion process.
        '''
        dd = os.path.dirname(__file__) + os.sep + "data" + os.sep

        df = DataTools.get_test_data(dd + r'test_cero_to_luto_initialdata.pickle') # Uses same data as LUTO
        c2a = FromCERO(df, conf_file=(dd + r'test_cero_to_austimes.yaml'))

        for series in c2a.series:
            if isinstance(series, dict):
                gen_output_file = series.get('output_file', series.get('name'))
                output_file = series['name']
            elif isinstance(series, str):
                gen_output_file = series
                output_file = series
            gen = np.load(gen_output_file + '.npy')
            old = np.load('test_' + output_file + '.npy')
            self.assertTrue(all(np.isclose(gen, old)))

if __name__ == '__main__':
    unittest.main()
