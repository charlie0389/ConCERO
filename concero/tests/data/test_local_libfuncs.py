"""
Created on Apr 24 11:08:00 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

from concero.libfuncs_wrappers import recursive_op, series_op, dataframe_op

@recursive_op
def test_local_recursive_op(x):
    return 2*x