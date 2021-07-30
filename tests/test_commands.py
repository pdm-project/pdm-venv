import os
import re


def test_venv_create(invoke):
    result = invoke(["venv", "create"])
    assert result.exit_code == 0, result.stderr
    venv_path = re.match(
        r"Virtualenv (.+) is created successfully", result.output
    ).group(1)
    assert os.path.exists(venv_path)


def test_venv_list(invoke):
    result = invoke(["venv", "create"])
    assert result.exit_code == 0, result.stderr
    venv_path = re.match(
        r"Virtualenv (.+) is created successfully", result.output
    ).group(1)

    result = invoke(["venv", "list"])
    assert result.exit_code == 0, result.stderr
    assert venv_path in result.output


def test_venv_remove(invoke):
    result = invoke(["venv", "create"])
    assert result.exit_code == 0, result.stderr
    venv_path = re.match(
        r"Virtualenv (.+) is created successfully", result.output
    ).group(1)
    key = venv_path.rsplit("-", 1)[-1]

    result = invoke(["venv", "remove", "non-exist"])
    assert result.exit_code != 0

    result = invoke(["venv", "remove", "-y", key])
    assert result.exit_code == 0, result.stderr

    assert not os.path.exists(venv_path)


def test_venv_recreate(invoke):
    invoke(["use", "-f", "python"])
    result = invoke(["venv", "create"])
    assert result.exit_code == 0, result.stderr

    result = invoke(["venv", "create"])
    assert result.exit_code != 0

    result = invoke(["venv", "create", "-f"])
    assert result.exit_code == 0, result.stderr


def test_venv_activate(invoke, mocker):
    result = invoke(["venv", "create"])
    assert result.exit_code == 0, result.stderr
    venv_path = re.match(
        r"Virtualenv (.+) is created successfully", result.output
    ).group(1)
    key = venv_path.rsplit("-", 1)[-1]

    mocker.patch("shellingham.detect_shell", return_value=("bash", None))
    result = invoke(["venv", "activate", key])
    assert result.exit_code == 0, result.stderr

    if os.getenv("DEFAULT_BACKEND") == "conda":
        assert result.output.startswith("conda activate")
    else:
        assert result.output.strip("'\"\n").endswith("activate")
        assert result.output.startswith("source")


def test_venv_auto_create(invoke, mocker):
    creator = mocker.patch("pdm_venv.backends.Backend.create")
    invoke(["install"])
    creator.assert_called_once()
