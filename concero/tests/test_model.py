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
Created on Jun 14 11:07:44 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import unittest
import shutil

import numpy as np
import harpy

import concero.conf
from concero.model import Model
from concero.tests.data_tools import DefaultTestCase


class TestModel(DefaultTestCase):
    '''Tests Scenario-related methods.'''

    _dd = os.path.join(os.path.dirname(__file__), "data", "")

    def test_isvalid(self):
        '''Tests a scenario run.'''

        # Load Model
        m = Model({})
        m.pop("name") # To deliberately create invalid model.

        with self.assertRaises(TypeError, msg="All models must have all of the keys: ['name', 'cmds', 'input_conf', 'output_conf']. Attempted to create model with at least one of these keys missing."):
            m.is_valid()

        m = Model({"name": "test_model", "cmds": "a cmd"})

        self.assertTrue(m.is_valid())

if __name__ == '__main__':
    unittest.main()
