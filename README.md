# forge-webhook-parser

[![Repository License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](COPYING)

Library for parsing webhook payloads from popular git forges

## Verifying your pull request

We welcome all contributions.
If you plan to submit a pull request with changes, you should run the automated tests to check for issues.

### Setting up nox

This project includes a `nox` configuration to automate tests, checks, and other functions.
You can use these automated tests to help you verify changes before you submit a PR.

* Install `nox` using `python3 -m pip install nox` or your distribution's package manager.

* Execute `nox` from the repository root with no arguments to run all Python code checkers.

* Alternatively, you can run only certain tasks as outlined in the following sections.
  Run `nox --list` to view available sessions.

### Running automated tests

* Perform static analysis with [ruff](https://docs.astral.sh/ruff/).

  ``` bash
  nox -s static
  ```

* Reformat code with [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/).

  ``` bash
  nox -s formatters
  ```

* Check code for formatting issues without applying changes.

  ``` bash
  nox -s formatters_check
  ```

* Perform static type checking with [mypy](https://mypy.readthedocs.io/en/stable/).

  ``` bash
  nox -s typing
  ```

## Dependency files

`nox` sessions use dependencies from requirements files in the `requirements/` directory.
Each session has a `requirements/*.in` file with direct dependencies and a lock file in `requirements/*.txt` that pins exact versions for both direct and transitive dependencies.

* Use the following `nox` session to update all dependency lock files:

  ``` bash
  nox -s pip-compile
  ```

* Update specific dependency lock files with individual `nox` sessions, for example:

  ``` bash
  nox -s "pip-compile-3.12(formatters)"
  ```

By default, the `nox` sessions upgrade dependencies.
You can pass `pip-compile` options `--no-upgrade` and `--upgrade-package` to update only specific packages and keep other dependencies at their current version.
For example, to upgrade the `isort` package only:

``` bash
nox -s "pip-compile-3.12(formatters)" -- --no-upgrade --upgrade-package=isort
```
