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
Output-Independent Instructions
-------------------------------

Setting up a FromCERO configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Like all other configuration files for this program, the configuration file must be in YAML format. The highest \
hierarchical level (i.e. with the least/no indentation) is referred to as a *FromCERO object*).
It is **necessary** (for the configuration to output anything meaningful) to define the option:

    * ``procedures: (list[dict|str])``, where ``procedures`` is a list of one or more *procedure* objects. \
    :ref:`procedure objects` are explained below .

Procedures define the mutation(s) and, if desired, the export of the mutated data to a file. If a procedure does not specify an export file then ConCERO will, by default, output the procedure to ``output.csv`` in the current working directory. The default output file can be overwridden by specifying the ``file`` option of the FromCERO object.

It is *recommended* that the following option be specified:

    * ``file: (str)`` - Names the file for which all procedure objects are exported into. Procedure objects will export \
     into this file unless a procedure-object-specific ``file`` has been defined. The extension of ``file`` determines \
     the exported file type. Supported file types are:

        * Numpy arrays - ``npy``
        * GAMS Data eXchange format - ``gdx`` (temporarily unsupported)
        * HAR files - ``har``
        * Shock files - ``shk``
        * Portable Network Graphics format - ``png``
        * Portable Document Format - ``pdf``
        * PostScript - ``ps``
        * Encapsulated PostScript - ``eps``
        * Scalable Vector Graphics - ``svg``

Other options include:

    * ``sets: (dict: str -> List[str])`` - sets is a dictionary mapping ``str`` to a ``list`` of  ``str``. ``sets`` provides \
    an easy and convenient way to select groups of CERO identifiers (see :ref:`cero_ids`), as opposed to simply listing \
    all the identifiers that are of interest for output. More detail about sets is provided below in the section :ref:`sets`.
    * ``map: (dict: str -> str)`` - key-value pairs that maps the "old" identifier to a "new" identifier.
    * ``ref_dir: (str)`` where ``ref_dir`` is a file path relative to the current working directory. By default, all \
    file names are interpreted as being relative to the configuration file. Providing this option overrides the default.
    * ``lstrip: (str)`` where ``str``, if provided, strips the left-most substring from all identifiers that make up the input. If the string does not match the start of the identifier (if the identifier is a `str`), or the first field of the identifier (if the identifier is a `tuple`), then a `ValueError` is raised. This option is designed to correspond to CEROs generated using ToCERO with the ``auto_prepend`` option provided.
    * ``libfuncs: (str|list[str])`` - paths relative to ``ref_dir`` of python files containing functions to use as operation functions. Note that the ``.py`` filename extension must be included. The structure of a libfuncs file is discussed below in :ref:`libfuncs_files`.

Note that, in general, properties at a lower level (i.e. more indentation) 'inherit' from a higher level.

So, an example configuration, in YAML format, is:

.. code-block:: yaml

    file: a_csv_file.csv
    procedures:
        - <Procedure Object A>
        - <Procedure Object B>
        - <Procedure Object C>
        - <etc.>

Examples of complete configuration files can be found in the ``tests/data`` subdirectory of the ConCERO install path.

.. _procedure objects:

Procedure Objects
#################

Conceptually, procedure objects provide the instructions to select data from a CERO, mutate that data (if necessary), \
and then either, (a): output this data into a file, or (b): return outputs for later export into a global file \
(specified by the ``file`` option in the outputs object). Any mutations that are applied to a procedure object's \
``inputs`` are isolated from any other procedure object and the CERO itself - i.e. each procedure can be \
considered a 'silo' separate from others.

A *procedure object* can be either a ``str`` or a ``dict``. The ``dict`` form is the more general form - if a \
procedure object is provided as the (``str``) ``ser_obj``, it is immediately converted to the equivalent form \
``{'name': ser_obj}``. The complete list of options is:

    * ``name: (str)`` - the name given to the procedure. Will, by default, given the name ``Unnamed_proc``.
    * ``file: (str)`` - if provided, the output from this procedure object, and only this procedure object, will \
    be exported to ``file``.
    * ``inputs: list(str|list(str))`` - is a list of identifiers corresponding to identifiers in the CERO. \
    If an item of the list is a string with one or more commas, or is itself a list, then the item will be \
    interpreted as a tuple-form identifier. See :ref:`cero_ids`.
    * ``outputs: list(str|list(str))`` - a list of identifiers that are to be exported to the file. If outputs \
    are not specified, then ConCERO will export all *updated* inputs after all operations are performed. Read \
    :ref:`output_process_flow` to understand what is meant by *updated* inputs. If it is desirable that none of the data \
    series be exported to a file in a conventional manner, which is the case if - for example - plotting output, \
    then specify ``outputs``, but leave the corresponding value blank to indicate a value of ``None``. \
    If an item of the list is a string with one or more commas, or is itself a list, then the item will be \
    interpreted as a tuple-form identifier. See :ref:`cero_ids`.
    * ``operations: list[operations objects]`` - to mutate the ``inputs`` into a desirable form for export, \
    operations must be applied to mutate the data. ``operations`` is a list of *operations objects*, which \
    modify the data in a sequential manner. See :ref:`operations_objects` for more information.
    * ``libfuncs: (str|list[str])`` - Identical in meaning to the equivalent ``FromCERO`` object option. Is inherited from a ``FromCERO`` object if not given.

Below is a shell showing the two different procedure object types:

.. code-block:: yaml

    procedures:
        - name: (str)
          inputs: (list[str])
          operations: (list[operation])
          output_file: (str)
        - (str)

The 1st procedure object is in dictionary form, and the 2nd is in string form.

Inheritance paths
#################

Below is an outline of how options are inherited:

    * ``inputs`` - If inputs is undefined, then ``inputs`` is the entire CERO (whatever that may be at runtime).
    * ``outputs`` - If outputs is undefined or ``True``, then all ``inputs`` are ``outputs``. If ``outputs`` is `False` or `None`, then there are no ``outputs``. A `list` or `str` can be provided to select specific ``outputs``.

.. _operations_objects:

Operations Objects
##################

An *operation* refers to the process of applying a function to some inputs to return an output(s). Unlike separate \
procedures, operations (within the same procedure object) can *not* be considered to operate in a 'silo-ed' manner, and \
therefore the order of ``operations`` is significant. Each item of the list ``operations`` must be an \
*operation object* - that is, a ``dict``, which may contain the options:

    * ``func: (str)`` - ``func`` is the name of a function present in a ``libfuncs`` library that is applied to \
    ``arrays`` (see below). The functions available \
    can be easily expanded by:
        #. Correctly identifying the class of the new function - see :ref:`func_classes`.
        #. Adding the function to a python source code file, *with the associated function decorator* (as explained in :ref:`func_classes`), and providing that file to ConCERO with the ``libfuncs`` *procedure* option. The system ``libfuncs.py`` will be searched after any referenced files.
    * ``arrays: list(str|list(str))`` - ``arrays`` defines which of the ``inputs`` that ``func`` will manipulate. If ``arrays`` is not provided, ``arrays`` defaults to all procedure object ``inputs``.  Note that any manipulation applied to ``arrays`` will be in effect for all subsequent ``operations``.
    * ``rename: (list|dict)`` - providing this option as a list renames ``arrays`` after the application of ``func`` (if provided). If ``rename`` is provided as a `list`, then the list is parsed as identifiers (see :ref:`cero_ids`) and must be the same length as ``arrays``. If provided as a `dict`, only those ``arrays`` matching keys in the dict are renamed to the corresponding value. Regardless of the form of ``rename`` (i.e. `list` or `dict`), references to ``sets`` can be made. In the specific case that there is one and only one ``arrays``, then ``rename`` can be provided as a `str`. If `rename` is provided and the new identifier values are not already in ``arrays``, then ``rename`` expands ``arrays`` to include the new identifers (and the data series corresponding to the original identifiers are left untouched). By using this behaviour, ``rename`` can be used to apply ``func`` to specific ``arrays`` without altering the original ``arrays``.
    * ``start_year: (int)`` - this option constrains the dataset to years after and **including** ``start_year``. This \
    option may be useful to avoid attempting to apply ``func`` to missing data.
    * ``end_year: (int)`` - this option constrains the dataset to years before and **including** ``end_year``. This \
    option may be useful to avoid attempting to apply ``func`` to missing data.

Any additional options are passed to ``func`` as keyword arguments.

.. _sets:

Sets
####

The ``sets`` option must have the following form:

``sets: dict[str -> list(str)]``

The ``sets`` option provides a powerful way to list many identifiers with a small amount of references. An example configuration of sets is:

.. code-block:: yaml

    sets:
        ASET:
            - a
            - b
            - c

A user can then specify all the elements of the set (for ``inputs``, ``arrays`` and ``outputs``) by referencing \
the set. For example:

.. code-block:: yaml

    sets:
        ASET:
            - a
            - b
            - c
            - d
            - e
    procedures:
        - name: a_procedure
          inputs: ASET
          operations:
            - func: a_func
        - name: b_procedure
          inputs: ASET
          operations:
            - func: b_func

Which is equivalent to the more verbose:

.. code-block:: yaml

    procedures:
        - name: a_procedure
          inputs:
            - a
            - b
            - c
            - d
            - e
          operations:
            - func: a_func
        - name: b_procedure
          inputs:
            - a
            - b
            - c
            - d
            - e
          operations:
            - func: b_func

Specifying ``sets`` is even more powerful when using them in the context of tuple-identifiers. For example, \
consider that these (100*100 = 10,000) identifiers were in the CERO (in python list form):

.. code-block:: python

    [('1', '1'), ('1', '2'), ('1', '3'), ..., ('1', '100'), ('2', '1'), ('2', '2'), ..., ('2', '100'),
     ('3', '1'), ..., ('3', '100'), ..., ('100', '100')]

Rather than listing all 10,000 identifiers, a user can create a set:

.. code-block:: python

    sets = {'century': ['1', '2', '3', ..., '100']}

and select all 10,000 identifiers by referencing the set twice with a comma inbetween - e.g. in YAML:

.. code-block:: yaml

    inputs:
        - century,century

Note that the selection takes place by using the cartesian product operation, and it is necessary that the \
cartesian product be convex.

.. _libfuncs_files:

Libfuncs Files
##############

A libfuncs file is a standard python source file. However, to use the definitions as operations in ConCERO, it is necessary to wrap the functions with specialised wrappers. Therefore, an example python source code file that provides ConCERO-compatible operations is:

.. code-block:: python

    from concero.libfuncs_wrappers import recursive_op

    @recursive_op
    def double_values(x):
        return 2*x

Where the ``double_values`` function will simply double the value of all input series. Note that ``series_op`` and ``dataframe_op`` are also wrappers to encapsulate functions to ensure they are ConCERO-compatible. For more information on how to use the wrappers, please consult :ref:`func_classes` .

.. _output_process_flow:

Description of the output process-flow
--------------------------------------

Each procedure object corresponds to the output of an object into a file. Every procedure takes inputs (from a CERO), mutates this inputs in some way (or not  and then outputs some, if not all, of the mutated inputs into a file. More specifically, in converting a CERO \
to an output file, the general process flow is:

    #. From the given CERO, identify using ``inputs`` the relevant data series by their identifier.
    #. Copy those ``inputs`` to avoid disturbing/mutating the original CERO.
    #. From the copied inputs, perform a sequence of operations where, for each operation:
        #. All of the ``inputs``, or a subset of ``inputs`` is selected (that is, the ``arrays``).
        #. A function mutates the ``arrays``.
        #. If given, ``arrays`` are ``rename`` d.
        #. The copied inputs get updated with the mutated ``arrays``. For values of ``arrays`` that match ``inputs``, those ``inputs`` are overwritten. Otherwise (in the event ``arrays`` have been ``rename`` 'd) they are added to ``inputs``.
    #. Export ``outputs`` to either:
        #. ``file``, if ``file`` is specified the procedure object, or
        #. ``file`` as defined in the FromCERO object, *if specified*, or
        #. ``output.csv`` if ``file`` is unspecified in either the procedure or FromCERO objects.


FromCERO Technical Specification
--------------------------------

.. autoclass:: FromCERO
    :members:

Created on Jan 22 08:44:08 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import concero.conf
if getattr(concero.conf, "gdxpds_installed", False):
    import gdxpds #: Warning given if not imported before pandas
import os
import copy
from collections import OrderedDict
import warnings
import getpass
import importlib.util
from types import ModuleType

import numpy as np
import pandas as pd

from concero.cero import CERO
import concero.libfuncs as libfuncs
from concero.format_convert_tools import read_yaml
from concero._identifier import _Identifier
import concero.libfuncs_wrappers as libfuncs_wrappers

warnings.simplefilter(action="ignore", category=FutureWarning)

class FromCERO(dict):
    sup_output_types = {'csv', 'xlsx', 'excel', 'npy', 'png', 'pdf', 'ps', 'eps', 'svg'}
    _logger = concero.conf.setup_logger(__name__)

    class _Procedure(dict):
        """_Procedure object class."""

        _sup_procedure_output_types = {'csv', 'xlsx', 'excel', 'npy', 'har', 'shk', 'png', 'pdf', 'ps', 'eps', 'svg'} # "gdx"

        def __init__(self, proc_dict: dict, *args, parent: 'FromCERO' = None, **kwargs):

            proc = FromCERO._Procedure.load_config(proc_dict, parent=parent)
            super().__init__(proc, *args, **kwargs)
            FromCERO._Procedure.is_valid(self)


        @staticmethod
        def load_config(proc_dict: dict, parent: 'FromCERO' = None):

            # Add default options here
            defaults = {"name": "Unnamed_proc",
                        "operations": [],
                        "inputs": [],
                        "ref_dir": None,
                        "sets": {},
                        "map": {},
                        "libfuncs": [],
                        }

            if parent is None:
                parent = {}

            defaults.update(parent)
            defaults.update(proc_dict)

            if defaults.get("ref_dir") is None:
                defaults["ref_dir"] = os.getcwd()
            defaults["ref_dir"] = os.path.abspath(defaults["ref_dir"])

            if defaults.get("file"):
                defaults["file"] = os.path.join(defaults["ref_dir"], os.path.relpath(defaults["file"]))

            if issubclass(type(defaults.get("libfuncs")), str):
                defaults["libfuncs"] = [defaults["libfuncs"]]

            lf_files = []
            for lf in defaults["libfuncs"]:
                if issubclass(type(lf), str) and lf in proc_dict.get("libfuncs", []):
                    lf = os.path.join(defaults["ref_dir"], lf)
                elif issubclass(type(lf), str):
                    pass
                elif issubclass(type(lf), ModuleType):
                    lf = lf.__file__
                else:
                    raise TypeError("'libfuncs' must be provided as a list of strings and/or modules (not %s)." % type(lf))

                lf_files.append(lf)

            # Ensure system libfuncs is on search path...
            system_libfuncs = concero.conf.find_file("libfuncs.py")
            if system_libfuncs not in lf_files:
                lf_files.append(system_libfuncs)
                defaults["libfuncs"].append(system_libfuncs)

            # Load all libfuncs modules
            mods = []
            for idx, (lf, mod) in enumerate(zip(lf_files, defaults["libfuncs"])):
                if issubclass(type(mod), str):
                    spec = importlib.util.spec_from_file_location(os.path.basename(lf), lf)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                mods.append(mod)
            defaults["libfuncs"] = mods

            # Load sets
            for k in defaults["sets"]:
                if isinstance(defaults["sets"][k], str):
                    defaults["sets"][k] = os.path.join(defaults["ref_dir"], defaults["sets"][k])
                    defaults["sets"][k] = read_yaml(defaults["sets"][k])

                defaults["sets"][k] = FromCERO._load_set(defaults["sets"][k])

            if isinstance(defaults["inputs"], str):
                defaults["inputs"] = [defaults["inputs"]]

            # Determine identifiers for all inputs
            defaults["inputs"] = _Identifier.get_all_idents(defaults["inputs"], sets=defaults["sets"])

            if "lstrip" in defaults:
                defaults["inputs"] = [_Identifier.lstrip_identifier(defaults["lstrip"], inp) for inp in defaults["inputs"]]

            if "outputs" in defaults:
                if isinstance(defaults["outputs"], str):
                    defaults["outputs"] = [defaults["outputs"]]

                if issubclass(type(defaults["outputs"]), list):
                    defaults["outputs"] = _Identifier.get_all_idents(defaults["outputs"], sets=defaults["sets"])
                elif defaults["outputs"] == True:
                    defaults.pop("outputs")
                elif defaults["outputs"] == False:
                    defaults["outputs"] = None
                elif defaults["outputs"] is None:
                    pass
                else:
                    raise ValueError("'outputs' must be provided as a list, True or None.")

            return defaults


        def _set_inputs(self, cero: pd.DataFrame):
            """Copies each data series in ``cero`` indexed by the items in ``inp_list`` to an ``OrderedDict``. This \
                    ensures that ``operations`` do not alter ``cero``.
                    """
            if self["inputs"] == []:
                # Input is entire CERO unless otherwise specified
                self["inputs"] = cero.index.tolist()

            # Check values in dataframe - check is necessary because KeyError is not thrown if some values are in index (pandas version 0.22).
            invalid_inputs = [i for i in self["inputs"] if i not in cero.index]

            try:
                self.inputs = copy.deepcopy(cero.iloc[[cero.index.get_loc(loc) for loc in self["inputs"]]]) # Reduce data frame to necessary data and copy
            except KeyError:
                invalid_inputs = [i for i in self["inputs"] if i not in cero.index]
                msg = ("Inputs %s do not exist. The most likely reason is that the configuration file is " +
                       "incorrectly specified, or lacks specification. If debugging level has been set to " +
                       "'DEBUG', then the input list is in the log file - note that this list may be " +
                       "extraordinarily long. Common causes of this problem include: \n" +
                       " 1. Set definition in configuration file includes elements that do not exist in the CERO.\n" +
                       " 2. Mis-spellings of identifiers in the configuration file (which includes names of sets for 'inputs' or 'arrays').\n" +
                       " 3. Incorrect ordering of sets in the identifier."
                       ) % invalid_inputs
                FromCERO._logger.error(msg)
                raise KeyError(msg)

            assert (isinstance(self.inputs, pd.DataFrame))

            map_dict = {}
            for map_op in self.get("map", []):

                idx = map_op.get("idx")
                orig_s = self["sets"][map_op["orig"]]
                ns = self["sets"][map_op["new"]]

                for val in self.inputs.index.values:

                    new_val = val

                    if idx is not None and (val[idx] in orig_s) and (not isinstance(val, str)):
                        new_val = val[:idx] + (ns[orig_s.index(val[idx])],) + val[idx+1:]
                    elif val in orig_s:
                        new_val = ns[orig_s.index(val)]

                    map_dict.update({val: new_val})
                CERO.rename_index_values(self.inputs, map_dict, inplace=True)

        def exec_ops(self, cero):
            """
            :param cero: The cero (``pandas.DataFrame``) object upon which to execute the operations. No modifications will be applied to the original cero (i.e. all modifications are applied to a copy of ``cero``).
            :return:
            """

            self._set_inputs(cero)

            for op in self["operations"]:
                ret = self._exec_op(op)
                if ret is not None:
                    self.inputs = CERO.combine_ceros([self.inputs, ret], overwrite=True)

            if "outputs" in self and self["outputs"] is None:
                # The result of this procedures operations is to be explicitly ignored, may be useful when objective is simply to plot data
                return

            if (self.get("outputs", []) == []) or (self.get("outputs", True) == True):
                    # Get all rows if none specified
                    self["outputs"] = self.inputs.index.tolist()

            out_df = self.inputs.iloc[[self.inputs.index.get_loc(o) for o in self["outputs"]]]

            assert issubclass(type(out_df), pd.DataFrame)

            if "file" in self:
                # If file is specified, all 'outputs' from this procedure go to its own file
                output_type = os.path.splitext(self["file"])[1][1:]
                FromCERO.dataframe_out(out_df, self["file"], output_type, self.get("output_kwargs"))
            else:
                # procedure output name is that provided
                return {self["name"]: out_df}

        def _exec_op(self, op: dict):

            # Apply operation to procedure
            func_name = op.pop('func', "noop") # Perform noop (no-operation) if no func provided.
            op_args = op.pop('args', [])
            rename = op.pop("rename", None)

            arrays = None
            if "arrays" in op:
                arrays = op.pop("arrays")
                if issubclass(type(arrays), str):
                    arrays = [arrays]
                arrays = _Identifier.get_all_idents(arrays, sets=self["sets"])

            for mod in self["libfuncs"]:
                if hasattr(mod, func_name):
                    func = getattr(mod, func_name)
                    break
            else:
                msg = ('Invalid function name provided - \'%s\'. Function does not exist in any of the modules %s. It may be necessary to create a python module with the necessary functions and provide this file with the \'libfuncs\' option.' %
                            (func_name, self["libfuncs"]))
                FromCERO._logger.error(msg)
                raise AttributeError(msg)

            FromCERO._logger.debug("Function call: %s(*arrays, **op)" % func.__name__)

            ret = func(self.inputs, *op_args, locs=arrays, **op)
            op['func'] = func.__name__  # For cleanliness of presentation

            if rename is not None:

                if ret is None:
                    ret = getattr(libfuncs, "noop")(self.inputs, *op_args, locs=arrays, **op)

                if isinstance(rename, str):
                    rename = {ret.index.tolist()[0]: rename} # Rename the first index by default

                if issubclass(type(rename), list):
                    # Build mapping dictionary
                    rename = _Identifier.get_mapping_dict(ret.index.tolist(), rename, sets=self.get("sets"))
                elif issubclass(type(rename), dict):
                    rename = _Identifier.get_one_to_one_mapping(rename, sets=self.get("sets"))

                # At this point, rename should be one-to-one mapping dict

                renamed = CERO.rename_index_values(ret.loc[list(rename.keys())], rename, inplace=False)
                ret = renamed.loc[list(rename.values())]  # Restrict renamed to only the rows that have been specified

                # Note that ret will be restricted to only those values that have been renamed.

            return ret

        def _check_ops(self, raise_exception=True):
            for operation in self["operations"]:

                if not issubclass(type(operation), dict):
                    msg = '\'%s\' is not a valid operation type. Operations must be of dict type, not %s.' % (operation,
                                                                                                              type(operation))
                    FromCERO._logger.error(msg)
                    if raise_exception:
                        raise TypeError(msg)
                    print(msg)
                    return False

                if "func" in operation:

                    for mod in self["libfuncs"]:
                        if hasattr(mod, operation["func"]):
                            break
                    else:
                        msg = ('Invalid function name provided - \'%s\'. Function does not exist in any of the modules %s. It may be necessary to create a python module with the necessary functions and provide this file with the \'libfuncs\' option.' %
                                    (operation["func"], self["libfuncs"]))
                        FromCERO._logger.error(msg)
                        if raise_exception:
                            raise AttributeError(msg)
                        print(msg)
                        return False

            return True

        @staticmethod
        def is_valid(proc, raise_exception=True):

            if not proc.get("name"):
                msg = "Invalid procedure object - no 'name' given."
                FromCERO._logger.error(msg)
                if raise_exception:
                    raise KeyError(msg)
                print(msg)
                return False

            if not issubclass(type(proc["operations"]), list):
                msg = "'operations' for procedure '%s' must be of list format." % proc["name"]
                FromCERO._logger.error(msg)
                if raise_exception:
                    raise TypeError(msg)
                print(msg)
                return False

            if proc.get("operations", []) and not "libfuncs" in proc:
                msg = "If 'operations' are defined, then so must be 'libfuncs' (for process '%s')." % proc["name"]
                FromCERO._logger.error(msg)
                if raise_exception:
                    raise TypeError(msg)
                print(msg)
                return False

            if not issubclass(type(proc.get("libfuncs", [])), (str, list)):
                msg = "'libfuncs' for procedure '%s' must be of str or list format." % proc["libfuncs"]
                FromCERO._logger.error(msg)
                if raise_exception:
                    raise TypeError(msg)
                print(msg)
                return False

            if not FromCERO._Procedure._check_ops(proc, raise_exception=raise_exception):
                return False

            if proc.get('file'):
                file_type = os.path.splitext(proc["file"])[1][1:]  # get file extension without full stop

                if file_type not in FromCERO._Procedure._sup_procedure_output_types:
                    msg = "Output type '%s' not supported. Supported types are: %s." % (file_type,
                                                                                        FromCERO._Procedure._sup_procedure_output_types)
                    FromCERO._logger.error(msg)
                    if raise_exception:
                        raise TypeError(msg)
                    print(msg)
                    return False

                if not FromCERO._check_permissions(proc["file"], raise_exception=raise_exception):
                    return False

            return True

        @staticmethod
        def run_checks(proc, cero, raise_exception=True):
            """
            Checks that the _Procedure ``proc`` is valid and can be executed by the current user.
            :return:
            """

            cero_index = cero.index.tolist()
            invalid_inputs = [v for v in proc["inputs"] if v not in cero_index]
            if invalid_inputs:
                msg = "Inputs %s are not valid." % invalid_inputs
                FromCERO._logger.error(msg)
                if raise_exception:
                    raise FromCERO._Procedure.InvalidInputs(msg)
                return False
            return True

        def get_inputs(self):
            return self.inputs

        @staticmethod
        def from_obj(obj, *args, **kwargs):
                # Code to convert procedure to dict type (the superset of supported types)
            if isinstance(obj, str):
                obj = {"name": obj}
            try:
                assert issubclass(type(obj), dict)
            except AssertionError:
                msg = "Object provided can not be converted to a procedure. Objects provided must be a dict, or a subclass of."
                FromCERO._logger.error(msg)
                raise TypeError(msg)
            proc = FromCERO._Procedure(obj, *args, **kwargs)
            return proc

        def get_filepath(self, filename):
            filename = os.path.relpath(filename)
            ret = os.path.join(self["ref_dir"], filename)
            FromCERO._logger.debug("get_filepath() returns: %s" % ret)
            return ret

        class InvalidInputs(ValueError):
            pass

    def __init__(self, conf: dict, *args, parent=None, **kwargs):
        """
        Any additional arguments and keyword arguments are passed to the superclass at initialisation (i.e. the `dict` class).

        :arg "Union[str,dict]" conf: A dictionary containing the configuration. If a `str` is provided, it is interpreted as a file (in YAML format) containing a configuration dictionary (relative to the current working directory).
        :arg dict parent: If provided, the created object will inherit from ``parent`` (a `dict`).
        """

        _conf = FromCERO.load_config(conf, parent=parent)
        FromCERO.is_valid(_conf)

        super().__init__(_conf, *args, **kwargs)

        FromCERO._logger.debug("self.procedures: %s" % self["procedures"])

    def exec_procedures(self, cero):
        """ Execute all the procedures of the FromCERO object
        .
        :param pandas.DataFrame cero: A CERO to serve as input for the procedures. The argument is not mutated/modified.
        """

        CERO.is_cero(cero, raise_exception=True, empty_ok=False)

        CERO.rename_index_values(cero, self.get("map", {}))

        self.output_procedures = OrderedDict()

        for procedure in self["procedures"]:

            try:
                ret = procedure.exec_ops(cero)
                # if ret is not None, should be dict with key: procedure["name"], value: resultant CERO
            except Exception as e:
                raise e.__class__(e.__str__() + " Error in procedure '%s'." % (procedure["name"]))

            if ret is None:
                ret = {}

            self.output_procedures.update(ret)
        else:
            if not self["procedures"]: # If empty list
                self.output_procedures["default_output"] = cero

        if any([not procedure.get("file") for procedure in self["procedures"]]):
            msg = "It has been detected that not all procedures direct output to file. Therefore some output will go to \'%s\'." % self["file"]
            print(msg)
            FromCERO._logger.info(msg)

        if self.output_procedures != {}:
            file_ext = os.path.splitext(self["file"])[1][1:]
            if file_ext in FromCERO.sup_output_types:
                out_df = CERO.combine_ceros(list(self.output_procedures.values()))
                FromCERO.dataframe_out(out_df, self["file"], output_type=file_ext)
            elif file_ext in FromCERO._Procedure.sup_output_types:
                raise ValueError("This data type is not supported for general export, because it probably has a more than 2 dimensions - export using 'procedures' instead.")
            else:
                raise ValueError("Unsupported data type detected for general export.")

    def get_filepath(self, filename):
        ret = FromCERO.get_relpath(self["ref_dir"], filename)
        FromCERO._logger.debug("get_filepath() returns: %s" % ret)
        return ret

    @staticmethod
    def get_relpath(base_dir: str, filename: str) -> str:
        filename = os.path.relpath(filename)
        return os.path.join(base_dir, filename)

    @staticmethod
    def _load_set(set: "List[str]"):

        set = _Identifier.get_all_idents(set)

        try:
            assert (issubclass(type(set), list))
        except AssertionError:
            msg = "Each set must be provided as a list, not type '%s' for object %s." % (
                type(set), set)
            FromCERO._logger.error(msg)
            raise TypeError(msg)

        return set


    @staticmethod
    def load_config(conf, parent=None):
        """
        Loads configuration of FromCERO. If conf is a `str`, this is interpreted as a file (in YAML format) containing a configuration dictionary (relative to the current working directory). Otherwise conf must be a dictionary.

        :param 'Union[str,dict]' conf:
        :return dict:
        """

        _conf = {"operations": [],
                 "file": "output.csv",
                 "sets": {},
                 "map": {},
                 "ref_dir": None, # Type: str
                 "procedures": [],
                 "libfuncs": []}  # Defaults

        if parent is None:
            parent = {}

        _conf.update(parent)

        if isinstance(conf, str):
            if _conf["ref_dir"] is None:
                _conf["ref_dir"] = os.path.abspath(os.path.dirname(conf))
            conf = read_yaml(conf) # Load configuration file

            if conf is None: # Loading an empty file
                raise TypeError("Attempted to load an empty file.")

        _conf.update(conf)

        if _conf.get("ref_dir") is None:
            _conf["ref_dir"] = os.path.abspath(os.getcwd())

        _conf["file"] = FromCERO.get_relpath(_conf["ref_dir"], _conf["file"])

        system_libfuncs = concero.conf.find_file("libfuncs.py")
        if system_libfuncs not in _conf.get("libfuncs", []):
            _conf["libfuncs"].append(system_libfuncs)

        # Load sets
        for k in _conf.get("sets", {}).keys():

            # If provided as a string, assume to be a file relative to ref_dir
            if isinstance(_conf["sets"][k], str):
                _conf["sets"][k] = os.path.join(_conf["ref_dir"], _conf["sets"][k])
                _conf["sets"][k] = read_yaml(_conf["sets"][k])

            _conf["sets"][k] = FromCERO._load_set(_conf["sets"][k])

        file_ext = os.path.splitext(_conf["file"])[1][1:]
        if file_ext in [".", ""]:
            raise TypeError("'file' must be specified with an extension.")

        for idx, procedure in enumerate(_conf["procedures"]):

            if isinstance(procedure, str) and str.lower(os.path.splitext(procedure)[1][1:]) in ["yaml", "yml"]:
                # If given a YAML filename, interpret as link to YAML dict
                _conf["procedures"][idx] = FromCERO.get_relpath(_conf["ref_dir"], procedure)
                _conf["procedures"][idx] = read_yaml(_conf["procedures"][idx])

            parent = _conf.copy()
            parent.pop("procedures")  # Avoid recursive inheritance loop
            parent.pop("file")  # Procedure should not output to file unless a file is specified

            if not _conf["procedures"][idx].get("name"):
                _conf["procedures"][idx]["name"] = "Unnamed_proc_%d" % idx

            _conf["procedures"][idx] = FromCERO._Procedure.from_obj(_conf["procedures"][idx], parent=parent)

        return _conf

    @staticmethod
    def is_valid(conf: dict, raise_exception=True):
        """
        Performs static checks on ``conf`` to verify if ``conf`` can be converted to a FromCERO object.

        Checks include:
            * Valid type.
            * Valid procedures.
            * If ``file`` given, that the user has write permissions in that directory.

        :param dict conf: The object to check the validity of.
        :param bool raise_exception: If `True` (the default) then an exception will be raised on failure. Otherwise an error message will be printed to stdout and `False` returned.
        :return bool: `True` if ``conf`` passes all static checks.
        """

        if not issubclass(type(conf), dict):
            msg = "Configuration is of type %s (that is, not a dictionary)." % type(conf)
            FromCERO._logger.error(msg)
            if raise_exception:
                raise TypeError(msg)
            print(msg)
            return False

        if any([not issubclass(type(procedure), FromCERO._Procedure)for procedure in conf["procedures"]]):
            msg = "Not all procedures are FromCERO._Procedure objects."
            FromCERO._logger.error(msg)
            if raise_exception:
                raise TypeError(msg)
            print(msg)
            return False

        if any(["file" not in procedure for procedure in conf["procedures"]]):
            if not FromCERO._check_permissions(conf["file"], raise_exception=raise_exception):
                return False

        for procedure in conf["procedures"]:
            if not FromCERO._Procedure.is_valid(procedure, raise_exception=raise_exception):
                return False

        return True

    @staticmethod
    def run_checks(conf: dict, cero: pd.DataFrame, raise_exception=True):
        """
        Performs runtime checks on ``conf``, given ``cero``.

        :param dict conf: The object to check the validity of.
        :param bool raise_exception: If `True` (the default) then an exception will be raised on failure. Otherwise an error message will be printed to stdout and `False` returned.
        :return bool: `True` if ``conf`` passes all runtime checks.
        """
        for procedure in conf["procedures"]:
            if not procedure.run_checks(cero, raise_exception=raise_exception):
                return False

        return True

    @staticmethod
    def check_config(conf, raise_exception=True, runtime=False):
        conf = FromCERO.load_config(conf)
        if runtime:
            return FromCERO.run_checks(conf, raise_exception=raise_exception)
        return FromCERO.is_valid(conf, raise_exception=raise_exception)

    @staticmethod
    def _check_permissions(file, raise_exception=True):
        try:
            test_file = os.path.join(os.path.dirname(file), ".write_test.tmp")
            fp = open(test_file, "w")
        except PermissionError:
            msg = "User '%s' does not have write permissions in directory '%s'." % (getpass.getuser(),
                                                                                    os.path.dirname(file["file"]))
            FromCERO._logger.error(msg)
            if raise_exception:
                raise PermissionError(msg)
            print(msg)
            return False
        finally:
            fp.close()
            os.remove(test_file)
        return True

    @staticmethod
    def dataframe_out(df: pd.DataFrame, output_file: str, output_type: str, output_kwargs: dict=None):

        if df.empty:
            msg = "CERO is empty - no data to export."
            print(msg)
            FromCERO._logger.warning(msg)
            return

        output_file = output_file + "." + output_type if os.path.splitext(output_file)[1] == "" else output_file
        if output_type.lower() in ['npy']:
            FromCERO._numpy_out(df.values, output_file, output_kwargs=output_kwargs)
        elif output_type.lower() in ['png', 'pdf', 'ps', 'eps', 'svg']:
            FromCERO._plot(df, output_file, output_kwargs=output_kwargs)
        elif output_type.lower() in ["csv"]:
            FromCERO._csv_out(df, output_file, output_kwargs=output_kwargs)
        elif output_type.lower() in ["xlsx", "excel"]:
            FromCERO._xlsx_out(df, output_file, output_kwargs=output_kwargs)
        elif output_type.lower() in {"gdx"}:
            FromCERO._gdx_out(df, output_file, output_kwargs=output_kwargs)
        else:
            raise TypeError("Output files of this type cannot be created from dataframes. It will be necessary " + \
                            "to create your own output function in concero.libfuncs and call it as an operation.")

    @staticmethod
    def _csv_out(df: pd.DataFrame, output_file: str, output_kwargs: dict=None, **kwargs):
        defaults = {"date_format": "%Y"}

        # Update with given arguments
        if output_kwargs is None:
            output_kwargs = {}
        defaults.update(output_kwargs)
        output_kwargs = defaults

        df.to_csv(output_file, **output_kwargs)

    @staticmethod
    def _xlsx_out(df: pd.DataFrame, output_file: str, output_kwargs: dict=None, **kwargs):

        defaults = {"columns": df.columns.strftime("%Y"),
                    "sheet_name": "CERO",
                    "tupleize_cols": False}

        # Update with given arguments
        if output_kwargs is None:
            output_kwargs = {}
        defaults.update(output_kwargs)
        output_kwargs = defaults

        df.index = pd.Index(df.index.tolist(), tupleize_cols=defaults.pop("tupleize_cols")) # Convert to multi-index for nice formatting

        df.to_excel(output_file, **output_kwargs)

    @staticmethod
    def _numpy_out(obj: np.array, output_file: str, output_kwargs: dict=None):
        if output_kwargs is None:
            output_kwargs = {}
        np.save(output_file, obj, **output_kwargs)

    @staticmethod
    def _gdx_out(df: 'Dict[str, pd.DataFrame]', output_file: str, output_kwargs: dict=None):
        """
        Note: output_kwargs is in signature for compatibility with other output functions. output_kwargs could be \
        implemented but is not currently.

        :param df:
        :param output_file:
        :param output_kwargs:
        :return:
        """
        if output_file[-4:] != '.gdx':
            output_file += '.gdx' # Add file extension if necessary

        # out_obj = copy.deepcopy(out_obj)

        # for out_ser, out_df in df.items():
        try:
            assert (issubclass(type(df), pd.DataFrame))
        except AssertionError as e:
            raise e
        libfuncs_wrappers._rename(df, df.index.values[0], "Value")
        df = df.transpose()
        df['Year'] = df.index.strftime('%Y') # Convert datetimes to strings
        df[out_ser] = df[['Year', 'Value']] # Reorder


        with gdxpds.gdx.GdxFile() as gdxf:

            # for out_ser, out_df in df.items():
            # Create a new set with one dimension
            gdxf.append(gdxpds.gdx.GdxSymbol(out_ser, gdxpds.gdx.GamsDataType.Parameter, dims=['Index']))
            gdxf[-1].dataframe = df
            gdxf.write(output_file) # Create a new parameter with one dimension

        FromCERO._logger.info("Exported to file \'%s\' successfully." % output_file)

    @staticmethod
    def _plot(out_obj: pd.DataFrame, output_file: str, output_kwargs: dict=None):
        if output_kwargs is None:
            output_kwargs = {}
        plotformat=os.path.splitext(output_file)[1][1:]
        libfuncs.plotdf(out_obj, figurepath=output_file, plotformat=plotformat, **output_kwargs)
