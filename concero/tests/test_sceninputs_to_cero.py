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
Created on Jan 25 13:32:30 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import os
import unittest

import pandas as pd

from concero.to_cero import ToCERO
from concero.tests.data_tools import DataTools, DefaultTestCase


class TestScenIn2CERO(DefaultTestCase):
    '''Test xlsx/csv to CERO conversion.'''

    _dd = os.path.dirname(__file__) + os.sep + "data" + os.sep

    def test_sceninputs_to_cero(self):
        '''Test xlsx/csv to CERO conversion.'''

        s2c = ToCERO(conf=(TestScenIn2CERO._dd + r'test_sceninputs_to_cero.yaml'))
        cero = s2c.create_cero()
        df = DataTools.get_test_data(TestScenIn2CERO._dd + r'test_sceninputs_to_cero.pickle')

        self.assertTrue(cero.loc[df.index].equals(df))  # Order-independent test

    def test_sceninputs_to_cero2(self):
        '''Test xlsx to CERO conversion.'''
        s2c = ToCERO(conf=(TestScenIn2CERO._dd + 'test_xlsx_to_cero.yaml'))
        cero = s2c.create_cero()
        df = DataTools.get_test_data(os.path.normpath('data/test_xlsx_to_cero.pickle'))

        self.assertTrue(cero.loc[df.index].equals(df))  # Order-independent test

if __name__ == '__main__':
    unittest.main()
