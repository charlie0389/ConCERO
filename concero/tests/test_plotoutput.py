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
Created on Jan 23 08:29:29 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""

script_run = True if __name__ == "__main__" else False
__name__ = "concero.tests.test_plotoutput"

import os
import unittest

import concero.conf as conf
from concero.from_cero import FromCERO
from concero.cero import CERO
from concero.tests.data_tools import DataTools, DefaultTestCase

class TestPlotOutput(DefaultTestCase):
    '''Tests plot output.'''

    _dd = os.path.join(conf.project_dir, "tests", "data", "")

    def test_plotoutput(self):

        try:
            import seaborn
        except ImportError:
            raise unittest.SkipTest("PyQt4 not installed, and therefore ConCERO's plotting capabilities cannot be used.")

        nf = "AssociateProfessionals.png"

        # CERO path
        png = DataTools.get_test_data(TestPlotOutput._dd + "test_plotoutput.png")

        cero = CERO.read_xlsx(TestPlotOutput._dd + "test_plotoutput.xlsx")
        fc = FromCERO(TestPlotOutput._dd + "test_plotoutput.yaml")
        fc.exec_procedures(cero)
        plt = DataTools.get_test_data(nf)

        # These lines have been commented out because figures are very hard to compare accurately - defaults seem to \
        # differ depending on operating system.
        # try:
        #     self.assertEqual(plt, png)
        # except AssertionError as e:
        #     raise e

        # Tidy up
        os.remove(os.path.relpath(nf))


if script_run:
    unittest.main()
