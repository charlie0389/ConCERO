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
.. to_cero:

The ToCERO class provides methods for converting data files **to** the CERO format.

Critical to the successful use of this class is a configuration file in YAML format. \
Do not be intimidated by the acronym - the YAML format is very simple and human readable. Typically, \
study [1]_ of the YAML format should be unnecessary - copying a working configuration file and then \
altering it for the desired purpose should satisfy most users (the ``tests/data`` subdirectory provides many examples). This documentation will show you how to build a YAML \
configuration file for use with the `ToCERO` class in a gradual, example-by-example process. A technical reference to the ``ToCERO`` class \
will follows.

Building a YAML file from scratch to convert *TO* the CERO format
-----------------------------------------------------------------

The configuration file can differ significantly depending on the type of file from which data is \
imported, but one aspect that all configuration files **must** have in common is the ``files`` field. As the \
name suggests, ``files`` specifies the input files that are sources of data for the conversion process. \
It therefore follows that a minimal (albeit useless) YAML configuration file will look like this:

    ``files:``

That is, a single line that doesn't specify anything. This simple file is interpreted as a `dict` with the key ``"files"`` with a corresponding value of `None` - the ``:`` identifies the key-value nature of the data. That is:

    ``{"files": None}``

This top-level dictionary object - is referred to as a *ToCERO* object. The obvious next step is to specify some input files to convert. \
This is done by adding **indented** [2]_ subsequent lines with a hyphen, **followed by a space**, followed by the relevant data. For example:

.. code-block:: yaml

    files:
        - <File Object A>
        - <File Object B>
        - <File Object C>
        - etc.

The hyphens (followed by a space) on subsequent lines identify separate items that collectively are interpreted as a python `list`. The indented nature of the list identifies that this list is the value for the key in the line above. Basically the previous example is interpreted as the python object:

.. code-block:: python

    {"files": [<Python interpretation of File Object A>,
                      <Python interpretation of File Object B>,
                      <Python interpretation of File Object C>,
                      <etc.>]}

Note that each item of the ``"files"`` list can be either a `str` or a `dict`. If a `str`, the string must refer to a YAML file containing a `dict` defining a *file* object. If a `dict`, then that dict must be a file object. A file object is a dictionary with one mandatory key-value pair - that is, (in YAML form):

.. code-block:: yaml

    file: name_of_file

Where ``name_of_file`` is a file path *relative to the configuration file*. The option ``search_paths: List[str]`` provided as on option to the file object (or the encompassing ToCERO object) overrides this behaviour (where paths earlier in the list are searched before paths later in the list).

Without further specification, if the file *type* is comma-separated-values (``CSV``) *and* if the data is of the default format, ConCERO can import the entire file. The 'default format' is discussed on this page :ref:`import_guidelines`. ConCERO determines the file type:

    1. by the key-value pair ``type: <ext>`` in the *file object*, and if not provided then
    2. by the key-value pair ``type: <ext>`` in the *ToCERO object*, and if not provided then
    3. by determining the extension of the value of ``file`` in the *file object*, and if not determined then
    4. an error is raised.

Providing the ``type`` option allows the user to potentially extend the program to import files that the program author was not aware existed, if the file is of a similar format to one of the known and supported formats. For example, if the program author was not aware ``shk`` files existed (and thus did not provide support for them), ``shk`` files could be imported by specifying ``type: har`` (given their similarity to ``har`` files). As it is, ``shk`` files *are* supported, so this is not necessary. Naturally, whether the import succeeds will be dependent on whether the underlying library allows importing that file type.

With respect to step 2 (of determining the file type), it can be said that the file object *inherits* from the ToCERO object. Many key-value pairs can be inherited from the ToCERO object, which reduces duplicating redundant information in the case that some properties apply to all the input files. Given that every key-value pair has some effect on configuration, the term *option* is used to refer to a key-value pair collectively. So an example of a YAML file including all points discussed so far is:

.. code-block:: yaml

    files:
        - file: a_file.csv
        - file: b_file
          type: csv

In the example above, ``a_file.csv`` and ``b_file`` would be successfully imported (assuming they are both of default format). \
The file extension can be discerned with respect to ``a_file.csv``, and \
``b_file`` has the corresponding ``type`` specified. Note that the ``type`` option (for ``b_file`` is indented at \
the same level as file option, *not* the list).

A minimal configuration form that demonstrates inheritance (and assuming ``c_file`` is of default ``csv`` type) is:

.. code-block:: yaml

    type: 'csv'
    files:
        - file: a_file.csv
        - file: b_file
        - file: c_file

Note that, alternatively, the file name of c_file could be changed to include a file extension. \
An important point is that the inheritance of ``type`` does not \
mean you - the user - can lazily drop the file extensions. The file extension is part of the file name, and so it \
must be provided, if it exists, to find the correct file.

In most cases, more specification in the file object is necessary to import data. \
The necessary and additional options in the file object depend on the type of the file - whether it be \
`CSV files`_, `Excel files`_, `HAR files`_ or `GDX files`_. That is, the supported types are \
``ToCERO.supported_file_types`` - a set of:

    * ``"csv"``
    * ``"xlsx"``
    * ``"har"``
    * ``"shk"``
..    * ``"gdx"``

.. _CSV files:

File Objects - CSV files
--------------------------

CSV files can be considered the simplest case with respect to data import. 'Under the hood' ConCERO uses the \
``pandas.read_csv()`` method to implement data import from CSVs (documentation for which can be found \
`here <http://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.read_csv.html>`_ ). Any option \
available for the ``pandas.read_csv()`` method is also available to ConCERO by including that option \
in the file object.

There are also a few additional options that can be provided that provide specific functionality for ConCERO. These \
options are:

**series: (list)**

   the list specifies the series in the index that are \
   relevant, so therefore providing a way to select data for export to the CERO. Each item in the list is referred to \
   as a *series object*, which is a dictionary with the following options:

        **name: (str)**

           ``name`` identifies the elements of the index that will be converted into a CERO. ``name`` is a mandatory option.

        **rename: (str)**

           If provided, after export into the CERO changes ``name`` to value provided by ``rename``.

A series object can be provided as a string - this is equivalent to the series object ``{'name': series_name}``.

**orientation: (str)**

   ``'rows'`` by default. If the data is in columns with respect to time, change this option to ``'cols'``, (and therefore effectively calling a transposition operation).

**skip_cols: (str|list)**

    A column name, or a list of column names to ignore.

And other ``pandas.read_csv()`` options that are regularly used include:

**usecols: (list)**

   From pandas documentation - Return a subset of the columns. If array-like, all elements must either be positional (i.e. integer indices into the document columns) or strings that correspond to column names provided either by the user in names or inferred from the document header row(s). For example, a valid array-like usecols parameter would be [0, 1, 2] or [‘foo’, ‘bar’, ‘baz’]. Note that ``usecols`` will take precedence over ``skip_cols``, and that the argument format for ``usecols`` for a ``csv`` file differs slightly to that for an ``xlsx`` file.

**index_col: (int|list)**

   The column or list of columns (zero-indexed) in which the identifiers reside or, if ``orientation=="cols"``, the column with the date index.

**header: (int|list)**

   The row or list of rows (zero-indexed) in which the date index resides or, if ``orientation=="cols"``, the rows with the data identifiers.

**nrows: (int)**

   Number of rows of the file to read. May be useful with very large ``csv`` files that have a lot of irrelevant data.

For further documentation, please consult the \
`pandas documentation <http://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.read_csv.html>`_ \
documentation.

.. _Excel files:

File Objects - Excel files
--------------------------

The process for importing Excel files is very similar to that of csv files. Underneath, the ``pandas.read_excel()`` \
method is used, with virtually identical options with identical meanings. Consequently, not all the standard options \
will be mentioned here - just the differences in contrast to those for ``csv`` files. For a complete list of available \
options, please consult `the pandas documentation <https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.read_excel.html>`_.

**sheet: (str)** or **sheet_name: (str)**

   The name of the sheet in the workbook to be imported.

**usecols: (list[int]|str)**

   Similar to the ``csv`` form of the option, ``usecols`` accepts a list of zero-indexed integers to identify the \
columns to be imported. **Unlike the csv option**, ``usecols`` will **not** accept a ``list`` of ``str``, but will accept \
a single ``str`` with an excel-like specification of columns. For example, ``usecols: A,C,E:H`` specifies the \
import of columns ``A``, ``C`` and all columns between ``E`` and ``H`` *inclusive*.

.. _HAR files:

File Objects - HAR (or SHK) files
-----------------------------------

In reading this section of the documentation, ``shk`` files can be considered equivalent to ``har`` files, so \
references to ``shk`` files can be dropped.

``har`` files contain one or more *header arrays*, and with each header array is an array of one or more dimensions \
(to a maximum of 7). Each dimension of each array has an associated *set*. Note that the terminology *set* can \
be considered misleading because, unlike the mathematical concept of a set, HAR sets *have an order*. \
The order of the set corresponds to the placement of items within the array.

To specify the import of a har file, only one option in the file object is necessary - that is, ``head_arrs`` with \
an associated list of strings specifying the names of header arrays to import from the file. Therefore, an example configuration file that specifies the import of a ``har`` file could \
look like:

.. code-block:: yaml

    files:
      - file: har_file.har
        head_arrs:
          - HEA1
          - HEA2

With the example configuration, header arrays ``HEA1`` and ``HEA2`` would be imported from file ``har_file.har``. *Note* \
that it is a restriction of the ``har`` format itself that header names can not be longer than 4 characters.

In the example above, each header array name is interpreted as a string. The more general format for a header definition is \
a ``dict``, referred to as ``header_dict``. Each ``header_dict`` *must* have the option:

    * ``name: header_name``, where ``header_name`` is the name of the header.

``header_dict`` *must* also have the following option *if one of the dimensions of the array is to be interpreted as a time \
dimension*:

    * ``time_dim: (str)``, where the string is the name of the set indexing the time-dimension (note that the \
    format/data-type of the time dimension is irrelevant).

If the data has no time dimension (which *definitely should be avoided*) and therefore ``time_dim`` is not specified, \
then ``default_year`` **must** be provided (or inherited from the file object) - otherwise a ValueError will be \
thrown.

Note that it may also be necessary to include some of the file-independent options if the time-dimension has a format \
that deviates from the default. Please see `File independent options`_ for more information.

File Objects - VD files (Experimental)
--------------------------------------

The coder writing the import connector is not familiar with the diversity of VEDA data files (if there are any). Consequently, the VEDA data file importer has been written with several assumptions. Specifically:

    #. Lines starting with an asterisk (*) are comments.
    #. The number of data columns remain constant throughout a single file.

If these assumptions are incorrect, please raise an issue on GitHub.

To specify the import of a vd file, it is mandatory to specify:

    * ``date_col: (int)``, where ``date_col`` is the zero-indexed number of the column containing the date.
    * ``val_col: (int)``, where ``val_col`` is the zero-indexed number of the column containing the values.

And optional to specify:

    * ``default_year: (int)`` - If left unspecified, all records with an invalid date in ``date_col`` are dropped. If specified (as a year), the value of ``date_col`` in all records with an invalid date are changed to ``default_year``.

Example:

.. code-block:: yaml

    files:
      - file: a_file.vd
        date_col: 3
        val_col: 8
        default_year: 2018

Note that it may also be necessary to include some of the file-independent options if the time-dimension has a format \
that deviates from the default. Please see `File independent options`_ for more information.

.. _GDX files:

File Objects - GDX files (Experimental)
---------------------------------------

GDX files can be imported by providing the option:
    * ``symbols: list(dict)`` - where each `list` item is a `dict` (referred to as a "symbol dict").

Each symbol dict must have the options:

    * ``name: (str)`` - where ``name`` is the name of the symbol to load.
    * ``date_col: (int)`` - where ``date_col`` specifies the (zero-indexed) column that includes the date reference.

.. _File independent options:

File Independent Options:
-------------------------

The options in this section are relevant to all input files, regardless of their type. They are:

**time_regex: (str)**

**time_fmt: (str)**

**default_year: (int)**

A fundamental principle ConCERO relies upon is that all data has some reference to time (noting that all data to date has been observed to reference the year only). The time-index data will typically be in a string format, and the year is interpreted by \
searching through the string, using the regular expression ``time_regex``. The default - ``'.*(\d{4})$'`` - will \
attempt to interpret the last four characters of the string as the year. Importantly, the match returns the \
year as the 1st 'group' (regular expression lingo). It is the first group that ``time_fmt`` is used with to \
convert the string to a datetime object. The default - ``'%Y'`` assumes that the string contains 4 digits \
corresponding to the year (and only that).

In the event that the date-time data isn't stored in the file itself, a ``default_year`` option (a single integer corresponding to the year - e.g. ``2017``) **must** be provided. \

What follows is an example, using the defaults of ``time_regex`` and ``time_fmt``, to \
demonstrate how this works...

Let's assume the time index series is given, in CSV form, by:

    .. code-block:: text

        bs1b-2017,bs1b-br1r-pl1p-2018,bs1b-br1r-pl1p-2019,...

which is typically seen with VURM-related data. The last four digits is obviously the year, so the default \
setting is appropriate. The regex essentially simplifies the data to a list of strings:

    ``['2017', '2018', '2019', etc...]``

However, ConCERO needs to convert these strings to ``pandas.datetime`` format. This is done by the \
`pandas.datetime.strftime() <https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior>`_ \
method, which relies on matching the strings with a pattern. The default - ``'%Y'`` - \
will interpret the strings as four digits corresponding to the year - an obviously satisfactory result. Hence, the \
following options are appropriate to include in the YAML configuration file.

    .. code-block:: yaml

        time_regex: .*(\d{4})$
        time_fmt: '%Y'

*Note*: if the default settings (as per the example immediately above) are appropriate, specifying them is **not** necessary.

.. [1] For a more thorough yet simple introduction to YAML files, `<http://docs.ansible.com/ansible/latest/YAMLSyntax.html>`_\
 is recommended.
.. [2] *'Indented'* can refer to a tab, 4 spaces or any combination of tabs/spaces. It is however critical that the \
indentation pattern *remains consistent* (which is a requirement in common with python).

ToCERO Technical Specification
------------------------------

.. autoclass:: ToCERO
    :members:

Created on Fri Jan 19 11:49:23 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import concero.conf
if getattr(concero.conf, "gdxpds_installed", False):
    import gdxpds #: Warning given if not imported before pandas
if getattr(concero.conf, "harpy_installed", False):
    import harpy

import re
import os
import itertools as it
from collections import OrderedDict
import builtins
import getpass

import pandas as pd
import xlrd

from concero.format_convert_tools import read_yaml
from concero._identifier import _Identifier
from concero.cero import CERO


class ToCERO(dict):

    _logger = concero.conf.setup_logger(__name__)

    class _FileObj(dict):

        supported_file_types = ["har", "csv", "xlsx", "xls", "shk", "gdx", "vd"]

        def __init__(self, *args, parent: dict=None,
                     **kwargs):
            """
            :param args: Passed to the superclass (`dict`) at initialisation.
            :param dict parent: Inherits at initialisation from parent.
            :param kwargs: Passed to the superclass (`dict`) at initialisation.
            """

            conf = ToCERO._FileObj.load_config(*args, parent=parent, **kwargs)
            super().__init__(conf)

        @staticmethod
        def load_config(conf: dict, *args, parent: dict=None, **kwargs):
            """
            :param 'Union[dict,str]' conf: The configuration dict, or if a `str`, the path (relative to the current working directory) of a YAML-format file containing the configuration dict.
            :return dict:
            """

            # Defaults
            _conf = {"header":0,
                        "index_col":0,
                        "time_regex":r".*(\d{4})$",
                        "time_fmt": r"%Y",
                        "search_paths": [],
                    "overwrite": False}

            if parent is None:
                parent = {}
            _conf.update(parent)

            if isinstance(conf, str):
                sp = _conf.get("search_paths")
                if not sp:
                    sp = [os.path.abspath(".")]
                conf = ToCERO._FileObj._find_file(conf, sp)
                conf = read_yaml(conf)

            _conf.update(dict(conf, *args, **kwargs))

            # search_paths initialisation, if not inherited
            if isinstance(_conf["search_paths"], str):
                _conf["search_paths"] = [os.path.abspath(_conf["search_paths"])]
            if _conf["search_paths"] == []:
                _conf["search_paths"].append(os.path.abspath("."))

            # Identify file type by extension if not given - the type determines which import function to use
            _conf["type"] = _conf.get("type", os.path.splitext(_conf["file"])[1][1:]).lower()

            # Series limits the data import to only those data series specified
            if _conf.get("series"):
                for idx in range(len(_conf["series"])):
                    if not isinstance(_conf["series"][idx], dict):
                        # Attempt to convert to dict...
                        _conf["series"][idx] = {"name": _conf["series"][idx]}

                    _conf["series"][idx]["name"] = _Identifier.tupleize_name(_conf["series"][idx]["name"])

                    if _conf["series"][idx].get("rename"):
                        _conf["series"][idx]["rename"] = _Identifier.tupleize_name(_conf["series"][idx]["rename"])

            return _conf

        @staticmethod
        def is_valid(conf, raise_exception=True):

            if not conf.get("file"):
                msg = "Key-value pair \"file: FILE_NAME\" must be provided for all " + "\'files\'."
                ToCERO._logger.error(msg)
                if raise_exception:
                    raise TypeError(msg)
                print(msg)
                return False

            return True

        @staticmethod
        def run_checks(conf, raise_exception=True):
            file = ToCERO._FileObj._find_file(conf["file"], conf["search_paths"], raise_exception=raise_exception)
            if not file:
                return False

            if not ToCERO._FileObj._check_permissions(file, raise_exception=raise_exception):
                return False

            return True

        @staticmethod
        def check_config(conf, *args, raise_exception=True, runtime=False, parent=None, **kwargs):
            conf = ToCERO._FileObj.load_config(conf, *args, parent=parent, **kwargs)
            if runtime:
                return ToCERO._FileObj.run_checks(conf, raise_exception=raise_exception)
            return ToCERO._FileObj.is_valid(conf, raise_exception=raise_exception)

        def import_file_as_cero(self):
            """
            Executes the import process.
            :return pandas.DataFrame: The CERO.
            """

            self["file"] = ToCERO._FileObj._find_file(self["file"], self["search_paths"])

            try:
                df = self._import_file() # _import_file documents the state of df.
            except xlrd.biffh.XLRDError as e:
                msg = e.__str__() + " Failed to import file '%s' - invalid sheet name." % self["file"]
                ToCERO._logger.error(msg)
                raise ImportError(msg)
            except Exception as e:
                msg = e.__str__() + " Failed to import file '%s'." % self["file"]
                ToCERO._logger.error(msg)
                raise e.__class__(msg)

            # Throw away unnecessary rows
            if self.get("series"):
                df = ToCERO._FileObj._filter_series(df, [series["name"] for series in self["series"]])
                assert isinstance(df, pd.DataFrame)
                assert isinstance(df.index, pd.Index)

                for series in self["series"]:

                    # Rename rows if specified
                    if "rename" in series:
                        ds = df.loc[series["name"],]
                        ds.name = series["rename"]
                        df = df.append(ds) # Note that this will move data series to the end of dataframe.
                        df.drop(labels=series["name"], inplace=True)
                        assert (series[
                                    "rename"] in df.index.tolist())  # Check new name has been properly added to the series

            assert isinstance(df, pd.DataFrame)

            # Find year in strings
            if isinstance(df.columns, pd.Int64Index):
                # Assumption: If column names are interpreted as integers, the integers must be years
                ts = pd.to_datetime(df.columns, format="%Y")
            else:
                try:
                    ts = pd.Series([re.match(self["time_regex"], x).group(1) for x in df.columns.tolist()])
                except AttributeError as e:
                    msg = ("Error attempting to perform string matching on datetime values for file '%s'. A " +\
                          "likely cause is too few datetimes for the size of the data array.") % self["file"]
                    ToCERO._logger.error(msg)
                    raise e.__class__(msg)
                ts = pd.to_datetime(ts, format=self["time_fmt"])  # Interpret as datetime

            df.columns = ts

            if "prepend" in self:
                new_values = [_Identifier.prepend_identifier(self["prepend"], name) for name in df.index.tolist()]
                df.index = CERO.create_cero_index(new_values)

            CERO.is_cero(df) # Will raise exception if invalid CERO

            return df

        @staticmethod
        def _find_file(file, search_paths: list, raise_exception=True):
            """
            Locates first occurance of ``file`` on ``search_paths`` and returns relative OS-specific path.

            :return str:
            """
            orig_filename = file
            file = os.path.relpath(os.path.normpath(file))
            for sp in search_paths:
                test_path = os.path.join(sp, file)
                msg = "ToCERO.find_file(): testing path: %s" % test_path
                ToCERO._logger.debug(msg)
                if os.path.isfile(test_path):
                    return os.path.abspath(test_path)
                    # return test_path
            else:
                msg = "File '%s' not found on any of the paths %s." % (orig_filename, search_paths)
                ToCERO._logger.error(msg)
                if raise_exception:
                    raise FileNotFoundError(msg)
                print(msg)
                return False

        @staticmethod
        def _check_permissions(file, raise_exception=True):
            try:
                fp = open(file, 'r')
                fp.close()
            except PermissionError:
                msg = "Current user - '%s' - does not have permissions to read file '%s'." % (getpass.getuser(), file)
                ToCERO._logger.error(msg)
                if raise_exception:
                    raise PermissionError(msg)
                print(msg)
                return False
            return True

        def _import_file(self) -> pd.DataFrame:
            """
            Executes appropriate function depending on file type, returning a ``pandas.DataFrame`` that is not necessarily of CERO type.
            :return: ``pandas.DataFrame``. ``df`` (the returned dataframe) must be of have identifiers as the index and the time-based data in columns. The index should be of CERO type, which can be ensured by using the ``CERO.create_CERO_index()`` method.
            """

            if self.get("type") not in ToCERO._FileObj.supported_file_types:
                raise TypeError(("\'type\' for input file %s is either: (a), not provided/inherited/deduced; " +
                                 "or (b), not supported. Supported types are %s.") % (self["file"],
                                                                                      ToCERO._FileObj.supported_file_types))

            elif self["type"] in ['xlsx', 'xls', 'csv']:
                df = self._import_csv_or_xlsx()

            elif self["type"] == 'gdx':
                df = self._import_gdx()

            elif self["type"] in ['har', 'shk']:
                df = self._import_har()

            elif self["type"] in ['vd']:
                df = self._import_vd()

            # If df does not fit these requirements, must be error in import...
            assert isinstance(df, pd.DataFrame)
            assert isinstance(df.index, pd.Index)

            try:
                df = df.astype(pd.np.float32, copy=False)
            except ValueError as e:
                raise e.__class__("Invalid dataframe type detected. One possible reason is invalid columns - " +
                                  "for example, columns that do not refer to a year when other columns do.")

            return df

        def _import_csv_or_xlsx(self) -> pd.DataFrame:
            # CSV/XLSX specific operations

            pd_opts = self.copy()
            file = pd_opts.pop("file")

            # This is messy, but there's not a neat way to select only pandas-relevant options
            read_csv_kwargs = set(["filepath_or_buffer", "sep", "delimiter", "header",
                                   "names", "index_col", "usecols", "squeeze", "prefix", "mangle_dupe_cols", "dtype",
                                   "engine", "converters", "true_values", "false_values", "skipinitialspace",
                                   "skiprows", "nrows", "na_values", "keep_default_na", "na_filter", "verbose",
                                   "skip_blank_lines", "parse_dates", "infer_datetime_format", "keep_date_col",
                                   "date_parser", "dayfirst", "iterator", "chunksize", "compression", "thousands",
                                   "decimal", "lineterminator", "quotechar", "quoting", "escapechar", "comment",
                                   "encoding", "dialect", "tupleize_cols", "error_bad_lines", "warn_bad_lines",
                                   "skipfooter", "skip_footer", "doublequote", "delim_whitespace", "as_recarray",
                                   "compact_ints", "use_unsigned", "low_memory", "buffer_lines", "memory_map",
                                   "float_precision"])
            read_excel_kwargs = set(["io", "sheet_name", "header", "skiprows", "skip_footer", "index_col",
                                     "names", "usecols", "parse_dates", "date_parser", "na_values", "thousands",
                                     "convert_float", "converters", "dtype", "true_values", "false_values",
                                     "engine", "squeeze"])

            if self["type"] == "csv":
                pandas_kwargs = read_csv_kwargs
            elif self["type"] in ["xlsx", "xls"]:
                pandas_kwargs = read_excel_kwargs

            for opt in list(pd_opts.keys()):
                if opt not in pandas_kwargs:
                    pd_opts.pop(opt, None)  # Get rid of pandas-irrelevant options. Some of the options ^^ may \
                    # refer to other file types.

            pd_op = "read_csv"  # Changed later to read_excel if necessary

            if "usecols" not in self:
                if self.get("skip_cols") is not None:
                    if self["type"] in ["csv"]:
                        # Need this parameter to skip irrelevant columns of data
                        if isinstance(self["skip_cols"], str):
                            self["skip_cols"] = [self["skip_cols"]]
                        sk_col_list = self["skip_cols"]
                        pd_opts["usecols"] = lambda x: x not in sk_col_list
                    else:
                        raise TypeError("'skip_cols' is a valid option for files of 'csv' type only.")

            if self["type"] in ['xlsx', 'xls']:
                # Check excel-specific requirements
                if self.get("sheet", None) is None:
                    raise TypeError(
                        "Key-value pair \"sheet: SHEET\" must be specified for file \'%s\'." % self["file"])
                else:
                    pd_opts["sheet_name"] = self["sheet"]
                    pd_op = "read_excel"

                if self.get("header") and not self.get("skiprows"):
                    self["skiprows"] = self["header"]
                    self["header"] = 0

            if isinstance(pd_opts.get("converters"), dict):
                for k, v in pd_opts["converters"].items():
                    if isinstance(v, str):
                        pd_opts["converters"][k] = getattr(builtins, v)

            # for k in ["header", "index_col", "nrows", "usecols"]:
            #     # Grab pandas-relevant options
            #     pd_opts[k] = self[k]

            pd_op = getattr(pd, pd_op)  # Identify the correct pandas read OPeration
            try:
                df = pd_op(file, **pd_opts)
                # Program will fail on the line above if:
                # - Pandas version <0.22 (failure observed when pandas = 0.20), AND
                # - read_excel operation, AND
                # - usecols is a string which has a column range in it, where one of the indices has more than
                #   one letter - e.g. usecols="B,C,E:AW".
            except ValueError as e:
                if re.match(r"^Passed header", e.__str__()):
                    raise ValueError(e.__str__() + ". This is likely because a range has been specified with a '-' instead of a ':'")
                raise e

            if self["type"] in ['xlsx', "xls"] and self.get("nrows"):
                df = df.iloc[:self["nrows"], :]

            if self.get("orientation", "") == "cols":
                # Put into CERO orientation if necessary
                df = df.transpose()

            df.index = CERO.create_cero_index(df.index.tolist())

            return df

        def _import_har(self) -> pd.DataFrame:

            # Load file using harpy
            try:
                hfo = harpy.HarFileObj.loadFromDisk(filename=self["file"])
            except PermissionError as e:
                raise e

            har_headers_list = hfo.getRealHeaderArrayNames()

            if not self.get("head_arrs", self.get("headers")): # "headers" is for backwards compatibility
                self["head_arrs"] = har_headers_list  # If "headers" not specified, get all headers
            if self.get("headers"):
                raise DeprecationWarning("Option 'headers' has been depracated in favour of 'head_arrs'.")

            header_dfs = []
            for header in self.get("head_arrs", self.get("headers")): # "headers" is for backwards compatibility

                if isinstance(header, str):
                    # If string, convert to dictionary
                    header = {"name": header}

                try:
                    assert isinstance(header, dict)
                except AssertionError:
                    raise TypeError("Invalid header format (can be either str or dict).")

                # Checks valid header name
                try:
                    assert (header["name"] in har_headers_list)
                except AssertionError:
                    msg = "\'%s\' is an invalid header name for file \'%s\'." % (header["name"], self["file"])
                    raise ValueError(msg)

                # Inherits time_dim, default_year from self if possible
                header["time_dim"] = header.get("time_dim", self.get("time_dim"))
                header["default_year"] = header.get("default_year", self.get("default_year"))

                header["obj"] = hfo.getHeaderArrayObj(header["name"])

                # ASSUMPTION: User wants to retrieve entire tensor
                # func = lambda x: header["obj"].SetElements[x]

                labels = OrderedDict()
                if header.get("time_dim"):
                    if isinstance(header["time_dim"], str):
                        # time_dim is positional index
                        for idx, s in enumerate(header["obj"]["sets"]):
                            if s["name"] == header["time_dim"]:
                                header["time_dim"] = idx
                                break
                        else:
                            raise ValueError("'time_dim' does not exist in har file.")
                    try:
                        assert isinstance(header["time_dim"], int)
                    except AssertionError:
                        raise TypeError("'time_dim' (for header %s) must be provided as an 'int' or 'str' - " +
                                        "an int if indexing the dimension in the header name list, or a str if " +
                                        "naming the time set." % header["obj"]["name"])

                    try:
                        assert (header["time_dim"] < len(header["obj"]["sets"]))
                    except AssertionError:
                        raise TypeError("Invalid 'time_dim' (for header %s) - integer (zero-indexed) is too large " +
                                        "for the number of sets." % header["obj"].HeaderName)

                    labels = [(x["name"], x["dim_desc"]) for i, x in enumerate(header["obj"]["sets"]) if i != header["time_dim"]]
                    time_dim_labels = header["obj"]["sets"][header["time_dim"]]["dim_desc"]

                    # Move that dimension to be the last...
                    tspse_tup = tuple([i for i in range(len(header["obj"]["sets"])) if i != header["time_dim"]] + [
                        header["time_dim"]])
                else:
                    if not header.get("default_year"):
                        raise ValueError(
                            "The 'default_year' option must be provided for har files that do not have a specified 'time_dim' (time dimension).")

                    # Assume we have to create time dimension...
                    time_dim_labels = ["%d" % header.get("default_year")]  # TODO: Ask Thomas what year the data references if time_dim is not specified

                    labels = [(x["name"], x["dim_desc"]) for x in header["obj"]["sets"]]
                    tspse_tup = tuple([i for i in range(len(header["obj"]["sets"]))])  # transpose-tuple

                array = header["obj"]["array"].transpose(tspse_tup)
                # ^^ ASSUMPTION: Sets and Elements in array have the same order as that HAR.Header.SetNames, SetElements
                # UPDATE: Checked with Florian that this assumption is correct.

                # Reshape into 2-dimensional array
                shape = [len(labs[1]) for labs in labels]
                new_dims = 1
                for i in range(len(shape)):
                    new_dims = new_dims * shape[i]
                new_dims = (new_dims, len(time_dim_labels))
                ToCERO._logger.debug("new_dims: %s" % (new_dims,))

                array = array.reshape(new_dims)  # Note that reshaping is in C-order, which is itertools.product() order
                columns = time_dim_labels

                labels = list(it.product(*[x[1] for x in labels]))
                labels = [_Identifier.tupleize_name(name) for name in labels]
                if self.get("har_auto_prepend"):
                    labels = [_Identifier.prepend_identifier(header["obj"]["coeff_name"], name) for name in labels]

                index = CERO.create_cero_index(labels)
                ToCERO._logger.debug("index: %s" % index)
                df = pd.DataFrame(data=array,
                                  index=index,
                                  columns=columns)
                header_dfs.append(df)

            return CERO.combine_ceros(header_dfs, overwrite=False, verify_cero=False)

        def _import_vd(self): # VEDA data file
            """ Import VEDA data files.

            Assumption: The number of columns in first line of data is consistent throughout file.

            :return: pandas.DataFrame (not of CERO type).
            """

            self["default_year"] = self.get("default_year", None)

            if not issubclass(type(self["date_col"]), int):
                raise TypeError("'date_col' for file '%s' must be provided as an int." % self["file"])

            if not issubclass(type(self["val_col"]), int):
                raise TypeError("'val_col' for file '%s' must be provided as an int." % self["file"])

            with open(self["file"], "r") as f:
                data = f.readlines()

            data = [l.rstrip() for l in data if (l[0] != "\n" and l[0] != "*")]  # Remove comments and empty lines
            data = [[l.rstrip("\"").lstrip("\"") for l in l.split(",")] for l in data] # Strip quotation marks

            def drop_data(line):
                try:
                    line[self["date_col"]] = int(line[self["date_col"]]) # Attempt to convert to int
                except ValueError:
                    if self["default_year"] is None:
                        return False # False has the effect of dropping this record...
                    line[self["date_col"]] = self["default_year"] # Set to the given default if provided
                return line

            data = list(map(drop_data, data))
            data = list(filter(None, data))

            no_cols = len(data[0]) # Assumes number of columns in first line holds for the rest
            index_col = [x for x in range(no_cols) if ((x != self["val_col"]) and (x != self["date_col"]))]

            df = pd.DataFrame(data=data)
            df.index = CERO.create_cero_index([[l[x] for x in index_col] for l in data])

            df = df[[self["date_col"], self["val_col"]]] # Remove the now-unneeded data
            df = df.pivot(columns=self["date_col"]) # NOTE: Pivot can change index to non-logical order
            df.columns = df.columns.droplevel()

            return df

        def _import_gdx(self) -> pd.DataFrame:
            """
            Import a gdx file. Some assumptions are made:

                * Year index is always the lowest-level in column hierarchy
                * gdxpds does not provide columns with distinct names (which is true at time of writing)

            :return:
            """

            parent_dict = self.copy()
            parent_dict.pop("file")

            sym_defs = {}
            sym_defs.update(parent_dict)

            if issubclass(type(self.get("symbols")), dict):
                self["symbols"] = [self["symbols"]]
            elif not issubclass(type(self.get("symbols", [])), list):
                raise TypeError("'symbols' must be provided as a dict, or a list of dicts. Each symbol must have 'name' and 'date_col' specified.")

            sym_tmp = []
            for sym in self["symbols"]:
                tmp = sym_defs.copy()
                if issubclass(type(sym), dict):
                    tmp.update(sym)
                else:
                    raise TypeError("Symbol '%s' is of invalid type (not a dict)." % (sym))
                sym_tmp.append(tmp)

            self["symbols"] = sym_tmp

            req_keys = ["name", "date_col"]
            for sym in self["symbols"]:
                try:
                    assert issubclass(type(sym), dict)
                except AssertionError as e:
                    ToCERO._logger.error("Symbol %s is not of dict type." % sym)
                    raise e
                try:
                    assert all([(k in sym) for k in req_keys])
                except AssertionError as e:
                    msg = "Symbol %s does not have all of %s specified." % (sym, req_keys)
                    ToCERO._logger.error(msg)
                    raise TypeError(msg)

            dfs_dict = OrderedDict([(sym["name"], gdxpds.to_dataframe(self["file"], sym["name"])[sym["name"]]) for sym in self["symbols"]])

            df_list = []
            for idx, sym in enumerate(self["symbols"]):
                df = dfs_dict[sym["name"]]

                # Renames the initial columns to a number string...
                col_labels = ["%d" % i for i in range(df.shape[1])]
                col_labels[-1] = "Value"
                col_labels[sym["date_col"]] = "YEAR"
                df.columns = pd.Index(col_labels)

                df.set_index(col_labels[:-1], inplace=True)
                new_level_order = [col_labels[sym["date_col"]]] + [x for i, x in enumerate(col_labels[:-1]) if i != sym["date_col"]]
                df = df.reorder_levels(new_level_order) #: Assumption: Year index is always the lowest-level in column hierarchy
                df = df.unstack(0)
                df.columns = df.columns.droplevel()
                df.index = pd.Index(df.index.tolist(), tupleize_cols=False)
                df_list.append(df)

            return CERO.combine_ceros(df_list, overwrite=False, verify_cero=False)

        @staticmethod
        def _filter_series(df: pd.DataFrame, names) -> pd.DataFrame:
            """Throws away unnecessary rows in ``df`` object."""
            s_list = []
            for name in names:
                try:
                    s = df.loc[(name,),].iloc[0]  # Ugly, but pandas isn't friendly with tuple index values
                    assert (isinstance(s, pd.Series))
                except KeyError as e:
                    msg = e.__str__() + (". There are several likely reasons: \n" + \
                                         "1. File orientation is in columns and this has not been specified.\n" +
                                         "2. Series names do not match those given in the file. Remember to " +
                                         "comma-separate the values if multiple columns are used as the index.\n"
                                         "3. Pandas is automatically converting the index values to a datatype other than " +
                                         "a string. Consider adding 'converters: {column_name: data_type}' to the configuration " +
                                         "file."
                                         )
                    raise KeyError(msg)
                except IndexError as e:
                    msg = ("Invalid series identifier. A cause for this error may be " +
                           "a lack of uniqueness in series identifier (consider expanding " +
                           "the number index columns).")
                    raise IndexError(msg)
                except AssertionError as e:
                    raise e
                s_list.append(s)
            df = pd.concat(s_list, axis=1).transpose()
            return df

    def __init__(self, conf: dict, *args, parent: dict=None, **kwargs) -> pd.DataFrame:

        """Loads a ToCERO configuration, suitable for creating CEROs from data files.

        :param 'Union[dict,str]' conf: The configuration dictionary, or a path to a YAML file containing the configuration dictionary. If a path, it must be provided as an absolute path, or relative to the current working directory.
        :param args: Passed to the superclass (`dict`) at initialisation.
        :param kwargs: Passed to the superclass (`dict`) at initialisation.
        """

        _conf = ToCERO.load_config(conf, parent=parent)
        super().__init__(_conf, *args, **kwargs)

        msg = "Loaded ToCERO configuration: %s" % self
        ToCERO._logger.debug(msg)

    def create_cero(self):
        """
        Create a CERO from the configuration (defined by ``self``).

        :return pd.DataFrame: A CERO is returned.
        """

        cero_series = []
        for file_obj in self["files"]:
            cero = file_obj.import_file_as_cero()
            cero_series.append(cero)

        cero = CERO.combine_ceros(cero_series, overwrite=[fo["overwrite"] for fo in self["files"]])
        return cero

    @staticmethod
    def load_config(conf, parent: dict=None):
        """

        :param 'Union[dict,str]' conf: A configuration dictionary, or a `str` to a path containing a configuration dictionary.
        :param dict parent: A dict from which to inherit.
        :return dict: The configuration dictionary (suitable as a ToCERO object).
        """
        _conf = {"header": 0,
                 "index_col": 0,
                 "time_regex": r".*(\d{4})$",
                 "time_fmt": r"%Y",
                 "search_paths": [],
                 "files": []}  # Defaults

        if parent is None:
            parent = {}

        _conf.update(parent)

        if isinstance(_conf["search_paths"], str):
            _conf["search_paths"] = [_conf["search_paths"]]

        if isinstance(conf, str):

            try:
                if not _conf["search_paths"]:
                    _conf["search_paths"] = os.path.abspath(os.path.dirname(conf))

                conf = read_yaml(conf) # If conf is a configuration file, this will succeed
            except UnicodeDecodeError:
                # Try auto-import (i.e. assumes that file is of default format) - not supported for all import formats
                # Works by feeding in appropriate kwargs
                conf_file_ext = os.path.splitext(conf)[1][1:].lower()

                if conf_file_ext in ["csv"]:
                    _conf["files"].append({"file": conf})
                elif conf_file_ext in ["xlsx", "xls"]:
                    _conf["files"].append({"file": conf, "sheet": "CERO"})

        conf = dict(conf)
        _conf.update(conf) # Arguments provided at initialisation supercede configuration file values

        if isinstance(_conf["search_paths"], str):
            _conf["search_paths"] = [_conf["search_paths"]]

        if not _conf["search_paths"]:
            _conf["search_paths"].append(os.path.abspath(".")) # Search in working directory if a dict is provided...

        par_dict = _conf.copy()
        par_dict.pop("files")  # Prevents infinite recursive inheritance
        for idx, file_obj in enumerate(_conf["files"]):
            try:
                _conf["files"][idx] = ToCERO._FileObj(file_obj, parent=par_dict)
            except TypeError:
                raise TypeError("'files' must be provided as a list.")

        return _conf

    @staticmethod
    def is_valid(conf, raise_exception=True):
        """
        Performs static validity checks on ``conf`` as a ``ToCERO`` object.

        :param dict conf: An object, which may or may not suitable as a ToCERO object.
        :param bool raise_exception: If `True` (the default) an exception will be raised in the event a test is failed. Otherwise (in this event) an error message is printed to stdout and `False` is returned.
        :return bool: A `bool` indicating the validity of ``conf`` as a ``ToCERO`` object.
        """

        if not issubclass(type(conf["files"]), list):
            msg = 'Files must be specified as a list (or a single item).' + \
                                 'For example:\n' + \
                                 'files:\n' + \
                                 '    - file: FILE_A\n' + \
                                 '      [properties of FILE_A] \n' + \
                                 '    - file: FILE_B\n' + \
                                 '      [properties of FILE_B] \n' + \
                                 '    - ... '
            ToCERO._logger.error(msg)
            if raise_exception:
                raise TypeError(msg)
            print(msg)
            return False

        for file_obj in conf["files"]:

            if not issubclass(type(file_obj), ToCERO._FileObj):
                msg = "Object '%s' is of '%s' type, not '_FileObj'." % (file_obj, type(file_obj))
                ToCERO._logger.error(msg)
                if raise_exception:
                    raise TypeError(msg)
                print(msg)
                return False

        return True

    @staticmethod
    def run_checks(conf, raise_exception=True):
        """
        Performs dynamic validity checks on ``conf`` as a ``ToCERO`` object.

        :param dict conf: An object, which may or may not suitable as a ToCERO object.
        :param bool raise_exception: If `True` (the default) an exception will be raised in the event a test is failed. Otherwise (in this event) an error message is printed to stdout and `False` is returned.
        :return bool: A `bool` indicating the validity of ``conf`` as a ``ToCERO`` object.
        """

        for file_obj in conf["files"]:

            if not ToCERO._FileObj.run_checks(file_obj, raise_exception=raise_exception):
                return False

        return True

    @staticmethod
    def check_config(conf, raise_exception=True, runtime=False):
        _conf = ToCERO.load_config(conf)
        if runtime:
            return ToCERO.run_checks(conf, raise_exception=raise_exception)
        return ToCERO.is_valid(_conf, raise_exception=raise_exception)

    @staticmethod
    def _find_file(file, search_paths: list, raise_exception=True):
        """
        Locates first occurance of ``file`` on ``search_paths`` and returns relative OS-specific path.

        :return str: The relative path to file.
        """
        orig_filename = file
        file = os.path.relpath(os.path.normpath(file))
        for sp in search_paths:
            test_path = os.path.join(sp, file)
            msg = "ToCERO.find_file(): testing path: %s" % test_path
            ToCERO._logger.debug(msg)
            if os.path.isfile(test_path):
                return test_path
        else:
            msg = "File '%s' not found on any of the paths %s." % (orig_filename, search_paths)
            ToCERO._logger.error(msg)
            if raise_exception:
                raise FileNotFoundError(msg)
            print(msg)
            return False
