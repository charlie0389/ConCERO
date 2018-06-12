#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
.. cero:

A core concept in the operation of ConCERO is that of a 'Collins Economic Results Object' - a CERO - which \
serves as a standard format for data-interchange between economic modelling programs. Conceptually, the CERO \
is a set of instances of a 'fundamental data type', a discussion of which can be found in the :ref:`Design_Philosophy` \
documentation.

Software-wise, the CERO is a ``pandas.DataFrame`` with some additional constraints. Those constraints are:

    * ``cero.index`` must be an instance of the ``pandas.Index`` class, and
    * ``cero.columns`` must be an instance of the ``pandas.DatetimeIndex`` class, and
    * both ``cero.index`` and ``cero.columns`` values must be unique and
    * all index values must be valid *identifiers* (see below) and
    * ``cero`` data/array values must all be of 32-bit floating-point type (specifically, be instances of a \
    subclass of the ``numpy.float32`` class),

where ``cero`` is a CERO. The values of ``cero.index`` are referred as *identifiers*.

.. _cero_ids:

CERO Identifiers
----------------

As mentioned previously, values of the index of a CERO are referred to as *identifiers*. Identifiers are \
subject to a couple of restrictions. They are:

    * The identifier must be unique - that is, no other value of ``cero.index`` can be exactly the same.
    * The identifier must be either:
        * a string (``str``) *with no commas*, or
        * a tuple of strings, where each string does not have any commas.

The comma constraint is a result of how ConCERO interprets commas when reading YAML files - ConCERO \
interprets commas as a string-splitting character. Thus, \
if a configuration file contains the string:

    ``"hello,world"``

in the context of CERO *identifiers*, then this will be interpreted as the python tuple:

    ``('hello','world')``

Note also that any white spaced is stripped when the string is split, so the string:

    ``"hello, world"``

also becomes:

    ``('hello','world')``

and this:

    ``" L_OUTPUT, Electricity, AUS"``

becomes:

    ``("L_OUTPUT","Electricity","AUS")``

The advantage of the tuple form of identifier is that it preserves ordered relationships, even though that \
ordered relationship has no meaning within the CERO itself. This is necessary to store data that is more \
than 2-dimensional in nature in 2-dimensions. It also allows for the implementation of ``sets`` (see :ref:`sets`),\
which provide the user with significant flexibility and power with respect to selecting identifiers of interest. \
In summary, ``sets`` allow the user to select large amounts of identifiers by just listing sets, \
as opposed to all the identifiers.


.. * VURM
.. * AusTIMES
.. * LUTO
.. * GALLM-E
.. * GALLM-T
.. * GTAP-E

.. The CERO provides methods for use with a pandas dataframe. Subclassing \
.. ``pandas.DataFrame`` is not a trivial exercise.

Created on Wed Dec 20 10:20:32 2017

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
import os

import pandas as pd
import numpy as np

from concero._identifier import _Identifier

class CERO(object):
    _msg_inv_type = "Object not of CERO type (pandas.DataFrame)."
    _msg_bad_idx = r"Object's index is not of pandas.Index type."
    _msg_bad_col = "Object.columns is not of pandas.DatetimeIndex type."
    _msg_idx_nunique = "Index values are not unique."
    _msg_col_nunique = "Column values are not unique."
    _msg_val_type = "Values are not of numpy.float32 type."
    _msg_empty_cero = "Object is empty - not a valid CERO."
    _msg_invalid_ids = "Values in object's index are not valid identifiers."

    class InvalidCERO(TypeError):
        pass

    class CEROIndexConflict(RuntimeError):
        pass

    class EmptyCERO(ValueError):
        pass

    @staticmethod
    def create_empty():
        """Returns empty CERO."""

        cero = pd.DataFrame()
        cero.columns = pd.DatetimeIndex(freq="AS", periods=0, start="2018")
        return cero

    @staticmethod
    def is_cero(obj, raise_exception=True, empty_ok=True):
        """

        :param obj: The object that may or may not be a CERO.
        :param raise_exception: If `True` will raise an exception on the event that obj is not a CERO.
        :param empty_ok: If `True`, ``obj`` must have at least one value that is not an NaN to qualify as a CERO. `False` by default.
        :return:
        """

        try:
            assert isinstance(obj, pd.DataFrame)
        except AssertionError:
            raise CERO.InvalidCERO(CERO._msg_inv_type)

        try:
            assert (type(obj.index) == pd.Index)
        except AssertionError:
            if raise_exception:
                raise CERO.InvalidCERO(CERO._msg_bad_idx +
                                       (" Instead it is of type '%s'." % type(obj.index)))
            return False

        try:
            assert isinstance(obj.columns, pd.DatetimeIndex)
        except AssertionError:
            if raise_exception:
                raise CERO.InvalidCERO(CERO._msg_bad_col)
            return False

        try:
            assert obj.index.is_unique
        except AssertionError:
            if raise_exception:
                raise CERO.InvalidCERO(CERO._msg_idx_nunique + (" Duplicated values are: %s." % obj.index.get_duplicates()))
            return False

        try:
            assert obj.columns.is_unique
        except AssertionError:
            if raise_exception:
                raise CERO.InvalidCERO(CERO._msg_col_nunique +
                                       (" Duplicated values are: %s." % obj.columns.get_duplicates()))
            return False

        try:
            assert all([issubclass(x.type, (np.float32,)) for x in obj.dtypes])
            # Note that this 'float32 requirement' is because df.to_pickle() automatically downsizes \
            # float64 to float32, and there is no option to change this behaviour.
        except AssertionError:
            if raise_exception:
                raise CERO.InvalidCERO(CERO._msg_val_type)
            return False

        invalid_idents = list(filter(lambda x: not _Identifier.is_valid(x), obj.index.tolist()))
        try:
            assert (not invalid_idents)
        except AssertionError:
            if raise_exception:
                raise CERO.InvalidCERO(CERO._msg_invalid_ids + (" Invalid index values are: %s." % invalid_idents))
            return False

        if not empty_ok:
            try:
                assert(not obj.isnull().all().all())
            except AssertionError:
                if raise_exception:
                    raise CERO.EmptyCERO(CERO._msg_empty_cero)
                return False

        return True

    @staticmethod
    def create_cero_index(values: 'List[str, tuple]'):
        """Creates pandas.Index object that adheres to CERO constraints."""
        values = [_Identifier.tupleize_name(value) for value in values]
        return pd.Index(values, tupleize_cols=False)

    @staticmethod
    def read_xlsx(xlsx_file, *args, **kwargs):
        """Reads CEROs that have been exported to xlsx files.

        :arg (str) file: Name of xlsx file that CERO resides in.
        """

        xlsx_file = os.path.abspath(xlsx_file)

        ch = pd.read_excel(xlsx_file, nrows=0) # Read header

        # Identify where index columns end
        ss = [type(col) for col in ch.columns].index(pd.datetime)
        index_col = list(range(ss))

        cero = pd.read_excel(xlsx_file, index_col=index_col)
        cero = cero.astype(pd.np.float32)
        cero.index = CERO.create_cero_index(cero.index.tolist())
        assert CERO.is_cero(cero)  # Check that it is a valid CERO object

        return cero

    @staticmethod
    def read_csv(csv_file):
        """
        Reads CEROs that have been exported to csv file. It is assumed that ';' are used to seperate the fields (if more than one) of the identifier.

        :param str csv_file: Path to the file containing the CERO.
        :return pandas.DataFrame: The imported CERO.
        """

        cero = pd.read_csv(csv_file, header=0, index_col=0)  # Read header
        cero = cero.astype(pd.np.float32)
        cero.index = CERO.create_cero_index(_Identifier.get_all_idents(cero.index.tolist(), sep=";"))
        cero.columns = pd.to_datetime(cero.columns.tolist(), format="%Y")
        assert CERO.is_cero(cero)  # Check that it is a valid CERO object

        return cero

    @staticmethod
    def combine_ceros(ceros: list, overwrite=True, verify_cero=True) -> pd.DataFrame:
        """Combine multiple CEROs (provided as a ``list``) into a common CERO. If ``overwrite`` is True, a CERO \
        that is later in ``ceros`` (i.e. has a higher index) will overwrite the merger of all preceding CEROs. If \
        ``overwrite`` is False and duplicate indices are detected, an ``CERO.CEROIndexConflict`` exception \
        will be raised.

        If ``verify_cero`` is ``True``, then a check is performed before and after combination to ensure that \
        only CEROs are combined with other CEROs, to form a CERO. By disabling this, ``combine_ceros`` can be \
        applied to ``pandas.DataFrames`` as well.
        """
        try:
            assert isinstance(ceros, list)
        except AssertionError:
            raise TypeError("'ceros' must be provided as a list of CEROs, not '%s'." % type(ceros))

        if verify_cero:
            for i, cero in enumerate(ceros):
                try:
                    CERO.is_cero(cero)
                except CERO.InvalidCERO as e:
                    raise CERO.InvalidCERO("The '%d'th CERO in the list (zero-indexed) is invalid." % i)

        if isinstance(overwrite, bool):
            overwrite = [overwrite]*len(ceros)

        # In the case first value is neglected because it is ineffectual...
        if issubclass(type(overwrite), list) and len(overwrite) == len(ceros) -1:
            overwrite.insert(0, overwrite[0])

        cero = ceros[0]
        for next_cero, ow in zip(ceros[1:], overwrite[1:]):
            if not ow:
                # Check the intersection of indices
                itsn = cero.index.intersection(next_cero.index)
                if not itsn.empty:
                    raise CERO.CEROIndexConflict(("Attempted to combine CEROs with duplicate indices " +
                            "(and 'overwrite' is not allowed). The duplicated indices are: %s." % itsn.values))

            cero = next_cero.combine_first(cero)
            cero = cero.astype(np.float32, copy=False)
            # #TODO: combine_first can output array of different dtypes then inputs. I have not isolated the circumstances \
            # that this occurs however...

        if verify_cero:
            CERO.is_cero(cero)  # check there have been no errors

        return cero

    @staticmethod
    def rename_index_values(cero: pd.DataFrame, map_dict: dict, inplace: bool=True):
        """
        :param cero: The CERO object to rename the index values of. The order of the CERO.index imposes order on the mapping operation - that is, the CERO retains its original order.
        :param map_dict: A `dict` of (old name, new name) are (key, value) pairs.
        :return:
        """

        if not issubclass(type(map_dict), dict):
            raise TypeError("The mapping dictionary must be a subclass of dict.")

        def f(x): # Copied from within pandas.core.generic.rename()
            if x in map_dict:
                return _Identifier.tupleize_name(map_dict[x])
            return _Identifier.tupleize_name(x)

        if inplace:
            ret = None
        else:
            cero = cero.copy(deep=False)
            ret = cero

        cero.index = CERO._transform_index(cero.index, f, tupleize_cols=False)

        return ret

    @staticmethod
    def _transform_index(index, func, level=None, tupleize_cols=False):
        """
        Apply function to all values found in index.

        This includes transforming multiindex entries separately.
        Only apply function to one level of the MultiIndex if level is specified.
        """
        # Copied from pandas.core.internals._transform_index() with minor modification in response to pandas bug #19497
        if isinstance(index, pd.MultiIndex):
            if level is not None:
                items = [tuple(func(y) if i == level else y
                               for i, y in enumerate(x)) for x in index]
            else:
                items = [tuple(func(y) for y in x) for x in index]
            return pd.MultiIndex.from_tuples(items, names=index.names)
        else:
            items = [func(x) for x in index]
            return pd.Index(items, name=index.name, tupleize_cols=tupleize_cols)


