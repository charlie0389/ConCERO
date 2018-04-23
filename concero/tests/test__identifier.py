"""
Created on Mar 27 13:45:58 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import unittest
import itertools as it

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

    def test_get_all_idents(self):

        sets = {"a_set": ["A", "B", "C"]}

        with self.assertRaises(ValueError):
            _Identifier.get_all_idents("a_set", sets=sets)

        idents = _Identifier.get_all_idents(["a_set"], sets=sets)
        self.assertEqual(idents, ["A", "B", "C"])

        idents = _Identifier.get_all_idents(["a_set,a_set"], sets=sets)
        self.assertEqual(idents, [("A", "A"), ("A", "B"), ("A", "C"),
                                  ("B", "A"),("B", "B"), ("B", "C"),
                                  ("C", "A"),("C", "B"), ("C", "C")])

        idents = _Identifier.get_all_idents([("a_set", "a_set")], sets=sets)
        self.assertEqual(idents, [("A", "A"), ("A", "B"), ("A", "C"),
                                  ("B", "A"), ("B", "B"), ("B", "C"),
                                  ("C", "A"), ("C", "B"), ("C", "C")])

    def test_mapping_dict(self):
        sets = {"a_set": ["A", "B", "C"]}

        map_dict = _Identifier.get_mapping_dict(sets["a_set"], sets["a_set"])
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

        map_dict = _Identifier.get_mapping_dict(["a_set"], sets["a_set"], sets=sets)
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

        map_dict = _Identifier.get_mapping_dict(sets["a_set"], ["a_set"], sets=sets)
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

        map_dict = _Identifier.get_mapping_dict("a_set", "a_set", sets=sets)
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

    def test_get_one_to_one_mapping(self):

        sets = {"a_set": ["A", "B", "C"]}

        map_dict = _Identifier.get_one_to_one_mapping(sets, sets=sets)
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

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