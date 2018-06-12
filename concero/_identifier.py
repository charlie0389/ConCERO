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
Provides the identifier class, which performs all string interpretations to provide the appropriate identifier \
from which pulling data out of the CERO is based.

Created on Jan 30 17:34:37 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
from collections import OrderedDict
import fnmatch
import itertools as it
import re


class _Identifier(object):

    @staticmethod
    def get_one_to_one_mapping(map_dict: OrderedDict, sets: "Dict[str, List[str]]" = None) -> "List[tuple]":
        old_names, new_names = [list(i) for i in zip(*map_dict.items())]

        assert (all([isinstance(on, (str, tuple)) for on in old_names]))
        _new_names = []
        for nn in new_names:
            if issubclass(type(nn), list):
                _new_names += nn
            else:
                _new_names.append(nn)
        new_names = _new_names

        return _Identifier.get_mapping_dict(old_names, new_names, sets=sets)

    @staticmethod
    def get_mapping_dict(names_old: "Union[str, List[str]]",
                         names_new: "Union[str, List[str]]",
                         sets: "Dict[str, List[str]]" = None) -> "List[tuple]":

        if isinstance(names_old, str):
            names_old = [names_old]
        if isinstance(names_new, str):
            names_new = [names_new]

        names_old = _Identifier.get_all_idents(names_old, sets=sets)
        names_new = _Identifier.get_all_idents(names_new, sets=sets)

        if len(names_old) != len(names_new):
            msg = "'old_names' and 'new_names' must refer to equal numbers of identifiers (otherwise one-to-one mapping cannot be achieved)."
            raise ValueError(msg)

        return OrderedDict(list(zip(names_old, names_new)))

    @staticmethod
    def get_all_idents(strings: "List[str]", sets: "Dict[str, List[str]]" = None, sep: str =",") -> "List[tuple]":

        if not issubclass(type(strings), list):
            msg = "First argument must be a list."
            raise ValueError(msg)

        strings = [_Identifier.get_identifiers(s, sets=sets, sep=sep) for s in strings]
        strings = list(it.chain(*strings))
        return strings

    @staticmethod
    def get_identifiers(string: str, sets: "Dict[str, List[str]]" = None,
                        sep: str=",",
                        universal_set: "List[Union[str, tuple[str]]]"=None) -> "List[tuple]":

        if sets is None:
            sets = {}

        tupled_name = _Identifier.tupleize_name(string, sep=sep)

        tup_f = lambda x: (x,) if issubclass(type(x), str) else x
        tupled_name = tup_f(tupled_name) # Temporarily convert to tuple

        if not isinstance(tupled_name, tuple):
            raise TypeError("Index field converted to unrecognised type.")

        if issubclass(type(universal_set), list):
            universal_set = [tup_f(us) for us in universal_set]

        new_fields = []
        for fno, field in enumerate(tupled_name):
            if field in sets:
                # field refers to a set
                new_fields.append(sets[field])
            elif (universal_set is not None) and (field not in universal_set):
                # Assume field must be glob pattern...

                universal_set = [us for us in universal_set if (len(us) == len(tupled_name))] # Only idents with same number of fields can be considered matched
                matches = _Identifier.get_matching_strs([us[fno] for us in universal_set], field)

                # Uniqify the matches...
                u_matches = []
                u_m_set = set()
                for m in matches:
                    if m not in u_m_set:
                        u_m_set.add(m)
                        u_matches.append(m)

                new_fields.append(u_matches)
            else:
                # specific field in set
                new_fields.append([field])

        f = lambda x: x[0] if len(x)==1 else x # Converts back to string if necessary
        return [f(_id) for _id in list(it.product(*new_fields))]


    @staticmethod
    def tupleize_name(name: "Union[str, tuple, list]", sep=",") -> "Union[tuple, str]":
        """Returns a `tuple` of `str` based on the iterable ``name``, unless ``name`` has a single element, in which \
        case that element is returned. Every `str` in the tuple has preceding and trailing whitespace removed."""

        if name is None:
            return name

        if isinstance(name, str):
            name = name.split(sep)

        name = list(name)
        name = [str(x) for x in name] # Ensure all fields are strings
        name = [x.strip() for x in name] # Remove all preceding and trailing whitespace from strings
        name = [x for x in name if x != ""]  # Drop if empty string

        if len(name) == 1:
            return name[0]
        else:
            return tuple(name)

    @staticmethod
    def prepend_identifier(prefix: str, ident: "Union[str, tuple]") -> tuple:
        if isinstance(ident, str):
            ident = prefix + "," + ident
        elif isinstance(ident, tuple):
            ident = tuple([prefix] + [x for x in ident])
        return _Identifier.tupleize_name(ident)

    @staticmethod
    def lstrip_identifier(strip: str, ident: "Union[str, tuple]") -> tuple:

        if isinstance(ident, str):
            m = re.match(strip + ",", ident)
        elif isinstance(ident, tuple):
            m = re.match(strip, ident[0])
        else:
            raise ValueError("Invalid ident %s." % ident)

        if not m:
            invalid_strip_msg = "String '%s' does not match the start of the identifier." % strip
            raise ValueError(invalid_strip_msg)

        if isinstance(ident, str):
            ident = ident.lstrip(strip + ",")
        elif isinstance(ident, tuple):
            ident = tuple([x for x in ident[1:]])

        return _Identifier.tupleize_name(ident)

    @staticmethod
    def keep_only_fields(field_no: "Union[int, List[int]]",
                         idents: "Union[tuple, List[tuple]]") -> "List[Union[str,tuple]]":

        if not isinstance(idents, list):
            idents = [idents]
        if not issubclass(type(field_no), list):
            field_no = [field_no]

        if any([isinstance(id, str) for id in idents]):
            raise TypeError("Cannot remove any fields from identifier that has only 1 field (%s)." % idents)

        try:
            idents = [_Identifier.tupleize_name(tuple([id[f] for f in field_no])) for id in idents]
        except TypeError as e:
            raise e

        return [_Identifier.tupleize_name(id) for id in idents]

    @staticmethod
    def remove_id_field(field_no: int, idents: "Union[tuple, List[tuple]]") -> tuple:

        if not isinstance(idents, list):
            idents = [idents]

        if any([isinstance(id, str) for id in idents]):
            raise TypeError("Cannot remove field from identsifier that has only 1 field (%s)." % idents)

        try:
            idents = [_Identifier.tupleize_name(id[:field_no] + id[field_no+1:]) for id in idents]
        except TypeError as e:
            raise e

        return _Identifier.tupleize_name(idents)

    @staticmethod
    def unique_id_fields(idents: list, key: "Union[List[int], int]"=None):
        """

        :param idents: A list of _Identifier objects.
        :param key: The zero-indexed number corresponding to the ident field (i.e. a tuple index), which limits the ``idents`` `list`. If `None` (the default), all idents (whether tuple or not) are considered.
        :return: A list of the unique elements of ``idents``, restricted to tuple fields defined by ``key`` (if given).
        """

        if key is not None:
            if issubclass(type(key), int):
                key = [key]

            nids = []
            for id in idents:
                if issubclass(type(id), tuple):
                    try:
                        nids.append(tuple(id[k] for k in key))
                    except IndexError:
                        pass
            idents = nids

        uids = OrderedDict()

        for id in idents:
            uids[id] = True

        return [_Identifier.tupleize_name(n) for n in list(uids.keys())]

    @staticmethod
    def is_valid(ident, raise_exception=True):
        try:
            assert issubclass(type(ident), (str, tuple))
            if issubclass(type(ident), tuple):
                assert all([issubclass(type(f), str) for f in ident])
        except AssertionError:
            if raise_exception:
                raise TypeError("Invalid identifer %s. Identifier is of type %s, not str or tuple of str." % ident)
            return False
        return True

    @staticmethod
    def get_matching_strs(strs: list, pattern):
        """

        :param list strs: A `list` of valid `str`.
        :param pattern: The glob pattern for matching.
        :return list: A filtered `list` - only items of ``idents`` that match ``pattern`` are returned.
        """
        return fnmatch.filter(strs, pattern)
