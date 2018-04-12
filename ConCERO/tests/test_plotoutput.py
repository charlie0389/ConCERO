"""
Created on Jan 23 08:29:29 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""

script_run = True if __name__ == "__main__" else False
# print(__name__)
__name__ = "ConCERO.tests.test_plotoutput"
# print(__name__)
# print(__file__)
# print(__package__)
# print(__spec__)
# import sys
# #print(sys.modules)
# print(sys.meta_path)

import os
import unittest

import ConCERO.conf as conf
from ConCERO.from_cero import FromCERO
from ConCERO.cero import CERO
from ConCERO.tests.data_tools import DataTools, DefaultTestCase

class TestPlotOutput(DefaultTestCase):
    '''Tests plot output.'''

    _dd = os.path.join(conf.project_dir, "tests", "data", "")

    def test_plotoutput(self):
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
