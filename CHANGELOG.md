# Changelog

## [0.6 - Unreleased]

## [0.5] - 2018-06-22

### Changed

 * `matplotlib`, `pyqt4` are now imported as needed, removing PyQt4 as a strict dependency for ConCERO.

## [0.4] - 2018-06-22:

### Added

 * Added pip-compatible changes.

## [0.3] - 2018-06-22:

### Added

 * Experimental support for *importing* VEDA data files (no export support yet).
 * Experimental support for *importing* GDX data files (no export support yet).
 * Anaconda environment file to simplify install process.
 * `-v`/`--version` option for printing program version.
 * Date and time is now printed at completion of model execution.
 * Tests of ``__main__``.
 * Added tests and documentation of `init`, `init_cols`, `init_icols`, `auto_init` and corresponding post keyword arguments of wrapper functions.

### Changed

 * Minimum python requirement increased to `3.5`.
 * Minimum pandas requirement increased to `0.23`.

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