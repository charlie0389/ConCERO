# Installing and Using ConCERO

Please consult ConCERO's documentation for installation instructions. Please also note that citing ConCERO (and any relevant dependent libraries) is requested and appreciated. Citation instructions can be found on the main page of ConCERO's documentation. The documentation can be read by downloading ConCERO as a zip file, extracting the zip and then opening, in a web browser, the file:

`concero/doc/build/html/index.html`

# Quick Example 1 - Data Format conversion

Note that this example assumes the CSV is in the default format - one header row labelling the years the data refers to, the first column names the data, with all following columns containing floating-point (or integer) numbers (corresponding to each year labelled in the header). An example file could be:

```
EnergyUse,2018,2019,2020
Gas,5,10,15
Coal,20,10,5
Oil,15,12,9.5
```

More complex files (for example, HAR files) require more specification - please see *Converting TO the Collins Economics Result Object (CERO) format* and *Converting FROM the Collins Economics Result Object (CERO) format* for a complete outline.

1. Create the import file ``import_data.yaml``, to import the file ``import_data.csv``:

    ```yaml
    files:
        - file: import_data.csv
    ```

   *Note that correct indentation, and the use of spaces for indentation, is critical*. The file must be in YAML format - a very simple and easy to understand format. See the documentation page *Building a YAML file from scratch to convert TO the CERO format* for more information about the YAML format and links to resources.

2. Create the export file ``data_export.yaml``, to export to the file ``xslx_file.xlsx``:

    ```yaml
    procedures:
       - file: export_data.xlsx
    ```
    The definition of files/data to be imported and exported is now complete.

3. To create ``export_data.xlsx``, from the command line (and assuming the system python interpreter is version 3.5 or above) run:

    ```concero convert import_data.yaml export_data.yaml```

    In the working directory, you will find that ``export_data.xlsx`` has been created.

# Quick Example 2 - Data Format Conversion and Model Execution

Lets assume that export_data.xlsx serves as the input file for a model (in the form of a python script ``model.py``), and we want to (a) convert data formats **and** (b) run the model, in a single run (the 'single run' is referred to as a *scenario*).

1. The first step is to create `example_scenario.yaml`:

    ```yaml
    input_conf: import_data.yaml
    models:
        - input_conf: data_export.yaml
          cmds: python model.py

2. Execute the scenario:

    ```concero run example_scenario.yaml```

More examples can be found on the *Quickstart: Common ConCERO-Related Commands* page.

# Introduction and Features

 ConCERO allows for automatic data format conversion for data that is time-based. ConCERO was designed to make it easy for distributed projects to automate the conversion of data formats. Initially, ConCERO was designed so that multiple economic forecasting models could easily be run, and data transferred between them (e.g. the output data of one model can be used as input to another). This is a non-trivial exercise because economic forecasting models come in a variety of types - from proprietary programs to simple python scripts. However, they do all have one thing in common - all input and output data is time-referenced. ConCERO exploits this similarity - this allows the user to write simple files that define the structure of the input/output data files, and using these files ConCERO automates the data format conversion. Furthermore, ConCERO can automate the execution of the models themselves, creating a pipeline of execution of economic models and data format conversion.

 - Documented
 - Simple API that can be used from a python script, or by defining data structure files in YAML syntax
 - Can execute any program that has a command line interface
 - Distributed nature

# Bug Reporting

Please submit bug reports to "Issues" - the issue tracker (with this Github project).

# Dependencies/Attributions:

 - Pandas - a data analytics library.
 - Harpy - used to interact with .har files (commonly associated with the program RunDynam written by GEMPACK software).
 - Gdxpds - used to interact with .gdx files (associated with the program GAMS).
 - Numpy - for number/matrix/array calculations.
 - Pyyaml - for reading/writing YAML files.
 - Matplotlib - for plotting.
 - Seaborn - makes matplotlib plots look nice.
 - Xlrd - for interacting with xlsx files.

# FAQs

 - What does the name *ConCERO* mean?

 ConCERO means to Con-vert to/from between the Collins Economics Result Object (CERO). In the context of this program, a collection of data series in which every series can (a), be represented as a sequence of floating point numbers *indexed by a date* and (b), the series itself indexed/identified by a string (or sequence of strings), is referred to as a CERO.
