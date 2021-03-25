from pathlib import Path

from pdm_venv import utils


def test_iter_project_venvs(project):
    venv_parent = Path(project.config["venv.location"])
    venv_prefix = utils.get_venv_prefix(project)
    for name in ("foo", "bar", "baz"):
        venv_parent.joinpath(venv_prefix + name).mkdir(parents=True)
    dot_venv_python = utils.get_venv_python(project.root / ".venv")
    dot_venv_python.parent.mkdir(parents=True)
    dot_venv_python.touch()
    venv_keys = [key for key, _ in utils.iter_venvs(project)]
    assert sorted(venv_keys) == ["bar", "baz", "foo", "in-project"]
