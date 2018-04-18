Running Tests
=============

ConCERO comes with a suite of tests to verify installation has been successful. If no errors are raised upon running ``python3 -m concero.tests.test_concero``, then installation has been successful.

Tests are available in the ``tests`` subdirectory. Test modules and classes have the same name as the module/class it tests, with the exception that the string ``test_`` is prepended. For example, ``test_cero.py`` contains tests for the code contained in ``cero.py``. To run a test, first change to the directory above the project directory - i.e. such that ``concero`` is a folder within this directory. Then execute:

    ``python3 -m concero.tests.<test_name>``

There is two aspects to this command to note. First, the ``-m`` option, second, that ``<test_name>`` does **not** have the ``.py`` suffix. For example, to run the tests on the ``cero.py`` module, the command would be:

    ``python3 -m concero.tests.test_cero``

To run all the tests, run the command:

    ``python3 -m concero.tests.test_concero``

