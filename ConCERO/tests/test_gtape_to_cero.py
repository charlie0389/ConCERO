#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:31:57 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""

import sys
import os
import unittest
sys.path.append(os.path.relpath('../'))
from ConCERO.to_cero import ToCERO
from ConCERO.tests.data_tools import DataTools, DefaultTestCase


class TestGTAPE2CERO(DefaultTestCase):
    '''Test the VURM to CERO conversion class.'''

    def test_gtape2cero(self):
        '''Tests VURM2CERO conversion process.'''

        dd = os.path.join(os.path.dirname(__file__), "data", "")

        g2c = ToCERO(dd + r'test_gtape_to_cero.yaml')
        cero = g2c.create_cero()
        df = DataTools.get_test_data(dd + r'test_gtape_to_cero_finaldata.pickle')

        self.assertTrue(cero.equals(df))

if __name__ == '__main__':
    unittest.main()
