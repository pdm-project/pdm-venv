import sys

from pdm_venv.backends import CondaBackend, VenvBackend, VirtualenvBackend


def test_virtualenv_backend_create(project, mocker):
    interpreter = project.python_executable
    backend = VirtualenvBackend(project, None)
    assert backend.ident
    mock_call = mocker.patch("subprocess.check_call")
    location = backend.create()
    mock_call.assert_called_once_with(
        [sys.executable, "-m", "virtualenv", str(location), "-p", interpreter]
    )


def test_venv_backend_create(project, mocker):
    interpreter = project.python_executable
    backend = VenvBackend(project, None)
    assert backend.ident
    mock_call = mocker.patch("subprocess.check_call")
    location = backend.create()
    mock_call.assert_called_once_with([interpreter, "-m", "venv", str(location)])


def test_conda_backend_create(project, mocker):
    backend = CondaBackend(project, "3.8")
    assert backend.ident
    mock_call = mocker.patch("subprocess.check_call")
    location = backend.create()
    mock_call.assert_called_once_with(
        ["conda", "create", "--yes", "--prefix", str(location), "pip", "python=3.8"]
    )
