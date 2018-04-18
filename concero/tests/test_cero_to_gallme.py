"""
Created on Jan 23 08:29:29 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
import os
import unittest

import numpy as np

import concero.conf as conf
from concero.from_cero import FromCERO
from concero.tests.data_tools import DataTools, DefaultTestCase


class TestCERO2GALLME(DefaultTestCase):
    '''Test the CERO to GALLME conversion class.'''

    @unittest.skipIf(not getattr(conf, "gdxpds_installed", True), "Skip if gdxpds is known not to be installed.")
    def test_cero2gallme(self):
        '''Tests CERO2GALLME conversion process. Tests procedure but not output to file.
        '''

        dd = os.path.dirname(__file__) + os.sep + "data" + os.sep

        df = DataTools.get_test_data(dd + r'test_cero_to_gallme_initialdata.pickle')

        c2g = FromCERO(dd + r'test_cero_to_gallme.yaml')
        c2g.exec_procedures(df)

        ser_a = df.loc[(("L_OUTPUT", "Electricity", "CAF"),),].iloc[0] + \
                df.loc[(("L_OUTPUT", "Electricity", "NAF"),),].iloc[0] + \
                df.loc[(("L_OUTPUT", "Electricity", "OSA"),),].iloc[0] + \
                df.loc[(("L_OUTPUT", "Electricity", "ZAF"),),].iloc[0]
        ser_b = df.loc[(("qo", "Electricity", "CAF"),),].iloc[0] + \
                df.loc[(("qo", "Electricity", "NAF"),),].iloc[0] + \
                df.loc[(("qo", "Electricity", "OSA"),),].iloc[0] + \
                df.loc[(("qo", "Electricity", "ZAF"),),].iloc[0]

        ser_b = ser_a * ser_b
        self.assertTrue(np.allclose(ser_b.values, c2g.output_procedures['DemandYearly']["Value"].values))

        os.remove("gallme_input_data.gdx") # Tidy up

if __name__ == '__main__':
    unittest.main()
