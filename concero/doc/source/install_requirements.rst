.. _install_requirements:

Install Requirements and Assumed Knowledge
==========================================

This documentation assumes the reader is familiar with basic python data types, particularly:

    * integers (``int``)
    * floating-point numbers (``float``)
    * booleans (``bool``)
    * strings (``str``)
    * lists (``list``)
    * dictionaries (``dict``)

To run this program, the user will need

 * python 3 (>= 3.5),
 * pandas (>= 0.23),
 * seaborn (>=0.8.1),
 * xlrd (>= 1.1.0),
 * pyyaml and
 * openpyxl (which is actually an unlisted dependency of `pandas`).

installed. ``matplotlib`` provides plotting functionality and ``seaborn`` is a plotting library that basically 'makes matplotlib plots look nice'. PyYAML provides YAML read functionality (necessary to read all the configuration files). No attempt has been made to make ConCERO backwards compatible with python 2. Unfortunately, it may be necessary to go through a rather arduous install process if it is necessary to have support for gdx file reading and/or har files (described below).

``xlrd`` is an excel spreadsheet file-reading program. It will be installed by default with ``pandas``, but may not be of a sufficiently high version. On Windows, a bug in older versions may cause an exception to be raised when reading legitimate excel files. To upgrade ``xlrd``, run the command:

    ``pip install xlrd --upgrade``

Installing PyQt4
----------------

PyQt4 is necessary to use the plotting functionalities of ConCERO, which relies on `matplotlib`.

**All platforms:** If using Anaconda, then

    #. Execute command ``conda install pyqt=4`` .

**NOTE - Windows Only**: It *may* be necessary to install PyQt4 on Windows through a manual process:

    #. Download the appropriate ``PyQt4`` package from `<https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4>`_.
    #. From the directory containing the downloaded file, execute from the command line ``pip install <downloaded PyQt4 file>`` .

Install GAMS Python API (Incomplete)
------------------------------------

The instructions in this section are only relevant if it is necessary to interact with GAMS ``.gdx`` files.

- Supported platforms for the GAMS Python API can be found at 'Supported Platforms' at \
  https://www.gams.com/latest/docs/API_MAIN.html#GAMS_HLAPIS_SUPPORTED_PLATFORMS.

- Install instructions and tutorial for GAMS Python API can be found at \
  https://www.gams.com/latest/docs/API_PY_TUTORIAL.html.

- Installing is dramatically simpler if you use a python interpreter that matches the version of the installed GAMS \
  python API. The 'bitness' (i.e. 32 bit or 64 bit) of your python interpreter has to match that of the installed \
  GAMS Python API.

- If your runtime version of python is *greater* than that of the installed version of GAMS, the necessary files to be \
  symlinked into corresponding directories are contained in <GAMS install directory>/apifiles/Python/api_<version>\
  /build/lib.

You may get warnings regarding the python version mismatch.

Installing gdxpds (necessary for gdx files)
-------------------------------------------

If working with the ``.gdx`` data type, in addition to ConCERO's requirements, it is necessary to install:

 1. GAMS python API - more details of which can be found at `the GAMS website <https://www.gams.com/latest/docs/API_PY_TUTORIAL.html#PY_GETTING_STARTED>`_ - and
 2. gdxpds,

*in that order*.

Installing/using the GAMS API is much easier (and probably more reliable) if the version of the python interpreter matches the version of the installed GAMS API files. That is, using Python 3.4 interpreter with Python 3.4 GAMS API. GAMS will complain even if the interpreter is more recent than that - for example, a version 3.5 interpreter with a 3.4 GAMS API. It is possible to install it anyway and link libraries manually, but that is a non-trivial process.

*gdxpds* will complain if it is not imported before pandas. Where possible, this program intends to heed this warning, but this may not always be the case, and so far, no adverse affects have been discovered by failing to heed the warning. Future versions of this program may remove this dependency.

Installing harpy (necessary for har or shk files)
-------------------------------------------------

Installing harpy is a simple process. The source code can be found at `github <https://github.com/GEMPACKsoftware/HARPY>`_. To install harpy, download the zip archive ('Clone or Download' -> 'Download ZIP'), extract into a directory, change into that directory, and run the command:

    ``python setup.py install``

If you have both python 2 and python 3 on your system, the install command may instead be:

    ``python3 setup.py install``

Installing ConCERO
------------------

Similar to harpy, the install command is either:

    ``python setup.py install``

or

    ``python3 setup.py install``

depending which command corresponds to the python 3 interpreter. To check that the installation was successful, run the test suite:

    ``python3 -m concero.tests.test_concero``

Assuming ConCERO has been installed successfully, you can identify how to run ConCERO, and the available options (by reading the documentation) or with the command:

    ``concero --help``

.. [1] To check whether this library (``lib``) is installed (correctly), the simplest way is to open python on the command line. For example - ``python``. Then, in the python interpreter, execute ``import lib``, where ``lib`` is the relevant library. If no errors are raised, then the program is installed correctly.

Installing ConCERO using Anaconda
---------------------------------

If the environment manager *Anaconda* is installed, a ConCERO environment can be installed by executing:

    ``conda env create -f concero/misc/concero_env.yaml``

**NOTE:** If installing using this method, the PyQt4 manual install process can be skipped. The manual install process for Harpy is still required however.


