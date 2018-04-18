.. _import_guidelines:

Guidelines for painless importing of data
-----------------------------------------

The guidelines outlined in this document provide instructions on how to provide data to 'minimise the pain' with respect to creating configuration files that define the import of data. *A file that adheres to all of guidelines 1 to 9 (below), and the 2 mandatory constraints, is in the default format*. A file that is in the default format requires the minimal amount of specification to successfully import the file as a CERO. The minimal specification, in YAML format, being:

.. code-block:: yaml

    input_files:
        - file: name_of_file.csv

As mentioned, there are two mandatory requirements that **must** be fulfilled to successfully import the data into a CERO.

* **The identifiers of data series must be globally unique**. Please see guideline 6 for a more thorough explanation.
* **There are no commas in any identifier**.  Commas have a specific meaning in a identifer - ConCERO will interpret commas as an instruction to split the string at that location, such that the string ``"item A, item B"`` becomes the tuple ``("item A", "item B")``. So, please do not use commas unless you know precisely what you intend to happen by doing so.

The Guidelines
^^^^^^^^^^^^^^

    #. **​File names, and the names of the sheets within them (al\`a Excel workbooks), should remain the same for different scenario runs.** By extension, this means that you should avoid including a date reference in the file name itself, such as ``20180222`` (for example). If you wish to keep the old files, feel free to include a date reference in name of the old file, and give the new file the original name. If you are only able to follow one guideline, please make it this one - every change in a name means a change in a configuration file.

    #. **Input files are to be in csv format**.

    #. **One table per worksheet**. Each worksheet should have one, and only one, table of data. Do not include irrelevant data/tables in the same spreadsheet, such as tables to 'do some maths on the side'.

    #. **The time dimension of the data should be in columns**. For example, 2017 data (for the respective data series) occupies column ``B``, 2018 data column ``C``, etc.

    #. **The data header should occupy the first row, and only the first row**. For example, the first row header may look like: ``["MajorOccupationGroup", 2017, 2018, 2019, etc.]``.

    #. **The index column (containing the series 'identifiers') should be in the first column, and only the first column**. Furthermore, the identifiers (identifying the series in the row that follows) ​must be globally unique. Failure to adhere to the mandatory part of this guideline results in namespace conflicts - i.e. at a higher level, it is impossible to determine what data the identifier references from amongst multiple data sources. If you are unsure if the identifier of the series is globally unique, prefix the identifier with the model the data is associated with, or the name of the issue that the data refers to. Do not reference by scenario name. If your sanity requires some reference to the scenario, include a reference to the scenario in the sheet name. It may be the case in some instances it is unavoidable, or just unbearably ugly, to have the identifier in just one column (particularly if you wish to include units of measurement). In this case, don't fret - use multiple columns to identify the data series (whilst ensuring that the group of fields, together, is globally unique).

    #. **The years indexing the data, should have the year as the last 4 characters**. For example, ``'bs1b-br1r-pl1p-2021'``, ``'Y2021'`` and ``'2012'`` are all good choices of date format - the year is both 4 digits and the last characters. ``'21-x'`` is bad because it violates both of these requirements (the year - 2021 - is 2 digits and it is not last in the string).

    #. **Avoid gaps/empty cells**. There should be no space between the header (in the first row) and the data, no space between the data and the index column (ideally column A), no empty columns between columns etc. Basically, the data should be one big continuous block that sits in the upper left corner of the sheet.

    #. **Avoid strange characters**. Please stick to alphanumeric characters to identify series (a-z, A-Z, 0-9). Please don't use %, \*, /, \\, (, ) or anything else that doesn't look like english. Very importantly (and discussed previously), don't use commas (,).

    #. Avoid spaces if possible. This is the least important of all the guidelines and has been deliberately left unbolded, because it shouldn't affect anything. As general practice, computers don't like spaces and humans don't easily catch them, so it's generally a good habit to avoid them - just cut them out altogether, not just for this program, but in general when dealing with computers. If you must have something to break up the words for readability, underscores ( _ ) are a good replacement. Consider this 'a quick brown fox jumps over a lazy dog '. Now, is there one or two spaces between 'brown' and 'fox'? It's not easy to tell in the event it was mistyped... The space on the end however (if it wasn't for the quotes) would be impossible for a human to pick up on, and is a critical difference for a computer.

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>