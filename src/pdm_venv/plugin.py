import os
from pathlib import Path
from typing import Iterable, Optional

from pdm import Project as PdmProject
from pdm import termui
from pdm.core import Core
from pdm.models.environment import Environment, GlobalEnvironment
from pdm.models.python import PythonInfo
from pdm.models.specifiers import PySpecSet
from pdm.utils import is_venv_python

from pdm_venv.backends import BACKENDS
from pdm_venv.commands import VenvCommand
from pdm_venv.config import venv_configs
from pdm_venv.utils import get_venv_python, iter_venvs


class Project(PdmProject):
    def find_interpreters(
        self, python_spec: Optional[str] = None
    ) -> Iterable[PythonInfo]:

        for _, venv in iter_venvs(self):
            python = get_venv_python(venv).as_posix()
            py_version = PythonInfo.from_path(python)
            if not python_spec:
                yield py_version
            elif all(d.isdigit() for d in python_spec.split(".")):
                desired = tuple(int(d) for d in python_spec.split("."))
                if py_version.version_tuple[: len(desired)] == desired:
                    yield py_version

        yield from super().find_interpreters(python_spec)

    def get_environment(self) -> Environment:
        if self.is_global:
            env = GlobalEnvironment(self)
            # Rewrite global project's python requires to be
            # compatible with the exact version
            env.python_requires = PySpecSet(f"=={self.python.version}")
            return env
        if self.config["use_venv"]:
            if self.project_config.get("python.path") and not os.getenv(
                "PDM_IGNORE_SAVED_PYTHON"
            ):
                return (
                    GlobalEnvironment(self)
                    if is_venv_python(self.python.executable)
                    else Environment(self)
                )
            if os.getenv("VIRTUAL_ENV"):
                venv = os.getenv("VIRTUAL_ENV")
                self.core.ui.echo(
                    f"Detected inside an active virtualenv {termui.green(venv)}, "
                    "reuse it."
                )
                # Temporary usage, do not save in .pdm.toml
                self._python = PythonInfo.from_path(get_venv_python(Path(venv)))
                return GlobalEnvironment(self)
            existing_venv = next((venv for _, venv in iter_venvs(self)), None)
            if existing_venv:
                self.core.ui.echo(
                    f"Virtualenv {termui.green(str(existing_venv))} is reused.",
                    err=True,
                )
                path = existing_venv
            else:
                # Create a virtualenv using the selected Python interpreter
                self.core.ui.echo(
                    "use_venv is on, creating a virtualenv for this project...",
                    fg="yellow",
                    err=True,
                )
                backend: str = self.config["venv.backend"]
                venv_backend = BACKENDS[backend](self, None)
                path = venv_backend.create(None, (), False)
                self.core.ui.echo(f"Virtualenv {path} is created successfully")
            self.python = PythonInfo.from_path(get_venv_python(path))
            return GlobalEnvironment(self)
        else:
            return Environment(self)


def entry_point(core: Core) -> None:
    core.register_command(VenvCommand)
    for name, item in venv_configs.items():
        core.add_config(name, item)
    core.project_class = Project
