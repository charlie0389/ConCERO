Models
======

.. _model_objects:

Model Objects
-------------

A model object must be of dictionary form and *may* have the following options:

    * ``name: (str)`` - the name of the model (for referencing purposes). The value of ``name`` does not alter scenario execution.
    * ``cmds: (command object|list[command objects])`` - a single *command object*, or a *list* of *command objects*. Command objects are discussed below here - :ref:`command_objects`. A good placeholder command (to test if the data conversion process works for example) is ``echo "Model running..."`` which simply outputs the text ``"Model running..."`` to the terminal.
    * ``input_conf: (str|list[str])`` - the input configuration file (or `list` of input configuration files) that specify the export of data *from* a given CERO (typically passed from a ``Scenario`` object) *into* appropriate input files for the model.
    * ``output_conf: (str|list[str])``- the output configuration file (or `list` of output configuration files) that specifies the import of data *into* a CERO (typically returned to a ``Scenario`` object) *from* the appropriate output files for the model.
    * ``wd: (str)``- the path to be the *working directory* for all executed commands (specified with ``cmds``).
    * ``search_paths: (str|list[str])``- a search path, or list of search paths, to look for ``input_conf`` and ``output_conf``.

.. _command_objects:

Command Objects
---------------

Command objects can be provided as either a ``str``, or a ``dict``. A ``dict`` is the more general form - if a command object is provided as a string ``cmd``, this is immediately converted to the equivalent command object ``{"args": cmd}``.

A command object *must* have the option:
    * ``args: (str|list[str])`` - how this is provided depends on the ``type`` of the command. If ``type: shell`` (the default), then a string corresponding to a console-based command should be provided. If ``type: python_method``, then a list of positional arguments (to be given to a python method) should be provided.

Currently, two different command types are supported, and is specified with the option:

    * ``type: ("shell"|"python_method")`` - explanations of the two types follow (``"shell"`` is default):
        * ``"shell"`` command is run from the command line and so therefore is, in general, operating-system *dependent*. Commands of this type take other options that correspond to keyword arguments of the ``subprocess.check_output()`` method - see the `subprocess documentation <https://docs.python.org/3.4/library/subprocess.html>`_ for more information. Commands of this type, by default, have the ``shell: True`` option provided as well (in contrast to the subprocess defaults). If this option needs to be changed, you'll know why, so no explanation is given here.
        * ``"python_method"`` - commands of this type execute a (python) method that has to be included in the module ``modfuncs.py`` so are, in general operating-system *independent*. For commands of this type, the ``func`` option must be provided. In addition to ``args``, the available options are:
            * ``func: (str)`` - this (required) option specifies the method in the ``modfuncs`` module to execute.
            * ``kwargs: dict[str -> objects]`` - ``kwargs`` is provided to the python method as keyword arguments.

Running VEDA-type models
------------------------

VEDA-type models include:

    * AusTIMES

Valid commands
^^^^^^^^^^^^^^

To run VEDA, the following command is sufficient:

``C154.nexus.csiro.au\c:\VEDA\VEDA_FE\GAMS_WRKANO2\VTRun.cmd``

After appropriately creating this using the interactive version of VEDA.

To provide alternative parameter input values, there will be a handful of files like (same folder)

elc_only_a1.dd
eis_price_cet_bounds.dd
cet_bounds_tsb.dd
transport_ci_sc.dd

which will have their values changed from scenario to scenario.

The processes for changing their values will be similar to the spreadsheets in the folder
C:VEDA\VEDA_Models\CSIRO_TIMES_ANO2_20180209\SuppXLS

With names like

Scen_elc_only_a1.xls
Scen_eis_price_cet_bounds.xls
Scen_cet_bounds_tsb.xls
Scen_transport_ci_sc.xls

With the first and last of the above taking inputs from VURM results.

The results from AUSTIMES are files that look like

C154.nexus.csiro.au\c:\VEDA\VEDA_FE\GAMS_WRKANO2\AusT_ET_zTw.VD

Models Technical Reference
--------------------------

.. autoclass:: model.Model
    :members:
