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

import os
import logging

project_dir = os.path.dirname(__file__)
d_t = os.path.join(project_dir, "tests", "") # Test directory with trailing /
d_td = os.path.join(d_t, "data", "") # test data directory with trailing /
_search_paths = [project_dir, d_t, d_td]

_logd = None

def set_logd(_dir):
    global _logd
    _logd = os.path.join(_dir, "ConCERO_logs")

    if not os.path.isdir(_logd):
        os.mkdir(_logd)

set_logd(os.getcwd())

def get_log_level():
    root_logger = logging.getLogger()
    return root_logger.getLevel()

def set_log_level(level="WARNING"):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

def setup_logger(name):
    log = logging.getLogger(name)
    if not log.handlers:
        log.addHandler(logging.FileHandler(filename=os.path.join(_logd, name + ".log")))
    return log

def add_search_path(path):
    global _search_paths
    _search_paths.append(os.path.normpath(path))

def rm_search_path():
    global _search_paths
    _search_paths.pop()

def find_file(filename):
    filename = os.path.normpath(filename)
    for sp in _search_paths:
        if os.path.isfile(os.path.join(sp, filename)):
            return os.path.join(sp, filename)
    else:
        raise FileNotFoundError("File '%s' not found in any of the locations: %s." % (filename, _search_paths))

try:
    __import__("gdxpds")
    gdxpds_installed = True
except ImportError:
    gdxpds_installed = False

try:
    __import__("harpy")
    harpy_installed = True
except ImportError:
    harpy_installed = False
