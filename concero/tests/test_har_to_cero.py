"""
Created on Jan 30 16:13:13 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
script_run = True if __name__ == "__main__" else False
# __name__ = "concero.tests.test_har_to_cero"

import os
import unittest
import shutil

from concero.tests.data_tools import DataTools, DefaultTestCase
from concero.to_cero import ToCERO


class TestHAR2CERO(DefaultTestCase):
    '''Tests the conversion of HAR objects to CERO objects.'''
    _dd = os.path.dirname(__file__) + os.sep + "data" + os.sep

    def test_sceninputs_to_cero(self):
        '''Tests the conversion of hars to ceros.'''

        shutil.copy2(TestHAR2CERO._dd + "Mdatnew7.har", "Mdatnew7.har")

        s2c = ToCERO(conf=(TestHAR2CERO._dd + r'test_har_to_cero.yaml'))
        cero = s2c.create_cero()
        df = DataTools.get_test_data(TestHAR2CERO._dd + r'test_har_to_cero.pickle')

        self.assertTrue(cero.loc[df.index].equals(df)) # Order-independent test

        os.remove("Mdatnew7.har")


    def test_time_dim(self):

        shutil.copy2(TestHAR2CERO._dd + "test_timedim.har", "test_timedim.har")

        h2c = ToCERO(conf=(TestHAR2CERO._dd + r'test_har_to_cero_timedim.yaml'))
        cero = h2c.create_cero()
        df = DataTools.get_test_data(TestHAR2CERO._dd + r'test_har_to_cero_timedim.pickle')

        self.assertTrue(cero.loc[df.index].equals(df)) # Order-independent test

        os.remove("test_timedim.har")


if script_run:
    unittest.main()
