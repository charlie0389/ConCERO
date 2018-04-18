#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
