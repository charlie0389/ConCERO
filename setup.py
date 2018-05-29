#!/usr/bin/env python
import os
from setuptools import setup, find_packages

def package_files(directory, append_to=None):
    directory = os.path.normpath(directory)
    if append_to is None:
        paths = []
    else:
        paths = append_to
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

test_files = package_files('concero/tests/data')
doc_files = package_files('concero/doc/build/html', append_to=test_files)
doc_files = package_files('concero/doc/source', append_to=doc_files)
doc_files = package_files('concero/aux', append_to=doc_files)
doc_files.append('doc/Makefile')

setup(name='concero',
    version='0.1',
    description='Automates the running of models and data conversion for the ANO2 project.',
    author='Lyle Collins',
    author_email='Lyle.Collins@csiro.au',
    url=r'https://svnserv.csiro.au/svn/OSM_CBR_LW_NATOUTLOOK2_work/ISAM/trunk/iam/integration/',
    packages=find_packages(),
    python_requires=">=3.4",
    setup_requires=["numpy", "pandas"], # Necessary for bug: https://github.com/numpy/numpy/issues/2434
    install_requires=["scipy", "pandas>=0.22", "numpy", "pyyaml", "seaborn>=0.8.1", "xlrd>=1.1.0", "openpyxl", "pytz",
                      "python-dateutil", "six"],
    tests_require=["harpy", "gdxpds"],
    test_suite="concero.tests.test_concero.TestConCERO.__init__",
    package_data={'concero': doc_files},
    entry_points={'console_scripts': ['concero = concero.__main__:launch']},
)
