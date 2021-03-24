from pathlib import Path

from pdm_venv import utils


def test_iter_project_venvs(project):
    venv_parent = Path(project.config["venv.location"])
    venv_prefix = utils.get_venv_prefix(project)
    for name in ("foo", "bar", "baz"):
        venv_parent.joinpath(venv_prefix + name).mkdir(parents=True)
    (project.root / ".venv" / utils.BIN_DIR).mkdir(parents=True)
    (
        project.root
        / ".venv"
        / utils.BIN_DIR
        / f"python{'.exe' if utils.IS_WIN else ''}"
    ).touch()
    venv_keys = [key for key, _ in utils.iter_venvs(project)]
    assert sorted(venv_keys) == ["bar", "baz", "foo", "in-project"]
