"""
Provides the identifier class, which performs all string interpretations to provide the appropriate identifier \
from which pulling data out of the CERO is based.

Created on Jan 30 17:34:37 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import itertools as it
import re

class _Identifier(object):

    @staticmethod
    def get_identifiers(string: str, sets: "Dict[str, List[str]]" = None) -> "List[tuple]":
        tupled_name = _Identifier.tupleize_name(string)
        if isinstance(tupled_name, tuple):
            new_fields = []
            for field in tupled_name:
                if field in sets:
                    # field refers to a set
                    new_fields.append(sets[field])
                else:
                    # specific field in set
                    new_fields.append([field])
            return list(it.product(*new_fields))
        elif isinstance(tupled_name, str):
            if tupled_name in sets:
                # tupled_name is a str
                return sets[tupled_name]
            else:
                # specific field in set
                return [tupled_name]
        else:
            raise TypeError("Index field converted to unrecognised type.")

    @staticmethod
    def tupleize_name(name: "Union[str, tuple, list]") -> "Union[tuple, str]":
        """Returns a `tuple` of `str` based on the iterable ``name``, unless ``name`` has a single element, in which \
        case that element is returned. Every `str` in the tuple has preceding and trailing whitespace removed."""

        if name is None:
            return name

        if isinstance(name, str):
            name = name.split(",")

        name = list(name)
        name = [str(x) for x in name] # Ensure all fields are strings
        name = [x.strip() for x in name] # Remove all preceding and trailing whitespace from strings

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

        return _Identifier.tupleize_name(idents)

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
    def unique_id_fields(idents: list, key: int=None):

        if key is not None:
            idents = [id[key] for id in idents if issubclass(type(id), tuple)]

        return list(set(idents))
