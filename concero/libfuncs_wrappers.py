"""
Classes of User-Specified Functions for operating on CEROs
==========================================================

The set of functions that *could* be applied to the CERO, and data series within the CERO, is infinitely large, \
so it is obviously impossible to provide all these functions. It is therefore necessary that the user provide \
functions as they are needed, by writing the appropriate python 3 code and including this function in ``libfuncs.py``. \
To minimise the difficulty and complexity of achieving this, ConCERO includes 3 classes of *wrapper functions*, that \
significantly reduce the difficulty for the user in extending the power of ``FromCERO``.

A *wrapper function* is a function that encapsulates another function, and therefore has access to both the inputs \
and outputs of the encapsulated function. Because the wrapper function has access to the inputs, it can provide \
pre-processing on the input to reshape it into a specific form, and because it has access to the output of the \
function, it can post-process the output of the function - mutating it into a desirable form.

A wrapper function can be directed to encapsulate a function by preceding the function with a *decorator*. A \
*decorator* is a simple one line statement that starts with the '\@' symbol and then the name of the wrapper \
function. For example, to encapsulate ``func`` with the ``dataframe_op`` wrapper, the code is:

.. code-block:: python

    @dataframe_op
    def func(*args, **kwargs):
        ...
        return None


The wrapper functions themselves are stored in  the ``libfuncs_wrappers`` module, but the wrappers themselves should \
*never* be altered by the user.

What the 3 classes of wrappers are, and how to apply the function wrappers, are explained below, in addition to the \
case where no wrapper/decorator is provided.

Class 1 Functions - DataFrame Operations
----------------------------------------

Class 1 functions are the most general type of wrapper functions, and can be considered a superset of the other two. \
Class 1 functions operate on a ``pandas.DataFrame`` object, and therefore can operate on an entire CERO if need be. \
A class 1 function must have the following function signature:

.. code-block:: python

    @dataframe_op
    def func_name(df, *args, **kwargs):
        ...
        return None

Note the following key features:

    * The function is proceeded by the @dataframe_op 'decorator' (imported from ``libfuncs_wrappers``).
    * The first argument provided to ``func_name`` - ``df`` - will be a CERO (an instance of a pandas.DataFrame), \
    reduced by the ``arrays``/``inputs`` options.
    * No parameters are to be returned (technically, the last line could be omitted).

**What is not clear from the function definition above** is the **requirement** that all operations on \
``df`` must occur inplace. In other words, all mutations/operations not applied to ``df`` will be ignored. \
Note that if this constraint is violated, no exceptions/errors will be raised as it is impossible to detect this \
'failure to understand intention'. As a rule of thumb, this can nearly always be achieved by restricting \
operations to the types:

    * ``df.loc[...] = ...``,
    * ``df.iloc[...] = ...``, or
    * ``df.func(*args, inplace=True, **kwargs)``.

It is highly recommended to consult ``pandas`` documentation \
(e.g. `<https://pandas.pydata.org/pandas-docs/stable/indexing.html#returning-a-view-versus-a-copy>`_) and \
``StackOverflow`` to develop a better understanding of what ``inplace`` operations are.

The ``libfuncs`` function ``merge`` provides a simple example of how to apply this wrapper:

.. code-block:: python

    @dataframe_op
    def merge(df, *args, **kwargs):
        df.iloc[0, :] = df.sum(axis=0) # Replaces the first series with the sum of all the series
        return

Class 2 Functions - Series Operations
-------------------------------------

Class 2 functions operate on a single ``pandas.Series`` object - note that a single row of a ``pandas.DataFrame`` is \
an instance of a ``pandas.Series``. The series operations class can be considered a subset of DataFrame operations, \
and a superset of all recursive operations (discussed below).

Similar to class 1 functions, class 2 functions must fit the form:

.. code-block:: python

    @series_op
    def func(series, *args, **kwargs):
        ...
        return pandas_series

With similar features:

    * The function is proceeded by the @series_op wrapper (imported from ``libfuncs_wrappers``).
    * The first argument (``series``) must be of pandas.Series type.

However, *dissimilar to class 1 functions*, class 2 functions must:

    * Return an object of ``pandas.Series`` type (``pandas_series``). ``pandas_series`` must be of the \
    same ``shape`` as ``series``.

Class 3 Functions - Recursive Operations
----------------------------------------

Recursive operations must fit the form:

.. code-block:: python

    @recursive_op
    def func(*args, **kwargs):
        ...
        return calc

Noting that:

    * Positional arguments are provided in the same order as their sequence in the data series.
    * The return value ``calc`` must be a single floating-point value.

Note that options can be provided to an operation object to alter the behaviour of the recursive operation. Those \
options are:

    * ``init: list(float)`` - values that precede the data series that serve as initialisation values.
    * ``post: list(float)`` - values that follow the data series for non-causal recursive functions.
    * ``inplace: bool`` - If ``True``, then the recursive operation will be applied on the array \
        inplace, such that the result from a previous iteration is used in subsequent \
        iterations. If ``False``, the operation proceeds ignorant of the results of \
        previous iterations. ``True`` by default.

How these items are to be applied is probably best explained with an example - consider the recursive operation is \
a 3 sample moving point averaging filter. This can be implemented by including ``mv_avg_3()`` (below) in \
``libfuncs.py``:

.. code-block:: python

    @recursive_op
    def mv_avg_3(a, b, c):
        return (a + b + c)/3

It is also necessary to provide the arguments, ``init`` and ``post`` in the configuration file, so the operation \
object looks somthing like:

.. code-block:: yaml

    func: mv_avg_3
    init:
        - 1
    post:
        - 2

This operation would transform the data series ``[2, 1, 3]`` to the values \
``[1.3333, 1.7777, 2.2593]`` - i.e. ``[(1+2+1)/3, (1.333+1+3)/3, (1.7777+3+2)/3]``. If, instead, the configuration \
file looks like:

.. code-block:: yaml

    func: mv_avg_3
    init:
        - 1
    post:
        - 2
    inplace: False

Then the output of the same series would be ``[1.3333, 2, 2]`` - that is, ``[(1+2+1)/3, (2+1+3)/3, (1+3+2)/3]``.

Wrapper-less Functions
----------------------

A function that is defined in ``libfuncs`` can be accessed by ``FromCERO``, though there are some constraints \
necessary to enable ``FromCERO`` to act in a programmatic way. A function (in ``libfuncs.py``) *that is called upon \
by* ``FromCERO`` must have the following function signature:

.. code-block:: python

    def plotdf(df, *args, locs=None, **kwargs):
        ...
        return None

Where ``df`` is the entire CERO provided to the calling class (so is therefore of ``pandas.DataFrame`` type), and \
``locs``, if provided, is a list of all identifiers specifying which series of the CERO have been specified.

**Note that any changes made to** ``df`` **will be applied in the calling class (i.e. the** ``FromCERO`` **class).**

Use of wrapper-less functions for use with ``FromCERO`` is **not recommended**, though if it is none-the-less \
desirable, ``libfuncs.plotdf()`` serves as an example.

Other Notes
-----------

    * Avoid trying to create a renaming function - use ``libfuncs._rename`` - it has been designed to work \
    around a bug in Pandas (Issue #19497).
    * ``libfuncs`` also serves as a source of examples for how to use the function wrappers.

Technical Specifications of Decorators
--------------------------------------

.. autofunction:: dataframe_op
.. autofunction:: series_op
.. autofunction:: recursive_op
.. autofunction:: log_func

Created on Thu Dec 21 16:36:02 2017

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
import functools

import pandas as pd

import concero.conf as conf
from concero._identifier import _Identifier
from concero.cero import CERO

log = conf.setup_logger(__name__)

def log_func(func):
    """Logging decorator - for debugging purposes. To apply to function ``func``:

    .. code-block:: python

        @log_func
        def func(*args, **kwargs):
            ...

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log.debug("Function call: %s(%s, %s)" % (func.__name__, args, kwargs))
        result = func(*args, **kwargs)
        log.debug("Returned: %s" % (result,))
        return result
    return wrapper

def dataframe_op(func):
    """
    This decorator is designed to provide ``func`` (the encapsulated function) with a restricted form \
    of ``df`` (a CERO). A \
    *restricted* ``df`` is the original ``df`` limited to a subset of rows and/or columns. All of the key-word \
    arguments, with the exception of ``rename``, define the restriction. Note that a restriction on ``df.columns`` \
    will be *compact*, but this is not necessarily the case for restriction on ``df.index``.
    """

    @functools.wraps(func)
    def wrapper(df: pd.DataFrame,
                *args,
                locs: "List[Union[tuple, str]]" = None,
                ilocs: "List[int]" = None,
                start_year: "Union[pd.datetime, int]" = None,
                end_year: "Union[pd.datetime, int]" = None,
                # rename: "Union[str, dict, List[str]]" = None,
                # sets: dict = None,
                **kwargs):

        """
        :param df: An CERO, which may or may not be a strict superset of data to perform the operation on.
        :param args: Passed to the encapsulated function as positional arguments, immediately after the restricted \
        ``df``.
        :param locs: ``locs``, if provided, must be a list of identifiers that correspond to values of ``df.index``. \
        It is ``df``, reduced to these specific indices, that a wrapped function will receive as an argument. An \
        error is raised if both ``locs`` and ``ilocs`` is specified.
        :param ilocs: Identical in nature to ``locs``, though instead a list of integers (zero-indexed) is \
        provided (corresponding to the row number of ``df``). An \
        error is raised if both ``locs`` and ``ilocs`` is specified.
        :param start_year: Note that ``df`` is a CERO, and CEROs have a ``pandas.DatetimeIndex`` on columns. \
        ``start_year`` restricts the CERO to years after *and including* ``start_year``.
        :param end_year: Note that ``df`` is a CERO, and CEROs have a ``pandas.DatetimeIndex`` on columns. \
        ``end_year`` restricts the CERO to years before, *but excluding* ``end_year``.
        :param rename: The first data series of ``df`` ('first' is defined by ``locs`` or ``ilocs``) can be \
        renamed by providing this argument. ``rename`` alters the original ``df``, after the encapsulated \
        function has been executed.
        :param kwargs: Keyword arguments to be passed to the encapsulated function.
        :return: The return value of the encapsulated function.
        """

        try:
            assert(isinstance(df, pd.DataFrame))
        except AssertionError:
            raise TypeError("First function argument must be of pandas.DataFrame type.")

        # Convert integer to datetime type
        if isinstance(start_year, int):
            start_year = pd.datetime(start_year, 1, 1)
        if isinstance(end_year, int):
            end_year = pd.datetime(end_year, 1, 1)

        # Get index locations
        if start_year is not None:
            start_year = df.columns.get_loc(start_year)
        if end_year is not None:
            end_year= df.columns.get_loc(end_year)

        if (locs is not None) and (ilocs is not None):
            raise TypeError("Only one of 'locs' or 'ilocs' can be provided (not both).")

        if locs is not None:
            ilocs = [df.index.get_loc(loc) for loc in locs]
        if ilocs is None:
            ilocs = pd.IndexSlice[0:]

        df_cp = df.iloc[ilocs, start_year:end_year].copy(deep=False) # df_cp is always different object to df

        ret = func(df_cp, *args, **kwargs)
        if ret is None:
            return ret
        else:
            CERO.is_cero(ret) # Performs checks to ensure ret is a valid CERO

        try:
            # TODO: If series, convert to dataframe
            assert issubclass(type(ret), pd.DataFrame)
        except AssertionError:
            raise TypeError("'dataframe_op'(s) must return a pandas.DataFrame.")

        return ret

    return wrapper


def _rename(df,
            old_names: "Union[List[Union[tuple, str]], tuple, str]",
            new_names: "Union[List[Union[tuple, str]], tuple, str]", *args, **kwargs):
    """If list provided for ``old_names`` and ``new_names``, must be of equal length. This method is an \
    obtuse way to do this in comparison to `rename` method, but pandas has a bug that this method is designed to \
    work around... (GitHub pandas issue #19497)"""
    if isinstance(old_names,(str, tuple)):
        old_names = [old_names]
        new_names = [new_names]

    old_index_name = df.index.name
    labels = df.index.tolist()

    for old_name, new_name in zip(old_names, new_names):
        labels[df.index.get_loc(old_name)] = _Identifier.tupleize_name(new_name)
        # The line below *should* work when the bug is fixed (obviously untested)
        # df.rename({old_name: new_name}, axis="index", inplace=True)

    df.index = pd.Index(labels, tupleize_cols=False, name=old_index_name)

    return df


def series_op(func):
    """This decorator provides ``func`` (the encapsulated function) with the first ``pandas.Series`` \
    in a ``pandas.DataFrame`` (i.e. the first row in ``df``). Note that this wrapper is encapsulated within \
    the ``dataframe_op`` wrapper."""

    @dataframe_op
    @functools.wraps(func)
    def wrapper(df: pd.DataFrame, *args, **kwargs):
        """
        :param df: A dataframe with a single row. ``df`` must be of CERO type.
        :param args: Passed to the encapsulated function as positional arguments immediately after the \
        ``pandas.Series`` object.
        :param kwargs: Passed to the encapsulated function as keyword arguments.
        :return: Returns ``df`` with the first data series updated with the result of the encapsulated function.
        """

        for idx, ser in df.iterrows():

            # Note that pandas slicing is inclusive (in contrast to standard python list slicing)...
            valid_ser = ser[ser.first_valid_index(): ser.last_valid_index()]

            result = func(valid_ser, *args, **kwargs)
            try:
                assert (isinstance(result, pd.Series))
            except AssertionError:
                raise TypeError("A \'series_op\' must return pandas.Series object.")

            df.loc[idx, ser.first_valid_index(): ser.last_valid_index()] = result

        return df
        # return None
    return wrapper


def recursive_op(func):
    """Applies the encapsulated function (``func``) iteratively to the elements of \
        ``array`` from left to right, with ``init`` prepended to ``array`` \
        and ``post`` postpended."""

    @series_op
    @functools.wraps(func)
    def wrapper(array: pd.Series, *args,
                init: list = None,
                post: list = None,
                inplace: bool = True,
                auto_init: int = None,
                auto_post: int = None,
                init_cols: list = None,
                post_cols: list = None,
                **kwargs) -> pd.Series:
        '''
        :param pandas.Series array: A ``pandas`` series for which the encapsulated recursive function will be applied to.
        :param list init: ``init`` is pre-pended to ``array`` before the recursive operation is applied.
        :param list post: ``post`` is post-pended to ``array`` before the recursive operation is applied.
        :arg (bool) inplace: If ``True``, the operation will be applied on the array \
        inplace, such that the result from a previous iteration is used in subsequent \
        iterations. If ``False``, the operation proceeds ignorant of the results of \
        previous iterations. ``True`` by default.
        :returns (pandas.Series): Returns the result of the recursively-\
        applied function. Will copy ``name`` and ``index`` \
        properties of the provided ``pandas.Series`` object to the returned object.'''

        if [bool(init), bool(auto_init), bool(init_cols)].count(True) >= 2:
            raise ValueError("Only one of the keyword arguments 'init', 'auto_init' and 'init_cols' must be provided.")
        if [bool(post), bool(auto_post), bool(post_cols)].count(True) >= 2:
            raise ValueError("Only one of the keyword arguments 'post', 'auto_post' and 'post_cols' must be provided.")

        if not init: init = []
        if not post: post = []

        if not auto_init: auto_init = 0
        if not auto_post: auto_post = 0

        if not init_cols: init_cols = []
        if not post_cols: post_cols = []

        if not isinstance(auto_init, int) or auto_init < 0:
            raise TypeError("'auto_init' keyword argument must be provided as an integer greater than 0.")
        if not isinstance(auto_post, int) or auto_post < 0:
            raise TypeError("'auto_post' keyword argument must be provided as an integer greater than 0.")

        if auto_init: init = [array[0]]*auto_init
        if auto_post: post = [array[-1]]*auto_post

        dis_start = len(init)
        dis_end = len(post)
        sl_start = None
        sl_end = None

        if init_cols:
            if isinstance(init_cols, int): init_cols = [dt.year for dt in array.index.tolist()[:init_cols]]
            init = array.loc[pd.to_datetime(init_cols, format="%Y")].tolist()
            sl_start = len(init)
        if post_cols:
            if isinstance(post_cols, int): post_cols = [dt.year for dt in array.index.tolist()[-post_cols:]]
            post = array.loc[pd.to_datetime(post_cols, format="%Y")].tolist()
            sl_end = -len(post)
        sl = slice(sl_start, sl_end)

        array_list = init + array.values.tolist()[sl] + post

        no_args = len(init) + len(post) + 1
        no_ops = len(array_list) - no_args + 1

        new_array = init + [None]*no_ops + post

        for i in range(no_ops):
            rec_args = array_list[i: i + no_args] + list(args)
            try:
                tmp = func(*rec_args, **kwargs)
                # tmp = func(*array_list[i - dis_start:i + dis_end + 1], # This form can only be used for Python 3.5 onwards...
                #            *args,
                #            **kwargs)
            except TypeError as e:
                msg = e.__str__() + ". A likely cause is that initial conditions (or columns) have not been specified."
                log.error(msg)
                raise TypeError(msg)
            if tmp is None:
                raise ValueError("'recursive_op' functions must return a floating point value.")

            if inplace: array_list[i + len(init)] = tmp
            else:        new_array[i + len(init)] = tmp

        if inplace: new_array = array_list

        new_array = new_array[dis_start: len(new_array) - dis_end]

        # Copy names and index to new series
        new_array = pd.Series(data=new_array, index=array.index, name=array.name)

        return new_array

    return wrapper
