Common ConCERO-Related Commands
===============================

This page serves to present some example commands on how to download, install and use ConCERO. To install ConCERO requires the installing git (a version control program).

Installing ConCERO
------------------

    #. Clone the source directory into ``DIR``:

        .. code-block:: shell

            git clone https://col530@bitbucket.csiro.au/scm/energy/concero.git DIR

    #. Change to the directory:

        .. code-block:: python

            cd DIR

    #. To get the latest version of the repository (if the first step was done a while ago):

        .. code-block:: python

            git pull

    #. Check that your python interpreter is version 3.4 or above:

        .. code-block:: python

            python --version

    #. Install ConCERO (may require administrator privileges):

        .. code-block:: python

            python setup.py install

    #. (Optional) Test installation has been successful:

        .. code-block:: python

            cd ..
            python -m concero.tests.test_concero

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

For Jupyter Notebooks
---------------------

Create a cero from a configuration file to_cero.yaml:

.. code-block:: python

    tc = concero.ToCERO(to_cero.yaml)
    cero = tc.create_cero()

Export the cero (or parts thereof) to a file, using the configuration in from_cero.yaml:

.. code-block:: python

    fc = concero.FromCERO(from_cero.yaml)
    fc.exec_procedures(cero)

