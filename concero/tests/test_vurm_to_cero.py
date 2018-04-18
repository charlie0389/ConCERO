#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:31:57 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
import os
import unittest

from concero.to_cero import ToCERO
from concero.tests.data_tools import DataTools, DefaultTestCase


class TestVURM2CERO(DefaultTestCase):
    '''Test the VURM to CERO conversion class.'''

    _dd = os.path.dirname(__file__) + os.sep + "data" + os.sep

    def test_vurm2cero(self):
        '''Tests VURM2CERO conversion process.'''

        v2c = ToCERO(conf=(TestVURM2CERO._dd + r'test_vurm_to_cero.yaml'))
        cero = v2c.create_cero()
        df = DataTools.get_test_data(TestVURM2CERO._dd + r'test_vurm_to_cero_finaldata.pickle')

        self.assertTrue(cero.equals(df))


if __name__ == "__main__":
    unittest.main()
