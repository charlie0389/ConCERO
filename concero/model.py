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
Created on Feb 05 12:28:55 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import subprocess
import contextlib

import concero.conf as conf
import concero.modfuncs as modfuncs
from concero.from_cero import FromCERO
from concero.to_cero import ToCERO
from concero.cero import CERO

@contextlib.contextmanager
def _modified_environ(*remove, wd=None, **update):
    """
    Temporarily updates the ``os.environ`` dictionary in-place.

    The ``os.environ`` dictionary is updated in-place so that the modification
    is sure to work in all situations.

    :param remove: Environment variables to remove.
    :param wd: Directory to change to (before any changes to environment variables are made). By default, current working directory.
    :param update: Dictionary of environment variables and values to add/update.

    Code for this function from: ``https://stackoverflow.com/questions/2059482/python-temporarily-modify-the-current-processs-environment``
    """
    for k, v in update.items():
        if not isinstance(v, str):
            update[k] = "%s" % v

    env = os.environ
    update = update or {}
    remove = remove or []

    # List of environment variables being updated or removed.
    stomped = (set(update.keys()) | set(remove)) & set(env.keys())
    # Environment variables and values to restore on exit.
    update_after = {k: env[k] for k in stomped}
    # Environment variables and values to remove on exit.
    remove_after = frozenset(k for k in update if k not in env)

    old_dir = os.getcwd()

    if wd:
        try:
            os.chdir(wd)
        except FileNotFoundError:
            # Attempt to create directory if it doesn't exist
            os.mkdir(wd)
            os.chdir(wd)

    try:
        env.update(update)
        [env.pop(k, None) for k in remove]
        yield
    finally:
        env.update(update_after)
        [env.pop(k) for k in remove_after]
        os.chdir(old_dir)


class Model(dict):

    _logger = conf.setup_logger(__name__)

    def __init__(self, model: dict, *args, parent: "Model"=None, **kwargs):
        """

        :param model: A `dict` containing ``Model`` options.
        :param args: Passed to superclass (`dict`) at initialisation.
        :param "Model" parent: If provided, inherits all key-value pairs from ``parent``.
        :param kwargs: Passed to superclass (`dict`) at initialisation.
        """

        defaults = {"name": "default_model_name",
                    "cmds": [],
                    "input_conf": [],
                    "output_conf": [],
                    "search_paths": [],
                    "wd": None}
        defaults.update(model)

        if parent is None:
            parent = {}

        defaults.update(parent)

        super().__init__(defaults, *args, **kwargs)

        if self["name"] == "default_model_name":
            Model._logger.warning("Model not named - default name '%s' assigned." % self["name"])

        # Command string processing
        if isinstance(self["cmds"], str):
            self["cmds"] = [self["cmds"]]

        if not self["cmds"]:
            Model._logger.info("No commands specified for model '%s'." % defaults["name"])

        if not self["search_paths"]:
            self["search_paths"].append(os.path.abspath("."))

        if isinstance(self["input_conf"], str):
            self["input_conf"] = [self["input_conf"]]
        if isinstance(self["output_conf"], str):
            self["output_conf"] = [self["output_conf"]]

        # Locate and load configuration files...
        for idx, input_conf in enumerate(self["input_conf"]):
            self["input_conf"][idx] = self.find_file(input_conf)
            par_dict = {"ref_dir": os.path.abspath(os.path.dirname(self["input_conf"][idx]))}
            self["input_conf"][idx] = FromCERO(self["input_conf"][idx], parent=par_dict)

        # Locate and load configuration files...
        for idx, output_conf in enumerate(self["output_conf"]):
            self["output_conf"][idx] = self.find_file(output_conf)
            par_dict = {"search_paths": os.path.abspath(os.path.dirname(self["output_conf"][idx]))}
            self["output_conf"][idx] = ToCERO(self["output_conf"][idx], parent=par_dict)

    def is_valid(self, raise_exception=True):
        """
        Checks the validity of ``self`` as a ``Model`` object. Method does not ensure runtime issues will not occur.
        :param bool raise_exception:
        :return bool: Returns `True` if ``self`` is a valid ``Model``.
        """
        req_keys = ["name", "cmds", "input_conf", "output_conf"]

        if not all([k in self for k in req_keys]):

            msg = ("All models must have all of the keys: %s. Attempted to create model" +
                            " with at least one of these keys missing.") % req_keys

            Model._logger.error(msg)
            if raise_exception:
                raise TypeError(msg)
            print(msg)
            return False

        for ic in self["input_conf"]:
            if not FromCERO.check_config(ic, raise_exception=raise_exception, runtime=False):
                return False

        for oc in self["output_conf"]:
            if not ToCERO.check_config(oc, raise_exception=raise_exception, runtime=False):
                return False

        return True

    def run_checks(self, raise_exception=True):
        """
        Performs runtime checks on ``self`` to ensure it is a valid Model object. Failure of runtime checks indicates that the model is not ready to run.

        :param bool raise_exception: If True, an exception is raised on check failure (as opposed to returning `False`).
        :return bool:
        """

        for ic in self["input_conf"]:
            if not FromCERO.check_config(ic, raise_exception=raise_exception, runtime=True):
                return False

        return True

    def check_config(self, raise_exception=False, runtime=False):
        if runtime:
            return self.run_checks(raise_exception=raise_exception)
        return self.is_valid(raise_exception=raise_exception)

    def run(self, cero) -> 'CERO':
        """
        Executes all data import/export operations (defined by ``input_conf`` and ``output_conf`` respectively) and the execution of any commands.

        :param pandas.DataFrame cero: A CERO that contains all necessary data for conversion to input files (for \
        model execution).
        :return pandas.DataFrame: A CERO of relevant output data ('relevant' is defined by ``output_conf``).
        """

        for input_conf in self["input_conf"]:
            input_conf.exec_procedures(cero)

        print("Completed converting CERO to model input files (%s). Now processing commands..." % self["name"])

        with _modified_environ(wd=self["wd"], **self.get("env_vars", {})):

            for cmdobj in self["cmds"]:

                cmd = {"type": "shell", "shell": True} # Default command

                if isinstance(cmdobj, str):
                    # cmd is interpreted as shell command by default
                    # cmdobj = cmdobj.split(" ")
                    cmd.update({"args": cmdobj})
                elif isinstance(cmdobj, dict):
                    cmd.update(cmdobj) # Add user updates
                    if "args" not in cmd:
                        raise ValueError("'args' must be provided for command of type 'dict'.")
                else:
                    raise TypeError("Invalid command object in configuration file.")

                # Change to command-specific directory
                cmd_run_dir = cmd.pop("wd", self["wd"])
                if cmd_run_dir:
                    cmd_run_dir = os.path.abspath(cmd_run_dir)

                cmd_type = cmd.pop("type")

                # Execute commands
                msg = "In directory '%s', executing command '%s'." % (cmd_run_dir, cmd)
                Model._logger.info(msg)
                with _modified_environ(wd=cmd_run_dir, **cmd.pop("env_vars", {})):

                    # Depending on cmd_type, execute command in different ways...
                    if cmd_type in ["shell"]:
                        args = cmd.pop("args")
                        Model._logger.info("Executing shell command: %s, with keyword args: %s." % (args, cmd))
                        try:
                            cmd["output"] = subprocess.check_output(args=args,
                                                                    stderr=subprocess.STDOUT,
                                                                    universal_newlines=True,
                                                                    **cmd)
                        except subprocess.CalledProcessError as e:
                            msg = ("Command '%s' failed with returncode: %s, and message:\n" +
                                   "%s\n" + "Program logs may have more information.") % (args, e.returncode, e.output)
                            Model._logger.error(msg)
                            print(msg)
                            raise e
                        Model._logger.info(cmd["output"])
                        print("Command returned: \n%s" % cmd["output"], end="")
                    elif cmd_type in ["python_method"]:
                        try:
                            assert("func" in cmd)
                        except AssertionError:
                            raise ValueError("'func' must be defined for commands of type 'python_method'.")
                        func = getattr(modfuncs, cmd.pop("func"))
                        cmd["output"] = func(*cmd["args"], **cmd["kwargs"])
                    else:
                        raise ValueError("Unsupported command type specified.")

        if not self["output_conf"]:
            return CERO.create_empty()

        ceros = []
        for oc in self["output_conf"]:
            ceros.append(oc.create_cero())

        try:
            cero = CERO.combine_ceros(ceros, overwrite=False)
        except CERO.CEROIndexConflict:
            raise RuntimeWarning("Attempts to duplicate the export of data - i.e. one or more data series are being " +
                                 "exported more than once (which should be avoided). The last procedure will define " +
                                 "the intended data.")
            cero = CERO.combine_ceros(ceros)

        return cero

    def find_file(self, filename):
        orig_filename = filename
        filename = os.path.relpath(filename)
        for sp in self["search_paths"]:
            Model._logger.debug("Model.find_file(): testing path: %s" % os.path.join(sp, filename))
            if os.path.isfile(os.path.join(sp, filename)):
                return os.path.join(sp, filename)
            else:
                raise FileNotFoundError("File '%s' not found." % orig_filename)
