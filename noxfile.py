import os

import nox

os.environ["PDM_IGNORE_SAVED_PYTHON"] = "1"


@nox.session(python=("3.7", "3.8", "3.9", "3.10"))
@nox.parametrize("backend", ("virtualenv", "venv", "conda"))
def test(session, backend):
    os.environ["DEFAULT_BACKEND"] = backend
    session.run("pdm", "install", "-vd", external=True)
    session.run("pytest", "tests/")
