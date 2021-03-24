from pathlib import Path

from pdm_venv.plugin import Project


def test_use_venv_default_to_true(invoke):
    result = invoke(["config", "use_venv"])
    assert result.output.strip() == "True"


def test_create_venv_first_time(invoke, isolated):
    result = invoke(["install"])
    assert result.exit_code == 0
    venv_parent = isolated / "venvs"
    venv_path = next(venv_parent.iterdir(), None)
    assert venv_path is not None

    project = Project(isolated)
    assert Path(project.project_config["python.path"]).relative_to(venv_path)


def test_find_interpreters_from_venv(invoke, isolated):
    result = invoke(["install"])
    assert result.exit_code == 0
    venv_parent = isolated / "venvs"
    venv_path = next(venv_parent.iterdir(), None)

    project = Project(isolated)
    assert next(project.find_interpreters()).comes_from.path.relative_to(venv_path)
