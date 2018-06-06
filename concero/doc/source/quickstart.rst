Common ConCERO-Related Commands
===============================

This page serves to present the most simple case of downloading, installing and using ConCERO. It is assumed that your python interpreter is version 3.4 or above (see *Other Commands* to identify your python version).

Installing ConCERO
------------------

    #. Download and extract the archive containing the source files
    #. From the command line, change into the source file directory:

        .. code-block:: python

            cd DIR

    #. Install ConCERO (which may require administrator privileges):

        .. code-block:: python

            python setup.py install

Example: Import a CSV file, export an XLSX file
--------------------------------------------------

Note that this example assumes the CSV is in the default format - one header row labelling the years the data refers to, the first column names the data, with all following columns containing floating-point (or integer) numbers (corresponding to each year labelled in the header). More complex files (for example, HAR files) require more specification - please see :ref:`to_cero` and :ref:`from_cero` for a complete outline.

    #. Create the import file ``import_data.yaml``, to import the file ``import_data.csv``:

        .. code-block:: yaml

            files:
               - file: import_data.csv

    #. Create the export file ``data_export.yaml``, to export to the file ``xslx_file.xlsx``:

        .. code-block:: yaml

            procedures:
               - name: export_data
                 file: export_data.xlsx

The definition of files/data to be imported and exported is now complete. To create ``export_data.xlsx``:

    #. Run the python interpreter (version 3.4 or above):

        .. code-block:: bash

            python

    #. The run the commands:

        .. code-block:: python

            import concero
            tc = concero.ToCERO("import_data.yaml") # creates the import object (a.k.a. a ``ToCERO`` object)
            cero = tc.create_cero("import_data.yaml") # creates a common object (a.k.a. a 'CERO')
            fc = concero.FromCERO("export_data.yaml") # creates the export object (a.k.a. a ``FromCERO`` object)
            fc.exec_procedures(cero) # execute the procedures defined in ``export_data.yaml`` on ``cero``.

In the working directory, you will find that ``export_data.xlsx`` has been created.

Example: Run a Model
--------------------

Anything that can be run from the command line can be run by ConCERO. Let's assume a model ``model.py`` is a python code defining the model we want to run.

    #. First, we create the scenario definition file, ``"example_scenario.yaml"``:

        .. code-block:: yaml

            name: example_scenario
            models:
                - name: a_model
                  exec_cmd: python model.py

       This scenario (an execution sequence of one or more models) has been named "example_scenario" (required).

    #. Then, from the command line:

        .. code-block:: bash

            concero example_scenario.yaml

    #. Alternatively, running the scenario could be accomplished in the python interpreter by executing the code:

        .. code-block:: python

            import concero
            s = concero.Scenario.load_scenario("example_scenario.yaml") # Loads the scenario from file
            s.run() # run the scenario

Example: Combining data import/export with model execution
----------------------------------------------------------

For this example - which builds on the previous 2 examples - let's consider that ``model.py`` requires ``export_data.xlsx`` to run successfully, and that file needs to be created from ``import_data.csv`` (as per the first example). Let's also assume that ``model.py`` will generate ``interesting_data.xlsx`` and that we wish to plot that data after the scenario has executed. ConCERO handles this operation by converting ``interesting_data.xlsx`` to a *CERO* and then generating a plot from the newly-created CERO (the process is identical to the import/export example).

Let's assume that ``model_output.yaml`` defines the import of ``interesting_data.xlsx`` and ``scenario_output.yaml`` defines the creation of interesting plots (and any other files we want to generate). We can change ``example_scenario.yaml`` (the YAML file created in the last example) to look like:

    .. code-block:: yaml

        name: example_scenario
        input_conf: import_data.yaml
        models:
            - name: a_model
              input_conf: data_export.yaml
              exec_cmd: python model.py
              output_conf: model_output.yaml
        output_conf: scenario_output.yaml

This file defines the process flow:

    #. Any input data that you (the user of ConCERO) wishes to convert (so to provide models such as ``a_model`` with input data) is imported and kept in an object referred to as a *CERO*. The line ``input_conf: import_data.yaml`` defines this.
    #. Data for the first model (``a_model``) is exported by converting the relevant parts of the CERO into the appropriate files. The line (in the model definition) ``input_conf: data_export.yaml`` defines this.
    #. Any data generated from the first model for which subsequent models require as input data must be imported (and stored in memory as a CERO). The model definition line ``output_conf: model_output.yaml`` defines this.
    #. The previous 2 steps are repeated for any subsequent models that you wish to execute. If this was the case, additional model definitions would follow underneath the definition for model ``a_model``.
    #. Finally, any data stored in memory (as a CERO) that is of interest to the user is exported into files. The line ``output_conf: scenario_output.yaml`` defines this.

It should hopefully be clear to the reader that there are 3 types of YAML files necessary to operate ConCERO:

    #. YAML files that define ``Scenario`` s.
    #. YAML files that define the conversion of data to a CERO.
    #. YAML files that define the conversion of data from a CERO.

Other Commands
--------------

       Note the for this example, the parent directory is chosen as the directory to run the tests. In practice, this could be any directory. Whatever directory is chosen, you must have write permissions.

    * Find help on how to use the ConCERO program:

        .. code-block:: python

            concero --help

    * Run the ConCERO scenario defined in ``scenario.yaml``:

        .. code-block:: python

            concero scenario.yaml

    * Perform a fake-run of the scenario defined in scenario.yaml (useful to check if there has not any 'obvious' errors with configuration files) ...

        .. code-block:: python

            concero --fake_run scenario.yaml

       Note that no runtime checks are performed (because successful operation may rely on the creation of some files that do not currently exist).

    * Test installation has been successful by running tests:

        .. code-block:: python

            cd ..
            python -m concero.tests.test_concero

       As long as their are no *failures*, then ConCERO has been installed correctly.

    * Clone the source directory into ``DIR`` using git:

        .. code-block:: shell

            git clone https://col530@bitbucket.csiro.au/scm/energy/concero.git DIR

    * Check version of your python interpreter:

        .. code-block:: python

            python --version
