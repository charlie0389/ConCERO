Scenarios
=========

This section has been written with the assumption that :ref:`automating_execution` has already been read, and the reader is familiar with the term *option*, as described in :ref:`to_cero` and :ref:`from_cero`, with respect to YAML files.

Scenarios are generally run by using a *scenario definition file*, and like all other configuration files used with ConCERO, this file must be of YAML format.

Scenario Definition Files
-------------------------

At the highest level (i.e. no indentation) in a scenario definition file can be either a single *scenario definition object*, or a ``list`` of *scenario definition objects*.

Scenario Definition Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A scenario definition object must have the options:

    * ``models: list[model objects]`` - the structure of model objects are described here - :ref:`model_objects`.

And may have the options:

    * ``name: (str)`` - the name of the scenario. For example, ``'A1'`` or ``'ExistingTrends'``.
    * ``input_conf: (str)`` - an input configuration file that defines all of the scenario inputs. See :ref:`to_cero` for more information.
    * ``output_conf: (str)`` - an output configuration file that defines outputs from the scenario. See :ref:`from_cero` for more information.
    * ``run_no: (int)`` - An integer numbering the execution run of the scenario. By default is 1. This integer will appear in the filenames of any files output as intermediate steps.
    * ``export_mod_xlsx: (bool)`` - Exports the returned output from each of the models as an ``xlsx`` file, which allows the user to easily analyse whether results are sensible. The output file will have a name of the format ``<scenario_name>_<run_no>_<model["name"]>.xlsx``. The default is ``True``.
    * ``export_int_xlsx: (bool)`` - Exports the returned output from each of the intermediate steps in the scenario execution as an ``xlsx`` file, which allows the user to easily analyse whether results are sensible. Conceptually, the output is the CERO before the previous model execution, updated with the output of the previous model execution. The output file will have a name of the format ``<scenario_name>_<run_no>_step_<execution_step>.xlsx``, where ``execution_step`` is the (1-indexed) number of model executions. The default is ``True``.

.. _scenario_example:

Scenario Example
^^^^^^^^^^^^^^^^

An example scenario definition file that demonstrates all options is:

.. code-block:: yaml

    name: A1
    run_no: 1
    input_conf: data/test_scen_inputs.yaml
    export_mod_xlsx: False
    export_int_xlsx: False
    models:
      - name: example_model
        cmds: python dummy_model.py
        input_conf: data/test_model_input.yaml
        output_conf: data/test_model_output.yaml
        export_xlsx: False
    output_conf: data/test_scen_outputs.yaml

In the first run (``run_no: 1``) of  scenario ``A1``, scenario inputs are imported into a scenario level CERO, as defined by ``data/test_scen_inputs.yaml``. ``example_model`` is the first (and only) model to be run. ``data/test_model_input.yaml`` defines the data series of the CERO that are of interest to ``example_model`` and exports these data series into the input files for ``example_model``. The single command ``python dummy_model.py``, which defines the execution of ``example_model`` is then run from the command line in the current working directory. The relevant output data is defined by ``data/test_model_output.yaml`` - this output data is then converted into a CERO, which then updates the scenario-level CERO (overwriting any data series with the same identifier). Given that ``example_model`` is the last model to be run, the file ``data/test_scen_outputs.yaml`` defines the CERO data series of interest for export into files.

Scenario Technical Reference
----------------------------

.. autoclass:: scenario.Scenario
    :members:
