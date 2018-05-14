"""
Created on Feb 05 16:07:52 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import sys
import shutil

import concero.conf

if __name__ == "__main__":
    shutil.copyfile("test_model_input.har", "test_model_output.har")
    print("Fake model successfully run!")
    sys.exit(0)