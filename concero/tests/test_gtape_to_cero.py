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
Created on Mon Jan 15 11:31:57 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""

import sys
import os
import unittest

import concero.conf
from concero.to_cero import ToCERO
from concero.tests.data_tools import DataTools, DefaultTestCase


class TestGTAPE2CERO(DefaultTestCase):
    '''Test the VURM to CERO conversion class.'''

    @unittest.skipIf(not concero.conf.gdxpds_installed, "gdxpds not installed")
    def test_gtape2cero(self):
        '''Tests VURM2CERO conversion process.'''

        dd = os.path.join(os.path.dirname(__file__), "data", "")

        g2c = ToCERO(dd + r'test_gtape_to_cero.yaml')
        cero = g2c.create_cero()
        df = DataTools.get_test_data(dd + r'test_gtape_to_cero_finaldata.pickle')

        self.assertTrue(cero.equals(df))

if __name__ == '__main__':
    unittest.main()
