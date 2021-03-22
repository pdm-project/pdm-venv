"""Configuration for the pytest test suite."""
import functools
import os
import pytest
from click.testing import CliRunner
from pdm.core import Core
from pdm_venv.plugin import Project
from pdm.utils import cd, temp_environ

DUMMY_PYPROJECT = """[project]
requires-python = ">=3.6"
dependencies = []
"""


@pytest.fixture
def isolated(tmp_path, mocker):
    tmp_path.joinpath("pyproject.toml").write_text(DUMMY_PYPROJECT)
    mocker.patch("pathlib.Path.home", return_value=tmp_path)
    return tmp_path


@pytest.fixture
def project(isolated):
    core = Core()
    core.init_parser()
    core.load_plugins()
    p = Project(isolated)
    p.core = core
    return p


DEFAULT_BACKEND = os.getenv("VENV_BACKEND", "virtualenv")


@pytest.fixture
def invoke(isolated):
    runner = CliRunner(mix_stderr=False)
    core = Core()
    with cd(isolated), temp_environ():
        os.environ.pop("VIRTUAL_ENV", None)
        runner.invoke(
            core, ["config", "venv.backend", DEFAULT_BACKEND], prog_name="pdm"
        )
        runner.invoke(
            core, ["config", "venv.location", str(isolated / "venvs")], prog_name="pdm"
        )
        (isolated / ".pdm.toml").unlink(True)
        yield functools.partial(runner.invoke, core, prog_name="pdm")
