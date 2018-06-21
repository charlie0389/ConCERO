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
Created on Feb 05 09:44:50 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""
import os

import datetime as dt

import concero.conf as conf
from concero.format_convert_tools import read_yaml
from concero.model import Model
from concero.to_cero import ToCERO
from concero.from_cero import FromCERO
from concero.cero import CERO

class Scenario(dict):

    _logger = conf.setup_logger(__name__)

    def __init__(self, sc_def: dict, *args, parent: dict=None, **kwargs):
        """
        :param sc_def: A scenario definition object.
        :param args: Passed to the superclass (dict) as positional arguments at initialisation.
        :param kwargs: Passed to the superclass (dict) as keyword arguments at initialisation.
        """

        defaults = {"name": None,
                    "run_no": None,
                    "search_paths": [],
                    "ref_dir": None,
                    "models": [],
                    "input_conf": [],
                    "output_conf": []}

        if parent is None:
            parent = {}

        defaults.update(parent)

        try:
            assert isinstance(sc_def, dict)
        except AssertionError:
            raise TypeError("Scenario definition provided in incorrect format - type %s instead of dict." % type(sc_def))

        defaults.update(sc_def)

        sc_def = defaults
        super().__init__(sc_def, *args, **kwargs)

        if not self.get("name"):
            self["name"] = "scenario_unnamed"
            self._logger.warn("Scenario name has not been specified - scenario named '%s'." % self["name"])

        if not issubclass(type(self.get("run_no")), int):
            self["run_no"] = 1
            self._logger.info("Scenario run_no (run number) has not been specified (or is not of integer type) - defaults to %s." % self["run_no"])

        if isinstance(self["search_paths"], str):
            self["search_paths"] = [os.path.abspath(self["search_paths"])]
        elif not self["search_paths"]:
            self["search_paths"].append(os.path.abspath("."))

        if self["ref_dir"] is None:
            self["ref_dir"] = os.path.abspath(".")

        model_parent = {"search_paths": self["search_paths"],
                        "ref_dir": self["ref_dir"]}
        self["models"] = [Model(m, parent=model_parent) for m in self.get("models")]

        if isinstance(self["input_conf"], str):
            self["input_conf"] = [self["input_conf"]]
        if isinstance(self["output_conf"], str):
            self["output_conf"] = [self["output_conf"]]

        # Load ToCERO conf
        par_dict = {"search_paths": self["search_paths"]}
        for idx, ic in enumerate(self["input_conf"]):
            self["input_conf"][idx] = self.find_file(ic)
            self["input_conf"][idx] = ToCERO(self["input_conf"][idx], parent=par_dict)

        # Load FromCERO conf
        par_dict = {"ref_dir": self["ref_dir"]}
        for idx, oc in enumerate(self["output_conf"]):
            self["output_conf"][idx] = self.find_file(oc)
            self["output_conf"][idx] = FromCERO(self["output_conf"][idx], parent=par_dict)

        self.is_valid()  # Check Scenario is valid

    def run(self) -> None:
        """
        Execute a scenario run.
        """

        self.cero = CERO.create_empty()

        ceros = [in_conf.create_cero() for in_conf in self["input_conf"]]
        if ceros:
            self.cero = CERO.combine_ceros(ceros)
            print("Successfully loaded scenario inputs as CERO.")

        FromCERO.dataframe_out(self.cero, (self.get_name() + "_%03d_step_%02d.xlsx" % (self["run_no"], 0)), "xlsx")

        for idx, model in enumerate(self["models"]):
            m_cero = model.run(self.cero)
            print("Completed run of model (%s) at %s." % (model["name"], dt.datetime.now().strftime('%Y-%m-%d %H:%M')))

            # If ouput_conf is not defined for a model, then None is returned...
            if m_cero is None:
                continue

            if not CERO.is_cero(m_cero):
                raise TypeError("Object returned from model run is *not* of CERO format.")

            if model.get("export_mod_xlsx", self.get("export_mod_xlsx", True)):
                # By default, export model outputs automatically to xlsx files
                model_out_file = (self.get_name() + "_%03d_%s.xlsx" % (self["run_no"], model["name"]))
                print("Exporting output of %s to %s." % (model["name"], model_out_file))
                m_cero.to_excel(model_out_file)

            self.cero = CERO.combine_ceros([self.cero, m_cero])

            if self.get("export_int_xlsx", True):
                # If true (default), export the intermediate steps to xlsx files
                isfn = (self.get_name() + "_%03d_step_%02d.xlsx" % (self["run_no"], idx + 1))
                print("Exporting updated CERO to %s." % (isfn))
                self.cero.to_excel(isfn)

        for out_conf in self["output_conf"]:
            out_conf.exec_procedures(self.cero)

        else:
            print("Completed generation of scenario outputs.")


    def is_valid(self, raise_exception=True) -> bool:
        """ Performs static checks on ``self`` to ensure it is a valid Scenario object."""

        req_keys = ["name", "models", "input_conf", "output_conf"]

        if not all([k in self.keys() for k in req_keys]):
            raise TypeError(("Not all required key-value pairs have been defined. " +
                            "It is necessary to define all of %s.") % req_keys)

        if not isinstance(self["models"], list):
            raise TypeError("Scenario property \'models\' must be defined as a list.")

        for model in self["models"]:
            if not issubclass(type(model), Model):
                raise TypeError("Object '%s' is of type '%s', not 'Model'." % (model, type(model)))

            if not model.check_config(raise_exception=raise_exception, runtime=False):
                return False

        for ic in self["input_conf"]:
            if not ToCERO.check_config(ic, raise_exception=raise_exception, runtime=False):
                return False

        for oc in self["output_conf"]:
            if not FromCERO.check_config(oc, raise_exception=raise_exception, runtime=False):
                return False

        return True

    def run_checks(self, raise_exception=True):
        """
        Performs runtime checks on ``self`` to ensure it is a valid Scenario object. Failure of runtime checks indicates that the scenario is not ready to run.

        :param bool raise_exception:
        :return:
        """

        for ic in self["input_conf"]:
            ToCERO.check_config(ic, raise_exception=raise_exception, runtime=True)


    def get_name(self, long_form: bool=True, raise_exception=False) -> str:
        """
        Returns the name of the ``Scenario``, which is dependent on the first linked ``ScenariosSet`` object.
        :param long_form: If ``True`` (default) return a long-form of the name. If ``False``, return a short form.
        :return: The name of the ``Scenario``.
        """
        if hasattr(self, "_linked_scenariosets"):
            return self._linked_scenariosets[0].get_scenario_name(self, long_form=long_form)
        elif self.get("name"):
            return self["name"]
        else:
            if raise_exception:
                raise TypeError("Must either link ScenariosSet, or give Scenario a 'name' before a name can be generated.")
            return ""

    def find_file(self, filename):
        orig_filename = filename
        filename = os.path.relpath(filename)
        for sp in self["search_paths"]:
            ToCERO._logger.debug("Scenario.find_file(): testing path: %s" % os.path.join(sp, filename))
            if os.path.isfile(os.path.join(sp, filename)):
                return os.path.join(sp, filename)
        else:
            msg = "File '%s' not found on any of the paths %s." % (orig_filename, self["search_paths"])
            Scenario._logger.error(msg)
            raise FileNotFoundError(msg)

    def get_linked_scenarios(self):
        """
        :return "List['ScenariosSet']": A list of linked ``ScenariosSet``.
        """
        return self.get("_linked_scenariosets")

    @staticmethod
    def load_scenarios(scen_def: str, parent=None):
        """Load one or more scenarios from a file.

        :param scen_def: The file containing one or more scenario definitions.
        :return "Union['Scenario',List['Scenario']]": Either a single ``Scenario`` , or a `list` of ``Scenario`` s.
        """

        defaults = {"search_paths": []}

        if parent is None:
            parent = {}

        defaults.update(parent)

        if isinstance(scen_def, str):
            scen_def = os.path.abspath(os.path.normpath(scen_def))
            defaults["search_paths"].append(os.path.dirname(scen_def))
            scen_def = read_yaml(scen_def)

        msg = "defaults: %s" % (defaults)
        Scenario._logger.debug(msg)

        if isinstance(scen_def, dict):
            # single scenario in file
            return [Scenario.load_scenario(scen_def, parent=defaults)]
        elif isinstance(scen_def, list):
            # List of scenarios
            return [Scenario.load_scenario(scd, parent=defaults) for scd in scen_def]

    @staticmethod
    def load_scenario(scen_def: str, parent=None):
        """
        :param scen_def: The file containing a single scenario definition, or a scenario definition `dict` .
        :return 'Scenario': A single ``Scenario`` object.
        """

        defaults = {"search_paths": [],
                    "ref_dir": os.path.abspath(os.getcwd())}

        if parent is None:
            parent = {}

        defaults.update(parent)

        if isinstance(scen_def, str):
            scen_def = os.path.abspath(scen_def)
            defaults["search_paths"].append(os.path.dirname(scen_def))
            scen_def = read_yaml(scen_def)

        if not isinstance(scen_def, dict):
            raise TypeError(
                "'scen_def' must be either a str to a file containing a scenario definition or a scenario definition dict.")

        return Scenario(scen_def, parent=defaults)
