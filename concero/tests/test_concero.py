script_run = True if __name__ == "__main__" else False

import unittest


from concero.tests.test_plotoutput import TestPlotOutput
from concero.tests.test_har_to_cero import TestHAR2CERO
from concero.tests.test_replace_har_header_in_file import TestHARHeaderReplace
from concero.tests.test_scenario import TestScenario
from concero.tests.test_vurm_to_cero import TestVURM2CERO
from concero.tests.test_sceninputs_to_cero import TestScenIn2CERO
from concero.tests.test_libfuncs import TestLibfuncs
from concero.tests.test_gtape_to_cero import TestGTAPE2CERO
from concero.tests.test_cero_to_luto import TestCERO2LUTO
from concero.tests.test_cero_to_gallme import TestCERO2GALLME
# from concero.tests.test_cero_to_austimes import TestCERO2AusTIMES
from concero.tests.test_cero_to_har import TestCERO2HAR
from concero.tests.test_cero import TestCERO
from concero.tests.test_libfuncs_wrappers import TestLibfuncsWrappers
from concero.tests.test_tocero import TestToCERO
from concero.tests.test_tocero__fileobj import TestToCERO_FileObj
from concero.tests.test_fromcero import TestFromCERO
from concero.tests.test_fromcero__procedure import TestFromCERO_Procedure
from concero.tests.test__identifier import Test_Identifier
from concero.tests.test_main import TestMain

class TestConCERO(unittest.TestSuite):
    """TestConCERO is a unittest.TestSuite, which provides an easy access point to run all the tests.
    """

    def __init__(self):
        super().__init__()
        for testcase in (TestPlotOutput, TestHAR2CERO, TestHARHeaderReplace, TestVURM2CERO, TestScenIn2CERO,
                         TestLibfuncs,
                         TestLibfuncsWrappers,
                         TestScenario,
                         TestCERO,
                         TestCERO2HAR,
                         TestToCERO,
                         TestFromCERO,
                         Test_Identifier,
                         TestToCERO_FileObj,
                         TestFromCERO_Procedure,
                         TestMain,
                         TestGTAPE2CERO,
                         # TestCERO2GALLME,
                         TestCERO2LUTO,
                     ):
            self.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(testcase))

if script_run:
    runner = unittest.TextTestRunner()
    runner.run(TestConCERO())