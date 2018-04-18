"""
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
                        tmp_dir="tmp_zipfile/") -> str:
    """
    Replaces a file in a zip archive with a ``new_file``.
    :param new_file:
    :param old_file:
    :param tmp_dir:
    :return:
    """

    new_file = os.path.abspath(new_file)
    if not os.path.isfile(new_file):
        # Must have reached file for replace
        msg = "%s is not a valid 'new_file' in 'replace_file_in_zip'." % new_file
        log.error(msg)
        raise ValueError(msg)

    tmp_dir = os.path.relpath(tmp_dir)
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
        print(base in os.listdir())
        print(os.path.isfile(base))
        print(os.path.isdir(base))
        msg = "'%s' is unrecognised." % base
        log.error(msg)
        raise ValueError(msg)