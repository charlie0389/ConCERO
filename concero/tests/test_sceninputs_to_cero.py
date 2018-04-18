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
