# Installing and Using ConCERO

Please consult ConCERO's documentation for installation instructions. Please also note that citing ConCERO (and any relevant dependent libraries) is requested and appreciated. Citation instructions can be found on the main page of ConCERO's documentation. The documentation can be read by opening, in a web browser, the file:

`concero/doc/build/html/index.html`

# Quick Example

Note that this example assumes the CSV is in the default format - one header row labelling the years the data refers to, the first column names the data, with all following columns containing floating-point (or integer) numbers (corresponding to each year labelled in the header). More complex files (for example, HAR files) require more specification - please see :ref:`to_cero` and :ref:`from_cero` for a complete outline.

1. Create the import file ``import_data.yaml``, to import the file ``import_data.csv``:

    ```yaml
    files:
        - file: import_data.csv
    ```

   *Note that correct indentation, and the use of spaces for indentation, is critical*. The file must be in YAML format - a very simple and easy to understand format. See the documentation page *Building a YAML file from scratch to convert TO the CERO format* for more information about the YAML format and links to resources.

2. Create the export file ``data_export.yaml``, to export to the file ``xslx_file.xlsx``:

    ```yaml
    procedures:
       - name: export_data
         file: export_data.xlsx
    ```
    The definition of files/data to be imported and exported is now complete. To create ``export_data.xlsx``:

3. Run the python interpreter (version 3.4 or above): `python`.

4. Then run the commands:

    ```python
    import concero
    tc = concero.ToCERO("import_data.yaml") # Loads the import configuration file and creates the import object (a.k.a. a ``ToCERO`` object)
    cero = tc.create_cero("import_data.yaml") # creates a "common object" (a.k.a. a 'CERO')
    fc = concero.FromCERO("export_data.yaml") # Loads the export configuration file and creates the export object (a.k.a. a ``FromCERO`` object)
    fc.exec_procedures(cero) # Executes the procedures defined in ``export_data.yaml`` on the common object (``cero``).
    ```
    In the working directory, you will find that ``export_data.xlsx`` has been created.

More examples can be found on the *Quickstart: Common ConCERO-Related Commands* page.

# Bug Reporting

Please submit bug reports to the issue tracker (with this Github project).

# Dependencies/Attributions:

 - Pandas - a data analytics library.
 - Harpy - used to interact with .har files (commonly associated with the program RunDynam written by GEMPACK software).
 - Gdxpds - used to interact with .gdx files (associated with the program GAMS).
 - Numpy - for number/matrix/array calculations.
 - Pyyaml - for reading/writing YAML files.
 - Matplotlib - for plotting.
 - Seaborn - makes matplotlib plots look nice.
 - Xlrd - for interacting with xlsx files.