#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess  # noqa: S404
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, NoReturn

from typer import Typer

if TYPE_CHECKING:
    from collections.abc import Iterable

app = Typer()


@app.callback()
def callback() -> None:
    """Build tools."""


@app.command()
def lint(*, fix: bool = False) -> None:
    """Run all linters and type checkers in order of importance - returns the first non-zero exit code or zero."""
    _run_commands_threaded(
        (
            _black_format_command(fix=fix),
            _mypy_command(),
            _flake8_command(),
            _yamllint_command(),
            _flynt_command(fix=fix),
        ),
    )


@app.command()
def lint_and_test(*, fix: bool = False) -> None:
    """Run all code fixs in order of importance - returns the first non-zero exit code or zero."""
    _run_commands_threaded(
        (
            _black_format_command(fix=fix),
            _mypy_command(),
            _flake8_command(),
            _pytest_command(),
            _yamllint_command(),
            _flynt_command(fix=fix),
        ),
    )


@app.command()
def black_format(*, fix: bool = False) -> None:
    """Run Black linter."""
    _run(_black_format_command(fix=fix))


def _black_format_command(*, fix: bool) -> str:
    return f"black {'' if fix else '--check '}{_python_base_paths_str()}"


@app.command()
def build(
    *,
    force: bool = False,
    help: bool = False,
    path: str = "dist",
) -> None:
    """Run ansible-galaxy collection build ."""
    _run(
        _build_command(
            force=force,
            help=help,
            path=path,
        ),
    )

def _build_command(
    *,
    force: bool,
    help: bool,
    path: str = "dist",
) -> str:
    command = "ansible-galaxy collection build ./pan_scm_ansible_collection"
    if force:
        command += " --force"
    if help:
        command += " --help"
    if path:
        command += f" --output-path {path}"
    return command

@app.command()
def install(
    *,
    force: bool = False,
    help: bool = False,
    version: str,
) -> None:
    """Run ansible-galaxy collection install ./dist/pan_scm_ansible_collection-*.tar.gz."""
    _run(
        _install_command(
            force=force,
            help=help,
            version=version,
        ),
    )

def _install_command(
    *,
    force: bool,
    help: bool,
    version: str,
) -> str:
    command = f"ansible-galaxy collection install dist/cdot65-scm-{version}.tar.gz "
    if force:
        command += " --force"
    if help:
        command += " --help"
    return command



@app.command()
def pytest(
    *,
    profile: bool = False,
    coverage: bool = True,
    threaded: bool = False,
) -> None:
    """Run pytest unittests."""
    _run(
        _pytest_command(
            profile=profile,
            coverage=coverage,
            threaded=threaded,
        ),
        environment={"COVERAGE_CORE": "sysmon"},
    )


def _pytest_command(
    *,
    profile: bool = False,
    coverage: bool = True,
    threaded: bool = False,
) -> str:
    command = "pytest"
    if profile:
        command += " --profile --profile-svg"
    if coverage:
        command += " --cov=pan_scm_ansible_collection --cov-fail-under=70 --cov-report=term-missing"
    if threaded:
        command += " -n auto"
    return command


@app.command()
def yamllint() -> None:
    """Run yamllint to check YAML syntax."""
    _run(_yamllint_command())


def _yamllint_command() -> str:
    return f"yamllint {_repo_path().relative_to(Path.cwd())}"


@app.command()
def flake8() -> None:
    """Run flake8 linter."""
    _run(_flake8_command())


def _flake8_command() -> str:
    return f"flake8 {_python_base_paths_str()}"


@app.command()
def mypy() -> None:
    """Run mypy type checker."""
    _run(_mypy_command())


def _mypy_command() -> str:
    return f"mypy {_python_base_paths_str()}"


@app.command()
def flynt(*, fix: bool = False) -> None:
    """Run flynt to enforce the use of f-strings."""
    _run(_flynt_command(fix=fix))


def _flynt_command(*, fix: bool) -> str:
    if fix:
        return f"flynt -tc {_python_base_paths_str()}"
    return f"flynt -d -tc -f {_python_base_paths_str()}"


@cache
def _python_base_paths_str() -> str:
    return " ".join(str(p) for p in _python_base_paths())


def _python_base_paths() -> Iterable[Path]:
    yield from (f.relative_to(Path.cwd()) for f in _project_base_paths("*.py"))


def _project_base_paths(glob: str) -> Iterable[Path]:
    yield from _project_paths(glob)
    yield from _project_base_files(glob)


def _project_base_files(glob: str) -> Iterable[Path]:
    yield from _repo_path().glob(glob)


def _project_paths(glob: str) -> Iterable[Path]:
    for base_dir in ("pan_scm_ansible_collection", "tests", "scripts"):
        base_path = _repo_path().joinpath(base_dir)
        if not base_path.exists():
            message = f"{base_path=} does not exist"
            raise FileNotFoundError(message)

        if next(base_path.glob(glob), None):
            yield base_path


def _run_commands_threaded(commands: tuple[str, ...]) -> NoReturn:
    return_codes: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=len(commands)) as executor:
        for future in as_completed(
            executor.submit(
                _run_for_thread,
                command,
            )
            for command in commands
        ):
            command, return_code, output = future.result()
            if return_code:
                print(output)  # noqa: T201
            return_codes[command] = return_code

    error_found = False
    for command, return_code in return_codes.items():
        if return_code != 0:
            print(f"{command.split()[0]} -> {return_code}")  # noqa: T201
            error_found = True
    if error_found:
        sys.exit(1)
    print("No issues found")  # noqa: T201
    sys.exit()


def _run(
    command: str,
    *,
    check: bool = True,
    environment: dict[str, str] | None = None,
) -> int:
    print(f"\n======== {command} ========\n")  # noqa: T201
    my_env = os.environ.copy()
    if environment:
        my_env.update(environment)
    result = subprocess.run(command.split(), check=False, env=my_env)  # noqa: S603
    if check:
        sys.exit(result.returncode)
    return result.returncode


def _run_for_thread(command: str) -> tuple[str, int, str]:
    print(f"Running: {command}")  # noqa: T201
    result = subprocess.run(  # noqa: S603
        command.split(),
        check=False,
        capture_output=True,
    )
    output = f"\n======== {command} ========\n{result.stdout.decode()}\n{result.stderr.decode()}"
    return command, result.returncode, output


@cache
def _repo_path() -> Path:
    return Path(__file__).parents[1]


def main() -> None:
    app()


if __name__ == "__main__":
    main()
