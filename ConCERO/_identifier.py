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
