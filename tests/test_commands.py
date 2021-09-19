import os
import re

import pytest


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


def test_venv_purge(invoke, mocker):
    result = invoke(["venv", "create"])
    assert result.exit_code == 0, result.stderr
    venv_path = re.match(
        r"Virtualenv (.+) is created successfully", result.output
    ).group(1)
    result = invoke(["venv", "purge"], input="y")
    assert result.exit_code == 0, result.stderr
    assert not os.path.exists(venv_path)


def test_venv_purge_force(invoke, mocker):
    result = invoke(["venv", "create"])
    assert result.exit_code == 0, result.stderr
    venv_path = re.match(
        r"Virtualenv (.+) is created successfully", result.output
    ).group(1)
    result = invoke(["venv", "purge", "-f"])
    assert result.exit_code == 0, result.stderr
    assert not os.path.exists(venv_path)


user_options = [("none", True), ("0", False), ("all", False)]


@pytest.mark.parametrize("user_choices, is_path_exists", user_options)
def test_venv_purge_interactive(invoke, mocker, user_choices, is_path_exists):
    result = invoke(["venv", "create"])
    assert result.exit_code == 0, result.stderr
    venv_path = re.match(
        r"Virtualenv (.+) is created successfully", result.output
    ).group(1)
    result = invoke(["venv", "purge", "-i"], input=user_choices)
    assert result.exit_code == 0, result.stderr
    assert os.path.exists(venv_path) == is_path_exists
