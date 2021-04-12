"""Configuration for the pytest test suite."""
import functools
import os

import pytest
from click.testing import CliRunner
from pdm.core import Core
from pdm.utils import cd

DUMMY_PYPROJECT = """[project]
requires-python = ">=3.6"
dependencies = []
"""


@pytest.fixture
def isolated(tmp_path, mocker, monkeypatch):
    tmp_path.joinpath("pyproject.toml").write_text(DUMMY_PYPROJECT)
    mocker.patch("pathlib.Path.home", return_value=tmp_path)
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    return tmp_path


@pytest.fixture
def project(isolated):
    core = Core()
    core.init_parser()
    core.load_plugins()
    p = core.create_project(isolated)
    p.global_config["venv.location"] = str(isolated / "venvs")
    p.global_config["venv.backend"] = os.getenv("VENV_BACKEND", "virtualenv")
    return p


@pytest.fixture
def invoke(isolated, monkeypatch):
    runner = CliRunner(mix_stderr=False)
    core = Core()
    invoker = functools.partial(runner.invoke, core, prog_name="pdm")
    monkeypatch.delenv("PDM_IGNORE_SAVED_PYTHON", raising=False)
    with cd(isolated):
        invoker(["config", "venv.location", str(isolated / "venvs")])
        invoker(["config", "venv.backend", os.getenv("VENV_BACKEND", "virtualenv")])
        if (isolated / ".pdm.toml").exists():
            (isolated / ".pdm.toml").unlink()
        yield invoker
