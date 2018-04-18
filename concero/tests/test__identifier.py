"""
Created on Mar 27 13:45:58 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import unittest

from concero._identifier import _Identifier
from concero.tests.data_tools import DefaultTestCase


class Test_Identifier(DefaultTestCase):
    '''Test the VURM to CERO conversion class.'''

    _dd = os.path.join(os.path.dirname(__file__),"data","")

    def test_tupleize_name(self):
        res = _Identifier.tupleize_name("abc,def")
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name(["abc", "def"])
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name(("abc", "def"))
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name("abc, def")
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name(["abc", " def"])
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name(("abc", " def"))
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name("abc ,def")
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name(["abc ", " def"])
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name(("abc ", " def"))
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name("abc")
        self.assertEqual(res, "abc")

        res = _Identifier.tupleize_name(["abc"])
        self.assertEqual(res, "abc")

        res = _Identifier.tupleize_name(("abc",))
        self.assertEqual(res, "abc")

        res = _Identifier.tupleize_name((1,))
        self.assertEqual(res, "1")

        res = _Identifier.tupleize_name(None)
        self.assertEqual(res, None)

    def test_lstrip_identifier(self):

        res = _Identifier.lstrip_identifier("abc", "abc,def")
        self.assertEqual(res, "def")

        res = _Identifier.lstrip_identifier("abc", ("abc", "def"))
        self.assertEqual(res, "def")

        res = _Identifier.lstrip_identifier("abc", ("abc", "def", "efg"))
        self.assertEqual(res, ("def", "efg"))

    def test_prepend_identifier(self):
        res = _Identifier.prepend_identifier("abc", "def")
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.prepend_identifier("abc", ("def", "efg"))
        self.assertEqual(res, ("abc", "def", "efg"))


if __name__ == "__main__":
    unittest.main()