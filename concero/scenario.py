"""
Created on Feb 05 09:44:50 2018

.. sectionauthor:: Lyle Collins <Lyle.Collins@csiro.au>
.. codeauthor:: Lyle Collins <Lyle.Collins@csiro.au>
"""

import os
import copy

import concero.conf as conf
from concero.format_convert_tools import read_yaml
from concero.model import Model
from concero.to_cero import ToCERO
from concero.from_cero import FromCERO
from concero.cero import CERO

class Scenario(dict):

    _logger = conf.setup_logger(__name__)

    def __init__(self, sc_def: dict, *args, scenarios_set: 'ScenariosSet' = None,
                 parent: dict=None,
                 **kwargs):
        """
        :param sc_def: A scenario definition object.
        :param args: Passed to the superclass (dict) as positional arguments at initialisation.
        :param scenarios_set: A ScenariosSet object, used to verify that ``sc_def`` is a valid \
        definition.
        :param kwargs: Passed to the superclass (dict) as keyword arguments at initialisation.
        """

        defaults = {"search_paths": [],
                    "ref_dir": None,
                    "models": [],
                    "scenarios_set": None,
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

        if scenarios_set is not None:
            defaults["scenarios_set"] = scenarios_set

        sc_def = defaults
        super().__init__(sc_def, *args, **kwargs)

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

        if self.get("scenarios_set"):
            scenarios_set = ScenariosSet(scen_defs=self["scenarios_set"])

        if scenarios_set is not None:
            self.link_scenario_set(scenarios_set)

        if "run_no" not in self:
            # run_no defaults to 1 if not provided
            self["run_no"] = 1

    def run(self) -> None:
        """
        Execute a scenario run.
        """

        self.cero = CERO.create_empty()

        ceros = [in_conf.create_cero() for in_conf in self["input_conf"]]
        self.cero = CERO.combine_ceros(ceros)
        print("Successfully loaded scenario inputs as CERO.")

        FromCERO.xlsx_out(self.cero, (self.get_name() + "_%03d_step_%02d.xlsx" % (self["run_no"], 0)))

        for idx, model in enumerate(self["models"]):
            m_cero = model.run(self.cero)
            print("Completed run of model (%s)." % model["name"])

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
            raise TypeError("Not all required key-value pairs have been defined. " +
                            "It is necessary to define all of %s." % req_keys)

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


    def link_scenario_set(self, scenarios_set: 'ScenariosSet') -> None:
        """Link a ScenariosSet object (``scenarios_set``) to this Scenario (if it hasn't already been done).
        """
        scenarios_set.is_valid_def(self)  # Check if scenario definition is valid
        self._linked_scenariosets = getattr(self, "_linked_scenariosets", [])
        if not any([ss == scenarios_set for ss in self._linked_scenariosets]):
            self._linked_scenariosets.append(scenarios_set)
        else:
            msg = "ScenariosSet already linked to Scenario."
            print(msg)
            Scenario._logger.error(msg)
            raise RuntimeError(msg)

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
    def load_scenarios(scen_def: str, scenarios_set: 'ScenariosSet' = None, parent=None):
        """

        :param scen_def: The file containing one or more scenario definitions.
        :param scenarios_set: Either a ``ScenariosSet`` object or a reference to a file containing a ``ScenariosSet`` \
        definition.
        :return "Union['Scenario', List['Scenario']]": Either a single ``Scenario``, or a ``list`` of ``Scenario``s.
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
            return [Scenario.load_scenario(scen_def, scenarios_set=scenarios_set, parent=defaults)]
        elif isinstance(scen_def, list):
            # List of scenarios
            return [Scenario.load_scenario(scd, scenarios_set=scenarios_set, parent=defaults) for scd in scen_def]

    @staticmethod
    def load_scenario(scen_def: str, scenarios_set: 'ScenariosSet' = None, parent=None):
        """
        :param scen_def: The file containing a single scenario definition, or a scenario definition `dict` .
        :param scenarios_set: Either a ``ScenariosSet`` object or a reference to a file containing a ``ScenariosSet`` definition.
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

        return Scenario(scen_def, scenarios_set=scenarios_set, parent=defaults)


class ScenariosSet(list):

    def __init__(self, scen_defs: str, *args, **kwargs):
        """
        A ``ScenariosSet`` object defines a set of valid ``Scenario``, and is therefore can be used to \
        name a ``Scenario``, or check validity of a ``Scenario``.

        :param scen_defs: The file containing the definition of valid scenarios.
        :param args: Passed to the superclass (``list``) on initialisation.
        :param kwargs: Passed to the superclass (``list``) on initialisation.
        """

        if isinstance(scen_defs, str):
            scen_defs = os.path.abspath(scen_defs)
            # scen_defs = os.path.relpath(os.path.normpath(scen_defs))
            scen_defs = read_yaml(scen_defs)

        if isinstance(scen_defs, dict):
            # If dict, assumed to be single-workstream ScenarioSet
            scen_defs = [scen_defs]

        try:
            assert(issubclass(type(scen_defs), list))
        except AssertionError:
            raise RuntimeError("'scen_defs' must be provided as a filename, or a list of workstreams, or a dict representing a single workstream.")

        scen_defs = [_WorkStream(wkstrm_def) for wkstrm_def in scen_defs]

        super().__init__(scen_defs, *args, **kwargs)

    def is_valid(self):
        """Checks object is a valid ScenarioSet. NOT implemented."""
        #TODO: Write this
        pass


    def is_valid_def(self, scenario):
        """Checks that ``scenario`` is a valid definition for this ``ScenarioSet``. A scenario is a valid definition\
        if it is an element of the set defined by ``self``."""

        try:
            assert isinstance(scenario, Scenario)

        except AssertionError:
            raise TypeError("Invalid scenario definition. Argument 'scenario' is not of scenario.Scenario type.")

        wkstrm_ids = [wkstrm["id"] for wkstrm in self]
        try:
            assert all([k in wkstrm_ids for k in scenario["def"].keys()])
        except AssertionError:
            raise TypeError("Non-existant workstreams defined in scenario.")

        try:
            assert all([wkstrm_id in scenario["def"].keys() for wkstrm_id in wkstrm_ids])
        except AssertionError:
            raise TypeError("Not all workstreams have been defined.")

        for wkstrm in self:
            id = wkstrm["id"]
            wkstrm.is_valid_def(scenario["def"][id])

        return True

    def get_scenario_name(self, scenario: Scenario, long_form=True) -> str:
        """
        Given ``scenario``, returns the name of the ``scenario`` in a long or short form.
        :param scenario: A ``Scenario`` object to retrieve the name of.
        :param long_form: If ``True`` (default), return the long form name, otherwise return the short form.
        :return: The name of the ``Scenario``.
        """

        assert self.is_valid_def(scenario)
        try:
            assert ("name" in scenario)
        except AssertionError:
            raise TypeError("Scenario must have a name to provide string representation.")

        nm = scenario["name"] + "_"

        for wkstrm in self:
            id = wkstrm["id"]
            nm += wkstrm.get_str(scenario["def"][id], long_form=long_form)
        return nm

    def __eq__(self, other):
        try:
            return [self.items()] == [other.items()]
        except AttributeError:
            return False


class _WorkStream(dict):

    def __init__(self, wkstrm_dict, *args, **kwargs):
        super().__init__(wkstrm_dict, *args, **kwargs)
        self.is_valid()
        self["issues"] = [_Issue(issue) for issue in self["issues"]]

    def is_valid(self):
        try:
            assert (type(self.get("issues")) is list)
            assert (all([
                "id" in self,
                "issues" in self,
            ]))
        except AssertionError:
            raise RuntimeError("Invalid workstream definition provided.")
        return True

    def is_valid_def(self, workstream):
        issue_ids = [issue["id"] for issue in self["issues"]]
        try:
            assert all([k in issue_ids for k in workstream.keys()])
        except AssertionError:
            raise TypeError("Issues inappropriate for workstream %s defined." % self["id"])

        try:
            assert all([issue_id in workstream.keys() for issue_id in issue_ids])
        except AssertionError:
            raise TypeError("Not all issues for workstream %s have been defined." % self["id"])

        for issue in self["issues"]:
            id = issue["id"]
            issue.is_valid_def(workstream[id])

        return True

    def get_str(self, workstrm_def, long_form=True):
        nm = self["id"] + "_"
        for issue in self["issues"]:
            id = issue["id"]
            nm += issue.get_str(workstrm_def[id], long_form=long_form)
        return nm


class _Issue(dict):

    def __init__(self, issue_dict, *args, **kwargs):
        super().__init__(issue_dict, *args, **kwargs)
        self.is_valid()

    def is_valid(self):
        try:

            assert (all([
                "id" in self,
                "values" in self,
                type(self["values"]) is list,
            ]))
            assert (type(value) in [str, float, int, bool] for value in self.get("values", []))
        except AssertionError:
            raise RuntimeError("Invalid issue definition provided.")

    def is_valid_def(self, issue):
        try:
            assert (issue in self["values"])
        except AssertionError:
            raise TypeError("Inappropriate value for issue %s defined." % self["id"])
        return True

    def get_str(self, issue_def, long_form=True):
        nm = self["id"] if long_form else ""
        if isinstance(issue_def, bool):
            nm += "B" if issue_def else "O"
        else:
            nm += issue_def
        return nm

