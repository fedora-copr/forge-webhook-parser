import glob
from pathlib import Path

import nox

LINT_FILES = glob.glob("*.py")

requirements_directory = Path("requirements")

requirements_files = [
    requirements_input_file_path.stem
    for requirements_input_file_path in requirements_directory.glob("*.in")
]


@nox.session(name="pip-compile", python=["3.12"])
@nox.parametrize(["req"], arg_values_list=requirements_files, ids=requirements_files)
def pip_compile(session: nox.Session, req: str):
    """Generate lock files from input files or upgrade packages in lock files."""
    # fmt: off
    session.install(
      "-r", str(requirements_directory / "pip-tools.in"),
      "-c", str(requirements_directory / "pip-tools.txt"),
    )
    # fmt: on

    # Use --upgrade by default unless a user passes -P.
    upgrade_related_cli_flags = ("-P", "--upgrade-package", "--no-upgrade")
    has_upgrade_related_cli_flags = any(
        arg.startswith(upgrade_related_cli_flags) for arg in session.posargs
    )
    injected_extra_cli_args = () if has_upgrade_related_cli_flags else ("--upgrade",)

    session.run(
        "pip-compile",
        "--output-file",
        str(requirements_directory / f"{req}.txt"),
        *session.posargs,
        *injected_extra_cli_args,
        str(requirements_directory / f"{req}.in"),
    )


def install(session: nox.Session, req: str):
    session.install(
        "-r",
        str(requirements_directory / f"{req}.in"),
        "-c",
        str(requirements_directory / f"{req}.txt"),
    )


@nox.session
def static(session: nox.Session):
    """
    Run static checkers
    """
    install(session, req="static")
    session.run("ruff", "check", *session.posargs, *LINT_FILES)


@nox.session
def formatters(session: nox.Session):
    """
    Reformat code
    """
    install(session, req="formatters")
    session.run("isort", *session.posargs, *LINT_FILES)
    session.run("black", *session.posargs, *LINT_FILES)


@nox.session
def formatters_check(session: nox.Session):
    """
    Check code formatting without making changes
    """
    install(session, req="formatters")
    session.run("isort", "--check", *session.posargs, *LINT_FILES)
    session.run("black", "--check", *session.posargs, *LINT_FILES)


@nox.session
def typing(session: nox.Session):
    """
    Run static type checker
    """
    install(session, req="typing")
    session.run("mypy", *session.posargs, *LINT_FILES)


@nox.session
def lint(session: nox.Session):
    session.notify("static")
    session.notify("formatters")
    session.notify("typing")
