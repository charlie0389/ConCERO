"""
Created on May 29 14:57:38 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import shutil
import sys
import os

from concero.format_convert_tools import read_yaml

copy_dict = read_yaml(sys.argv[1])

for k, v in copy_dict.items():

    k = os.path.abspath(k)

    if isinstance(type(v), str):
        v = [v]

    for p in v:
        p = os.path.abspath(p)
        try:
            shutil.copy(k, p)
        except FileNotFoundError:
            os.mkdir(os.path.dirname(p))
            shutil.copy(k, p)
