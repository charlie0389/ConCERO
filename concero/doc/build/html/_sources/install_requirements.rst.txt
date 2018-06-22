.. _install_requirements:

Installing ConCERO
==================

Installing ConCERO from PIP (recommended)
-----------------------------------------

The simplest way to install ConCERO is through pip:

    ``pip install concero``

**NOTE: It is assumed PyQt4 (required for matplotlib) is already installed. If not, refer to** :ref:`pyqt-install` **.**

For GDX file support, please refer to :ref:`gams-install` and :ref:`gdxpds_install`.

Installing ConCERO from source
------------------------------

Change to the source directory and execute:

    ``python3 setup.py install``

To check that the installation was successful, run the test suite:

    ``python3 -m concero.tests.test_concero``

Assuming ConCERO has been installed successfully, you can identify how to run ConCERO, and the available options (by reading the documentation) or with the command:

    ``concero --help``

.. [1] To check whether this library (``lib``) is installed (correctly), the simplest way is to open python on the command line. Then, in the python interpreter, execute ``import lib``, where ``lib`` is the relevant library. If no errors are raised, then the program is installed correctly.

Installing ConCERO using Anaconda
---------------------------------

If the environment manager *Anaconda* is installed, a ConCERO environment can be installed by executing:

    ``conda env create -f concero/misc/concero_env.yaml``

**NOTE:** If installing using this method, the PyQt4 manual install process can be skipped. The manual install process for Harpy is still required however.

.. _gdxpds_install:

Installing gdxpds (necessary for gdx files)
-------------------------------------------

Can be done through pip:

    ``pip install gdxpds``

.. _gams-install:

Install GAMS Python API
-----------------------

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

.. _pyqt-install:

Installing PyQt4
----------------

PyQt4 is necessary to use the plotting functionalities of ConCERO, which relies on `matplotlib`.

**All platforms:** If using Anaconda, then

    #. Execute command ``conda install pyqt=4`` .

**NOTE - Windows Only**: It *may* be necessary to install PyQt4 on Windows through a manual process:

    #. Download the appropriate ``PyQt4`` package from `<https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4>`_.
    #. From the directory containing the downloaded file, execute from the command line ``pip install <downloaded PyQt4 file>`` .


Dependencies and Assumed Knowledge
==================================

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

Known Bugs
==========

``xlrd`` is an excel spreadsheet file-reading program. It will be installed by default with ``pandas``, but may not be of a sufficiently high version. On Windows, a bug in older versions may cause an exception to be raised when reading legitimate excel files. To upgrade ``xlrd``, run the command:

    ``pip install xlrd --upgrade``

