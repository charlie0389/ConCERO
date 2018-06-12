Welcome to ConCERO!
===================

ConCERO is a Python 3 based program for achieving two primary tasks:

    #. Automating the execution of economic models, and
    #. *Con*-verting both to and from the "Collins Economics Results Object" (*CERO*) into a variety of formats appropriate for the economic models such as:

      * VURM
      * LUTO
      * GALLM-E
      * GALLM-T
      * AusTIMES
      * GLOBIOM

By 'economic models', it is meant a computer program for calculating predictions of the future state of an economy. The list above is not exhaustive - **the interface supports expansion to any computer program that can be run from a command line/terminal interface.**

ConCERO is released under Version 3 of the Gnu General Public License (GPL). Please see the ``LICENSE`` file for a copy of the GPL v3.

Creating a common format facilitates automating the transfer of information between the economic models. Regardless of the economic models involved, ConCERO converts the output files of the listed economic models into appropriate input files with 2 simple steps.

  1. Convert the output file(s) of an economic model into a CERO.
  2. Convert the CERO into an appropriate input file(s) for a different economic model.

For a more detailed yet high-level overview of how ConCERO operates, please consult :ref:`Design_Philosophy`.

At the heart of the programs operation is appropriate configuration files which, once configured the first time, are unlikely to undergo significant alteration. Configuration files are written in ``YAML`` format and, for the sake of convention, should be named ``model_to_cero.yaml`` or ``cero_to_model.yaml``, where ``model`` is the name of the economic model. Do not be intimidated by the acronym - the YAML format is very simple and human readable. Typically, study of the YAML format should be unnecessary - how to alter the file is, in general, obvious if an example configuration file is accessible. Documentation for constructing the configuration file for converting *to* a CERO can be found at :ref:`to_cero` and *from* a CERO can be found at :ref:`from_cero`.

For a more thorough yet simple introduction to YAML files, `this webpage <http://docs.ansible.com/ansible/latest/YAMLSyntax.html>`_ is recommended, or reviewing the yaml files in the ``tests/data`` subdirectory of the ConCERO system directory, alongside the documentation, should be sufficient as an introduction to YAML.

The founding author of ConCERO is Lyle Collins, and can be contacted for questions and comments at `Lyle.Collins@csiro.au <Lyle.Collins@csiro.com>`_.

If you use this program for academic publications, a citation, such as below, is requested and much appreciated:

.. [1] Collins, Lyle D. *ConCERO\: Software for automating the execution of economic models and data format conversion between them.* CSIRO, Newcastle, Australia. 2018.

If using ``gdx`` files, the author of ``gdxpds`` (an underlying library) requests a citation:

.. [2] Hale, Elaine T. *gdxpds 1.0.4*. NREL, Colorado, USA. 2016. https://pypi.python.org/pypi/gdxpds/

The latest version of ``gdxpds`` (and citation format) can be found on `GitHub <https://github.com/NREL/gdx-pandas/tree/master/gdxpds>`_.

And if using ``har`` files, the authors of ``harpy`` - an underlying library - request a citation:

.. [3] F. Schiffmann and L. D. Collins, *"Harpy v0.3: A Python API to interact with header array (HAR) files,"* Melbourne, Australia, 2018, `<https://github.com/GEMPACKsoftware/HARPY>`_.

**Note regarding the use of '/' and '\\' in file names (applicable if running ConCERO on different operating systems)**: Note that different operating systems prefer a different style to define file locations. The Windows operating system uses the backslash (\\), whereas Linux/Mac based systems use the forward slash (/). **When specifying filenames for the purpose of using ConCERO, forward slashes (/) are preferred**. The reason being that '\\' is also the escape character in Python (for example, ``\n`` indicates a new line, not a backslash followed by 'n'). However, for filenames in YAML files, \\ is correctly interpreted as a directory separator on *Windows-based systems only*. This should not be considered a sufficient reason to use \\ in filenames, because it detracts from the operating-system independent nature of ConCERO, and it is reasonably likely that other operating systems will be used, especially in the context of supercomputers (for which Linux has >90% market share). In summary, / is preferred because ConCERO correctly interprets it on all operating systems, whereas \\ is correctly interpreted on Windows-based systems only.

**There is an exception to this guideline (regardless of the operating system in use).** When specifying commands to be executed (such as commands to execute a model run), it is *necessary* that the directory separator be the same style as that required by the operating system that the command is to be executed on. This is because the commands are passed directly to the command line (and it is infeasible for ConCERO to understand, parse and modify all the possible commands that may be used for either operating system style).

Contents:

.. toctree::
    :maxdepth: 3

    reference
    quickstart
    design_philosophy
    install_requirements
    tests
    cero
    to_cero
    from_cero
    libfuncs_wrappers
    scenarios
    models
    import_guidelines
    coding_guidelines
    modfuncs

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>