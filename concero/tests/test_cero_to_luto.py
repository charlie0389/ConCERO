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
Created on Fri Dec 22 09:04:58 2017

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
import os
import unittest

import numpy as np

from concero.from_cero import FromCERO
from concero.tests.data_tools import DataTools, DefaultTestCase


class TestCERO2LUTO(DefaultTestCase):
    '''Test the CERO to LUTO conversion class.'''

    def test_cero2luto(self):
        '''Tests CERO2LUTO conversion process.
        '''

        dd = os.path.join(os.path.dirname(__file__), "data", "")

        df = DataTools.get_test_data(dd + "test_cero_to_luto_initialdata.pickle")
        c2l = FromCERO(dd + r'test_cero_to_luto.yaml')
        c2l.exec_procedures(df)

        for procedure in c2l["procedures"]:
            if isinstance(procedure, dict):
                gen_output_file = procedure.get('output_file', procedure.get('name'))
                output_file = procedure['name']
            elif isinstance(procedure, str):
                gen_output_file = procedure
                output_file = procedure
            gen = np.load(gen_output_file + '.npy')[0]
            old = np.load(dd + 'test_' + output_file + '.npy')
            self.assertTrue(all(np.isclose(gen, old)))
            os.remove(gen_output_file + '.npy')

if __name__ == '__main__':
    unittest.main()
