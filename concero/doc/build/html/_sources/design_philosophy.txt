.. _Design_Philosophy:

.. default-role:: py:obj

ConCERO's Design Philosophy
===========================

ConCERO was built to achieve two objectives:

    1. automate the conversion of data formats between models, and
    2. automate the execution of models,

where a *model* is a computer program that calculates a prediction on some aspect of the \
Australian economy (given input data).

How, in general terms, the program accomplishes this is discussed below.

Automating Data Format Conversion
---------------------------------

A core concept in the data conversion process is that the data exchanged between any two of the economic models is one or more instances of a single *fundamental data type* - that is, a named time-indexed series of floating-point values. The data comes in many forms (e.g. ``csv``, ``xlsx``, ``har`` files), but is, conceptually, a set of one or more instances of the fundamental data types.

For example, consider a spreadsheet table with a list of names in the first column (column ``A``) that *names* the remainder of the row of data. Each of those values in the rows have *meaning* with respect to time, so therefore it can be said that each row is a instance of the fundamental data type - each row is a named, time-indexed series of floating point values. Sometimes, it may be the case that the time-index values do not reside in the same file as the values, but the fact remains that the *values have meaning with respect to time*.

**A set of one or more of these fundamental data types is referred to as a CERO - a Collins Economic Results Object**. \

Conveniently, in the python (version 3) programming language, `pandas.DataFrame` objects (as defined in the ``pandas`` library) are ideally suited for storing CEROs. Consequently, ConCERO uses the ``pandas`` python library extensively, and stores CEROs as ``pandas.DataFrame`` objects, and the terms *CERO* and *DataFrame* are considered interchangeable in this documentation. For the purposes of ConCERO and data format conversion, a CERO is a special type of ``pandas.DataFrame`` - in addition to the defining requirements of a ``pandas.DataFrame``, a CERO is required to have:

    1. the columns indexed by a ``pandas.DatetimeIndex`` object, and
    2. the rows indexed by a ``pandas.Index`` object, where each value is either a

        1. `str`, where each `str` does not have any commas (``,``), or a
        2. `tuple`, where each element of the `tuple` is a `str` (also without any commas).

    3. all values are of a floating-point type [1]_ (specifically, the values must be a subclass of ``numpy.float32`` type), and
    4. all column values must be unique, and
    5. all index values must be unique.

Currently, ConCERO does not enforce requirements 2.1 or 2.2, but successful program operation is not \
guaranteed if those requirements are not adhered to.

By using the CERO format, data can be converted between any two data formats by a simple two-step process:

    1. Mutating the data into the CERO format.
    2. Mutating the data from the CERO format into another format.

These two processes are captured respectively by the ``ToCERO`` and ``FromCERO`` classes, in the ``to_cero.py`` and \
``from_cero.py`` modules respectively. For a more technical overview, please see :ref:`to_cero` and :ref:`from_cero`.


.. [1] The values can be of ``numpy.nan`` (not-a-number) type, to be interpreted as 'the lack of a value'. However, there is a type of ``numpy.nan`` that is a subclass ``numpy.float32``, so this is not a breach of the technical requirement.

.. _automating_execution:

Automating the Execution of Models
----------------------------------

Before an overview of how the models are executed, it is first necessary to provide an introduction to the context \
in which ConCERO was built. As part of the *'Australian National Outlook'* (ANO) project, it was necessary to run a \
variety of *scenarios*. A 'scenario', with respect to the ANO project, is a collection of \
*stances* on particular *issues* that ultimately determine how predictions (regarding the state of the future Australian \
economy) are calculated. For example, one particular *issue* is the 'future of work'. All of the scenarios conducted as \
part of the ANO project took 1 of 2 *stances* on this issue. That is, 'automation would destroy work' or \
'jobs would evolve'.

For the purposes of ConCERO, a *scenario* refers to a specific collection of *stances*, but also references:
    * the associated models,
    * the input data to each of these models,
    * the output data from each of these models,
    * the procedure to execute each of the models, and
    * the order of execution, of each model (with respect to the other models).

Where, as described previously, a *model* [2]_ refers to the computer program that calculates a prediction (on some aspect \
of the Australian economy) based on the given input data.

Given this information, ConCERO was designed to run in accordance with the following procedure:

    1. Retrieve as much input data as possible to run all of the models, and convert this into a 'scenario-level' CERO. Refer to :ref:`to_cero`.

    2. Convert selected parts of the 'scenario-level' CERO into a suitable format as input for the first model (where 'first' refers to its order of execution). Refer to :ref:`from_cero`.

    3. Execute/run the first model.

    4. Convert any output data - that is necessary as input for subsequent [3]_ models - into a CERO and combine with the 'scenario-level' CERO. Refer to :ref:`to_cero`.

    5. Repeat steps 2-4 for any subsequent models.

    6. After all models have been executed/run, convert data in the scenario-level CERO into a format suitable for plotting, visualisation etc. Refer to :ref:`from_cero`.


.. [2] Given the economic nature of the models, sometimes the term *'models'* may be used interchangeably with the term *'economic models'*.
.. [3] 'Subsequent' refers to the order of execution.

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>