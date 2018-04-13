script_run = True if __name__ == "__main__" else False

import unittest


from ConCERO.tests.test_plotoutput import TestPlotOutput
from ConCERO.tests.test_har_to_cero import TestHAR2CERO
from ConCERO.tests.test_replace_har_header_in_file import TestHARHeaderReplace
from ConCERO.tests.test_scenario import TestScenario
from ConCERO.tests.test_vurm_to_cero import TestVURM2CERO
from ConCERO.tests.test_sceninputs_to_cero import TestScenIn2CERO
from ConCERO.tests.test_libfuncs import TestLibfuncs
from ConCERO.tests.test_gtape_to_cero import TestGTAPE2CERO
from ConCERO.tests.test_cero_to_luto import TestCERO2LUTO
from ConCERO.tests.test_cero_to_gallme import TestCERO2GALLME
# from ConCERO.tests.test_cero_to_austimes import TestCERO2AusTIMES
from ConCERO.tests.test_cero_to_har import TestCERO2HAR
from ConCERO.tests.test_cero import TestCERO
from ConCERO.tests.test_libfuncs_wrappers import TestLibfuncsWrappers
from ConCERO.tests.test_tocero import TestToCERO
from ConCERO.tests.test_tocero__fileobj import TestToCERO_FileObj
from ConCERO.tests.test_fromcero import TestFromCERO
from ConCERO.tests.test_fromcero__procedure import TestFromCERO_Procedure
from ConCERO.tests.test__identifier import Test_Identifier
from ConCERO.tests.test_main import TestMain

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
                         TestCERO2GALLME,
                         TestCERO2LUTO,
                     ):
            self.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(testcase))

if script_run:
    runner = unittest.TextTestRunner()
    runner.run(TestConCERO())