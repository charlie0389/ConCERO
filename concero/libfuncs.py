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
Note: This is the only source code file that should be touched by the user, and even then, very infrequently.

This module provides a library of functions that may be required for operations on CEROs, or for \
running file-processing commands. All functions in this file fit into one of the following four categories:

    1. A CERO/pandas.DataFrame operation.
    2. A pandas.Series operation.
    3. A recursive operation.
    4. A file-processing operation.

For any function, depending on the category above, there are constraints imposed on the function structure/defition.

### Class 1 Functions - Operations on ``CERO``/``pandas.DataFrame`` objects

A class 1 function must fit the form:

.. code-block:: python
    @dataframe_op
    def func(df, *args, **kwargs):
        ...
        return None

Note the following key features:
    * The function is proceeded by the @dataframe_op wrapper (imported from ``libfuncs_wrappers``).
    * The first argument (``df``) must be of CERO/pandas.DataFrame type.
    * No parameters are returned (technically, the last line could be omitted).

**What is not clear from the function definition above** is the **additional requirement** that all operations on \
``df`` must occur inplace. In other words, all mutations/operations must be applied to ``df`` - *not* a copy of \
``df``. If this constraint is violated, no exceptions/errors will be raised (note that it is impossible to detect this \
'failure of intention'). As a rule of thumb, this can nearly always be achieved by restricting operations to the \
types:
    * ``df.loc[...] = ...``,
    * ``df.iloc[...] = ...``, or
    * ``df.func(*args, inplace=True, **kwargs)``.

It is highly recommended to consult ``pandas`` documentation and ``StackOverflow`` to develop a better \
understanding of what ``inplace`` operations are.

### Class 2 Functions - Operations on ``pandas.Series`` objects

Similar to class 1 functions, class 2 functions must fit the form:

.. code-block:: python
    @series_op
    def func(series, *args, **kwargs):
        ...
        return pandas_series

With similar features:

    * The function is proceeded by the @series_op wrapper (imported from ``libfuncs_wrappers``).
    * The first argument (``series``) must be of pandas.Series type.

However, *dissimilar to class 1 functions*, class 2 functions must:

    * Return an object of ``pandas.Series`` type (``pandas_series``). ``pandas_series`` must be of the \
    same ``shape`` as ``series``.

* Documenation incomplete from this point forwards...
A function must have the signature:

    def func(prev: object, inp: object) -> object

For example, if the function

    def func(a, b):
        return a + b

is referenced as ``recfunc`` with the iterable [1,2,3,4,5] and initial \
value 2, the result will be [3, 5, 8, 12, 17].

**IMPORTANT**: Be careful to ensure the result is not modified in place. For example, note that:
::

    result = result + array

is subtly different to:
::

    result += array

The latter modifies ``result`` in place, and should be avoided.

Avoid trying to create a renaming function - use the one created below. If you must, please consult the function \
already created - it has been designed to work around a bug in Pandas (Issue #19497).


Created on Thu Dec 21 16:36:02 2017

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""

from collections import OrderedDict
import os
import shutil

import pandas as pd
import numpy as np

import concero.conf as conf
if getattr(conf, "harpy_installed", False):
    import harpy

from concero.libfuncs_wrappers import dataframe_op, series_op, recursive_op
from concero._identifier import _Identifier
from concero.cero import CERO

def plotdf(df,
           figurepath,
           plotformat='png',
           plottitle=None,
           ylabel=None,
           plottype='area',
           scaletype='linear',
           set_xlabel = None,
           set_ylabel = None,
           set_title = None,
           legend = None,
           **plot_options):
    """ Various plot types for CERO. ``plot_options`` are directly passed as ``pandas.DataFrame.plot()`` options.

    :param pandas.DataFrame df: The CERO providing the data for plotting. All series of the CERO are plotted by default.
    :param str figurepath: Location to output figure generated.
    :param str plotformat: The format of the output figure. ``'png'`` by default. A value provided for this argument is passed as the ``format`` keyword argument of ``fig.savefig()``.
    :param str plottitle: `None` by default. If provided is the title of the plot.
    :param str ylabel: Y-axis label.
    :param str plottype: ``'area'`` by default. Passed as ``'kind'`` to the plot function.
    :param str scaletype: The scale type of the axis. Some of the valid values are ``'logx'``, ``'logy'`` and ``'loglog'``.
    :param dict set_xlabel: `dict` of options provided to the ``axis.set_xlabel()`` method.
    :param dict set_ylabel: `dict` of options provided to the ``axis.set_ylabel()`` method.
    :param dict set_title: `dict` of options provided to the ``axis.set_title()`` method.
    :param dict legend: `dict` of options provided to the ``axis.set_legend()`` method.
    :param dict plot_options: Any additional options to pass to the plotting method. Refer to the `pandas documentation<https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html>`_ for more information.
    :return:
    """

    try:
        import seaborn
        seaborn.set()  # Necessary from version 0.8.1 onwards to import colour palette
    except ImportError as e:
        if str(e) != "No module named 'PyQt4'":
            raise e
        raise ImportError("PyQt4 has not been installed, and is necessary to use ConCERO's plotting capabilities. Please consult ConCERO documentation or the internet for install instructions.")

    sxl = {"xlabel": ""}
    syl = {"ylabel": "", "fontsize": 12, "fontstyle": 'italic'}
    sto = {"label": ""}
    leg = {"bbox_to_anchor":(1.05, 1),
           "loc":'upper left',
           "prop":{'size': 9}}
    if set_xlabel is None:
        set_xlabel = {}
    if set_ylabel is None:
        set_ylabel = {}
    if set_title is None:
        set_title = {}
    if legend is None:
        legend = {}
    sxl.update(set_xlabel)
    syl.update(set_ylabel)
    sto.update(set_title)
    leg.update(legend)

    if ylabel is not None:
        syl["ylabel"] = ylabel

    ao = {"set_xlabel": sxl,
          "set_ylabel": syl,
          "set_title": sto, # NOT to be confused with options for setting the *figure* title...
          "legend": leg}

    # xao = {} # Default x-axis options
    # yao = {}  # Default x-axis options
    #
    # xao.update(xaxis_options)
    # yao.update(yaxis_options)

    dpo = {"figsize": (10, 5),
           "style":'-',
           "fontsize": 12} # Default plot options
    dpo.update(plot_options)
    plot_options = dpo

    plot_options.update({"logx": False,
                         "logy": False,
                         "loglog": False}) # Linear by default
    if scaletype == 'logx':
        plot_options.update({"logx":True})
    elif scaletype == 'logy':
        plot_options.update({"logy": True})
    elif scaletype == 'loglog':
        plot_options.update({"loglog": True})

    plot_options.update({"kind" : plottype, "title": plottitle})

    df = df.transpose()
    ax = df.plot(**plot_options)

    for attr, kwargs in ao.items():
        getattr(ax, attr)(**kwargs)

    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, 0.9 * box.width, box.height]) # Not sure why this was here...

    # ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 9})

    fig = ax.get_figure()
    fig.savefig(os.path.relpath(figurepath), format=plotformat, bbox_inches='tight')

@dataframe_op
def merge(df, *args, **kwargs):
    df.iloc[0, :] = df.sum(axis=0) # Replaces the first series with the sum of all the series
    return df

@dataframe_op
def merge_multiply(df, *args, **kwargs):
    result = pd.Series(np.ones(df.shape[1]), index=df.columns, name=df.index.values[0])
    for (_, array) in df.iterrows():
        result = result * array
    df.iloc[0, :] = result
    return

def build_har_obj(df: pd.DataFrame,
                  names_of_sets: 'List[str]' = None,
                  header_name: str = None,
                  time_dim_name: str = "TIME",
                  time_dim_fmt: str = r"Y%Y",
                  split_char: str = None,
                  name_idx: int = None,
                  coeff_name: str = None,
                  **kwargs) -> 'harpy.HeaderArrayObj':
    """
    .. py:method:: build_har_obj(df, names_of_set=None, header_name=None, time_dim_name="TIME", \
    time_dim_fmt=r"Y%Y", split_char=None, name_idx=None, coeff_name=None, **kwargs)
    Builds a header appropriate for writing to a HAR file (``harpy.HAR.HAR`` object).
    :param (pandas.DataFrame) df: The dataframe from which the header is generated. The header will be generated from \
    the entire object.
    :param (str) header_name: The name of the header to be created.
    :param (str) time_dim_name: The name of the time dimension created. Defaults to ``"TIME"``.
    :param (str) time_dim_fmt: A ``pandas.DatetimeIndex.strftime`` compatible string. This **string must be provided** \
    in rawstring format - i.e. prefixed by an 'r' - e.g. r"Y%Y". Consult the \
    `datetime documentation <https://docs.python.org/3.5/library/datetime.html#strftime-and-strptime-behavior>`_ \
    for information \
    regarding valid identifiers. It is likely the only one of relevance is ``%Y`` - referring to a 4-digit year. The \
    default value ``"Y%Y"`` will format year labels as ``"Y2018"``, ``"Y2019"``, ``"Y2020"`` etc.
    :param (str) split_char: If ``df.index.values`` are strings and ``split_char`` is defined, each index value is \
    split by ``split_char``, and the ``name_idx``th item (zero-indexed) is taken as the new ``df.index`` value. \
    Valid values are include the single character as a string, or the string "space". Note that representing \
    a space with the former format in a YAML is very difficult (if not impossible).
    :param (int) name_idx: See ``split_char`` parameter documentation.
    :param (str) coeff_name: The header coefficient name.
    :param (dict) kwargs: Any additional keyword arguments are passed to ``harpy.Header.Header.HeaderFromData`` on \
    header generation.
    :return:
    :type harpy.Header.Header: The generated header.
    """
    for k, v in {'names_of_sets': names_of_sets, 'header_name': header_name}.items():
        if v is None:
            raise RuntimeError("\'%s\' must be provided for function \'build_har_obj\'." % k)
    if isinstance(split_char, str) and isinstance(name_idx, int):
        if split_char == "space":
            split_char = " "
        new_values = [val.split(split_char)[name_idx] if not isinstance(val, tuple) else val for val in df.index.values]
        df.index = pd.Index(data=new_values, name=df.index.name, tupleize_cols=False)

    # Identify MultiIndex
    idx = pd.MultiIndex.from_tuples([(val,) if not isinstance(val, tuple) else val for val in df.index])

    # Index may not be sorted according to the order of appearance, therefore develop elements list from appearance
    unique_labs = [OrderedDict([(lab, None) for lab in levlabs]) for levlabs in idx.labels]
    reord_labs = [[idx.levels[i][k] for k in unique_labs[i].keys()] for i in range(len(unique_labs))]
    sets = [{"name": name, "dim_desc": labs, "dim_type": "Set"} for (name, labs) in zip(names_of_sets, reord_labs)]

    # Add time dimension
    sets.append({"name": time_dim_name, "dim_desc": df.columns.strftime(time_dim_fmt).tolist(), "dim_type": "Set"})
    new_dims = tuple(len(s["dim_desc"]) for s in sets)
    header_array = df.values.reshape(new_dims)
    header_kwargs = {'long_name': None, 'coeff_name': coeff_name,}

    # Update from arguments given
    for k in header_kwargs:
        if k in kwargs:
            header_kwargs[k] = kwargs[k]
    return harpy.HeaderArrayObj.HeaderArrayFromData(name=header_name,
                                         array=header_array,
                                         sets=sets,
                                         # sets=list(sets.keys()),
                                         # SetElements=sets,
                                         **header_kwargs)

@dataframe_op
def replace_har_header_in_file(df, har_file=None, new_har_file=None, header_name=None, **kwargs):
    """Replaces the header ``header_name`` in ``har_file`` by the data contained in ``df``. If ``new_har_file`` \
    is given, ``har_file`` is first copied to ``new_har_file``, and then ``header_name`` is overwritten. If \
    ``header_name`` does not exist, it is appended to the end of the file - consequently, this function can be used \
    to add headers to a har file as well.

    ``kwargs`` is passed to :py:meth:build_har_obj() - used to create the header object.
    """

    if not isinstance(har_file, str):
        raise ValueError("Output file ('har_file') must be specified and of string type.")

    if os.path.splitext(har_file)[1] == "":
        # Add file extension if not specified
        har_file += ".har"

    # Create the new header-array object
    head_arr_obj = build_har_obj(df, header_name=header_name, **kwargs)

    if new_har_file is not None:
        new_har_file = os.path.normpath(new_har_file)
        shutil.copy2(har_file, new_har_file)
        har_file = new_har_file

    har_file = os.path.normpath(har_file)

    try:
        hfo = harpy.HarFileObj.loadFromDisk(filename=har_file)
        idx = hfo.getHeaderArrayObjIdx(header_name)
        hfo.removeHeaderArrayObjs(header_name)
    except FileNotFoundError:
        # Create file object if it doesn't exist
        hfo = harpy.HarFileObj()
        idx = None # Results in header-array being appended to empty list
    hfo.addHeaderArrayObj(head_arr_obj, idx=idx)
    hfo.writeToDisk(filename=har_file)

@dataframe_op
def fillna(df, *args, value=None, method=None, **kwargs):
    kw = {"axis": 1, "inplace": True}
    kw.update(kwargs)
    kwargs = kw

    if method is not None:
        df.fillna(method=method, **kwargs)
    elif value is not None:
        df.fillna(value=value, **kwargs)
    else:
        df.fillna(method="ffill", **kwargs)
    return df

@dataframe_op
def apply_func(df, *args, numpy_func: str=None, **kwargs):

    defaults = {"axis": 1}
    defaults.update(kwargs)

    df.loc[:,:] = df.apply(getattr(np, numpy_func), **kwargs)
    return df

@dataframe_op
def noop(df):
    return df

@dataframe_op
def groupby(df: "CERO", *args, key: "Union[int, list[int]]"=None, match: str=None, agg: str=None, **kwargs):

    if key is None:
        raise TypeError("'key' must be provided to 'groupby' function as either an int or list of ints.")
    elif not issubclass(type(key), list):
        key = [key]

    if not all([issubclass(type(k), int) for k in key]):
        raise TypeError("'key' must be provided to 'groupby' function as either an int or list of ints.")

    defaults = {"axis": 0,
                "sort": False,
                "group_keys": False}
    defaults.update(kwargs)

    match = _Identifier.tupleize_name(match)
    m_ids = [match]
    if match is None:
        m_ids = _Identifier.unique_id_fields(df.index.values, key=key)

    conv = lambda x: tuple(x) if issubclass(type(x), str) else x
    m_ids = [conv(m) for m in m_ids]

    rename_dict = {}
    for m in m_ids:

        # Create func that identifies rows for grouping
        def f(x):
            return all([x[k] == m[idx] for idx, k in enumerate(key)])

        # Groupby and apply aggregation function
        agg_df = df.groupby(by=f, **defaults).agg(agg)

        # Put aggregated calculation in first row that meets the condition
        row_loc = next(x for x in df.index.values if f(x))
        df.iloc[df.index.get_loc(row_loc)] = agg_df.loc[True]

        # Rename row
        rename_dict.update({row_loc: _Identifier.keep_only_fields(key, row_loc)[0]})

    CERO.rename_index_values(df, rename_dict, inplace=True)
    return df

@series_op
def interpolate(series, **kwargs):
    defaults = {"method":"time"}
    defaults.update(kwargs)
    return series.interpolate(**defaults)

@dataframe_op
def mult(df, factor: float=1.0):
    return df*factor

@recursive_op
def pc_change(x, y):
    return x*(1 + y/100)

@recursive_op
def iter_and_norm(prev: float, inp: float) -> float:
    res = prev + prev * inp / 100
    return res


@recursive_op
def carbon_price(prev: float, inp: float) -> float:
    res = prev + inp * 1000
    return res


@recursive_op
def zero_floor(inp: float) -> float:
    return max(inp, 0)

@recursive_op
def reciprocal_growth(prev: float, next: float) -> float:
    return -(100*next/prev - 100)
