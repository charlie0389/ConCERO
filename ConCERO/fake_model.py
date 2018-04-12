"""
Created on Feb 05 16:07:52 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import sys
import shutil

if __name__ == "__main__":
    shutil.copyfile("vurm_input.har", "Mdatnew7.har")
    print("Fake model successfully run!")
    sys.exit(0)