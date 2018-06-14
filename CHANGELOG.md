# Changelog

## [0.2] - 2018-06-14:

### Changed
 * (BACKWARDS INCOMPATIBLE) Command-line interface for ``concero`` has been changed to enable data format conversion operations (without model executions) from the command line. A ``Scenario`` defined in a YAML file is now run like:

    ```concero run scenario_file.yaml```

   And data format conversion can be accomplished by running the command:

   ```concero convert import_def.yaml export_def.yaml```

   Or (more simply):

   ```concero co import_def.yaml export_def.yaml```

 * Removed requirement for procedures to have a specified `name`. `name` will be `"Unnamed_proc"` by default. Documentation has been updated to reflect this.
 * Removed requirements for models to have a specified `name` and ``cmds`` (and updated documentation to reflect this). A default name is given if none is provided.
 * Removed the requirement for scenarios to have a specified ``name`` (a default ``name`` is given instead). Documentation updated to reflect this.