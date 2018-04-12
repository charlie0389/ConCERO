#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from ConCERO.from_cero import FromCERO
from ConCERO.tests.data_tools import DataTools, DefaultTestCase


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
