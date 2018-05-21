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

        res = _Identifier.tupleize_name("abc,")
        self.assertEqual(res, "abc")

        res = _Identifier.tupleize_name(["abc", ""])
        self.assertEqual(res, "abc")

        res = _Identifier.tupleize_name(("abc", ""))
        self.assertEqual(res, "abc")

        res = _Identifier.tupleize_name("abc;def", sep=";")
        self.assertEqual(res, ("abc", "def"))

        res = _Identifier.tupleize_name("abc;", sep=";")
        self.assertEqual(res, "abc")

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
        sets = {"a_set": ["A", "B", "C"],
                "bad_set": ["A", "B", "C", "A"]}

        map_dict = _Identifier.get_mapping_dict(sets["a_set"], sets["a_set"])
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

        map_dict = _Identifier.get_mapping_dict(["a_set"], sets["a_set"], sets=sets)
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

        map_dict = _Identifier.get_mapping_dict(sets["a_set"], ["a_set"], sets=sets)
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

        map_dict = _Identifier.get_mapping_dict("a_set", "a_set", sets=sets)
        self.assertEqual(map_dict, {"A": "A", "B": "B", "C": "C"})

        map_dict = _Identifier.get_mapping_dict(sets["bad_set"], sets["bad_set"])
        self.assertNotEqual(4, len(map_dict.keys()))

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

    def test_get_matching_idents(self):
        universal_set = ["abc", "abd", "def", "1ab", "123", "de3"]

        fil_set = _Identifier.get_matching_idents(universal_set, "*")
        self.assertEqual(fil_set, ["abc", "abd", "def", "1ab", "123", "de3"])

        fil_set = _Identifier.get_matching_idents(universal_set, "ab*")
        self.assertEqual(fil_set, ["abc", "abd"])

        fil_set = _Identifier.get_matching_idents(universal_set, "*3")
        self.assertEqual(fil_set, ["123", "de3"])

        fil_set = _Identifier.get_matching_idents(universal_set, "1*")
        self.assertEqual(fil_set, ["1ab", "123"])

        fil_set = _Identifier.get_matching_idents(universal_set, "de[f3]")
        self.assertEqual(fil_set, ["def", "de3"])

        fil_set = _Identifier.get_matching_idents(universal_set, "f*")
        self.assertEqual(fil_set, [])

    def test_get_identifiers(self):

        uset = ["a", "b",
               ("a", "b"),
               ("a", "b", "c"),
               ("d", "b", "c"),
               ("a", "d", "c"),
               ("d", "d", "c"),
               ("a", "b", "d"),
               ("d", "b", "d"),
               ("a", "d", "d"),
               ("d", "d", "d")]

        fil_ids = _Identifier.get_identifiers("*", universal_set=uset)
        self.assertEqual(fil_ids, ["a", "b"])

        fil_ids = _Identifier.get_identifiers("*,b,c", universal_set=uset)
        self.assertEqual(fil_ids, [("a", "b", "c"), ("d", "b", "c")])

        fil_ids = _Identifier.get_identifiers("a,*,c", universal_set=uset)
        self.assertEqual(fil_ids, [("a", "b", "c"), ("a", "d", "c")])

        fil_ids = _Identifier.get_identifiers("a,b,*", universal_set=uset)
        self.assertEqual(fil_ids, [("a", "b", "c"), ("a", "b", "d")])

        fil_ids = _Identifier.get_identifiers("a,b", universal_set=uset)
        self.assertEqual(fil_ids, [("a", "b")])


if __name__ == "__main__":
    unittest.main()