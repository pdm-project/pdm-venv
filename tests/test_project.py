from pathlib import Path


def test_use_venv_default_to_true(invoke):
    result = invoke(["config", "use_venv"])
    assert result.output.strip() == "True"


def test_create_venv_first_time(invoke, project):
    result = invoke(["install"])
    assert result.exit_code == 0
    venv_parent = project.root / "venvs"
    venv_path = next(venv_parent.iterdir(), None)
    assert venv_path is not None

    assert Path(project.project_config["python.path"]).relative_to(venv_path)


def test_find_interpreters_from_venv(invoke, project):
    result = invoke(["install"])
    assert result.exit_code == 0
    venv_parent = project.root / "venvs"
    venv_path = next(venv_parent.iterdir(), None)

    assert Path(next(project.find_interpreters()).executable).relative_to(venv_path)
