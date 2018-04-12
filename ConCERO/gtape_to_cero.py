#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class requires access to the GAMS API bindings. Install instructions can be \
found at `<https://www.gams.com/latest/docs/API_PY_TUTORIAL.html>`_.

Requires the use of third party software from NREL. The project page can be found at \
`<https://github.com/NREL/gdx-pandas>`_.

``pip install git+https://github.com/NREL/gdx-pandas.git@master``

If the previous install instruction does not work, consult the project page.

.. autoclass:: GTAPE2CERO

Created on Fri Jan 19 9:59:27 2018

@author: Lyle Collins
@email: Lyle.Collins@csiro.au
"""
from ConCERO.to_cero import ToCERO

class GTAPE2CERO(ToCERO):

    def __init__(self, conf_file: str, *args, **kwargs):

        """Executes the conversion of a VURM output file to a CERO. The configuration file specified by \
        ``conf_file`` contains virtually all the options.

        :param \*args: Passed to the ``object`` superclass at initialisation.
        :param (str) conf_file: The relative path to the configuration file.
        :param kwargs: Is passed to the ``pandas`` function invoked to read any input files. By default, \
        the ``header=None`` and ``index_col=0`` options are provided.
        :ivar cero: The resultant CERO (a ``pandas.DataFrame`` object).
        """

        super().__init__(conf_file, *args, **kwargs)
