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
    key_venvs = list(utils.iter_venvs(project))
    assert key_venvs[0][0] == "in-project"
    assert key_venvs[1][0] == "bar"
    assert key_venvs[2][0] == "baz"
    assert key_venvs[3][0] == "foo"
