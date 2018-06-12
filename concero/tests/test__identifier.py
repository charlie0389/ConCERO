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

        fil_set = _Identifier.get_matching_strs(universal_set, "*")
        self.assertEqual(fil_set, ["abc", "abd", "def", "1ab", "123", "de3"])

        fil_set = _Identifier.get_matching_strs(universal_set, "ab*")
        self.assertEqual(fil_set, ["abc", "abd"])

        fil_set = _Identifier.get_matching_strs(universal_set, "*3")
        self.assertEqual(fil_set, ["123", "de3"])

        fil_set = _Identifier.get_matching_strs(universal_set, "1*")
        self.assertEqual(fil_set, ["1ab", "123"])

        fil_set = _Identifier.get_matching_strs(universal_set, "de[f3]")
        self.assertEqual(fil_set, ["def", "de3"])

        fil_set = _Identifier.get_matching_strs(universal_set, "f*")
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

    def test_unique_id_fields(self):

        idents = ["a", ("a", "b"), ("a", "b", "c"), ("c", "d"), ("c", "e")]

        uids = _Identifier.unique_id_fields(idents=idents)
        self.assertEqual(uids, idents)

        uids = _Identifier.unique_id_fields(idents=idents, key=0)
        self.assertEqual(uids, ["a", "c"])

        uids = _Identifier.unique_id_fields(idents=idents, key=1)
        self.assertEqual(uids, ["b", "d", "e"])

        uids = _Identifier.unique_id_fields(idents=idents, key=2)
        self.assertEqual(uids, ["c"])

        uids = _Identifier.unique_id_fields(idents=idents, key=[0, 1])
        self.assertEqual(uids, [("a", "b"), ("c", "d"), ("c", "e")])

    def test_keep_only_fields(self):

        idents = [("a", "b"), ("a", "b", "c"), ("c", "d"), ("c", "e")]

        ni = _Identifier.keep_only_fields(field_no=0, idents=idents)
        self.assertEqual(ni, ["a", "a", "c", "c"])

        ni = _Identifier.keep_only_fields(field_no=1, idents=idents)
        self.assertEqual(ni, ["b", "b", "d", "e"])

        ni = _Identifier.keep_only_fields(field_no=[0,1], idents=idents)
        self.assertEqual(ni, [("a", "b"), ("a", "b"), ("c", "d"), ("c", "e")])


if __name__ == "__main__":
    unittest.main()