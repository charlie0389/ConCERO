#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version_file:
    version = version_file.read().strip()

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
doc_files.append('../concero/doc/Makefile')
doc_files.append('../VERSION')

setup(name='concero',
    version=version,
    description='Automates the running of models and data format conversion for csv, xlsx, vd and har files.',
    author='Lyle Collins',
    author_email='Lyle.Collins@csiro.au',
    url=r'https://github.com/charlie0389/ConCERO',
    packages=find_packages(),
    python_requires=">=3.4",
    setup_requires=["numpy", "pandas>=0.22"], # Pandas >=0.22 necessary for bug: https://github.com/numpy/numpy/issues/2434
    install_requires=["pandas>=0.22", "numpy", "pyyaml", "seaborn>=0.8.1", "xlrd>=1.1.0"],
    tests_require=["harpy", "gdxpds"],
    test_suite="concero.tests.test_concero.TestConCERO.__init__",
    package_data={'concero': doc_files},
    entry_points={'console_scripts': ['concero = concero.__main__:launch']},
)
