#      ConCERO - a program to automate data format conversion and the execution of economic modelling software.
#      Copyright (C) 2018  CSIRO Energy Business Unit
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Below is a complete listing of python functions accessible to models as commands. That is, commands of ``type: python_method`` must have a ``func`` defined in this file, in addition to ``args`` and ``kwargs`` corresponding to the ``func``.

For example, a valid command object is:

    .. code-block:: python

        cmds: replace_file_in_zip
        type: python_method
        args:
            - a_new_file.txt
            - zip_archive.zip
            - the_old_file.txt
        kwargs:
            tmp_dir: tmp_dir



Specifications
--------------

.. currentmodule:: modfuncs

.. autofunction:: replace_file_in_zip

Created on Feb 27 09:10:22 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import os
import shutil
import zipfile

import concero.conf as conf

log = conf.setup_logger(__name__)

def replace_file_in_zip(new_file: str,
                        *old_file: str,
                        tmp_dir: str="tmp_zipfile") -> str:
    """
    Replaces a file in a zip archive with a ``new_file``.

    :param str new_file: The file to add to the archive.
    :param "List[str]" old_file: Arguments, in order, that identify the old file. For example, if the file to be replaced is ``a_file.txt`` in the folder ``a_folder`` in the zip archive ``a_zip.zip``, then the function signature is ``replace_file_in_zip("new_file.txt", "a_zip.zip", "a_folder", "a_file.txt")``.
    :param str tmp_dir: The directory in which the contents of the zip file are temporarily extracted to.
    :return str: The new zip file.
    """

    new_file = os.path.abspath(new_file)
    if not os.path.isfile(new_file):
        # Must have reached file for replace
        msg = "%s is not a valid 'new_file' in 'replace_file_in_zip'." % new_file
        log.error(msg)
        raise ValueError(msg)

    tmp_dir = os.path.relpath(os.path.join(tmp_dir, ""))
    if tmp_dir[-1] != os.sep:
        tmp_dir += os.sep

    base = old_file[0]
    base = os.path.relpath(base)
    old_file = old_file[1:]

    if os.path.isdir(base):
        prev_dir = os.getcwd()
        if base[-1] != os.sep:
            base += os.sep
        os.chdir(base)
        new_file = replace_file_in_zip(new_file, *old_file, tmp_dir=("tmp_%s/" % old_file[0]))
        os.chdir(prev_dir)
        return base

    elif os.path.isfile(base):

        if base[-3:].lower() == "zip":

            zfobj = zipfile.ZipFile(base, 'r')
            log.info("Extracting zip temporarily to directory %s ...", tmp_dir)
            compress_type = zfobj.compression
            zfobj.extractall(path=tmp_dir)
            zfobj.close()

            zip_dir = replace_file_in_zip(new_file, tmp_dir, *old_file)

            log.info("Creating archive '%s' from files %s." % (base, os.listdir(zip_dir)))
            zfobj = zipfile.ZipFile(base, 'w')
            for file in os.listdir(zip_dir):
                zfobj.write(zip_dir + file, arcname=file, compress_type=compress_type)
            zfobj.close()

            # Remove temporary extraction directory
            shutil.rmtree(zip_dir)

            return base

        else:
            shutil.move(new_file, base)
            return base
    else:
        msg = "'%s' is unrecognised." % base
        log.error(msg)
        raise ValueError(msg)