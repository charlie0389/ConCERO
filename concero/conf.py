#------DON'T EDIT BELOW THIS STATEMENT UNLESS YOU KNOW WHAT YOU'RE DOING
import os
import logging

project_dir = os.path.dirname(__file__)
d_t = os.path.join(project_dir, "tests", "") # Test directory with trailing /
d_td = os.path.join(d_t, "data", "") # test data directory with trailing /
_search_paths = [project_dir, d_t, d_td]
# _search_paths = []

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
    orig_filename = filename
    filename = os.path.normpath(filename)
    if os.path.isfile(filename):
        return filename
    else:
        filename = os.path.relpath(filename)
        for sp in _search_paths:
            if os.path.isfile(os.path.join(sp, filename)):
                return os.path.join(sp, filename)
        else:
            raise FileNotFoundError("File '%s' not found in any of the locations: %s." % (orig_filename, _search_paths))

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
