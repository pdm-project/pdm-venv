import abc
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Optional, Tuple, Type

from pdm.exceptions import ProjectError
from pdm.project import Project
from pythonfinder import Finder

from pdm_venv.utils import hash_path


class VirtualenvCreateError(ProjectError):
    pass


class Backend(abc.ABC):
    """The base class for virtualenv backends"""

    def __init__(self, project: Project, python: Optional[str]) -> None:
        self.project = project
        self.python = python

    @property
    def ident(self) -> str:
        """Get the identifier of this virtualenv.
        self.python can be one of:
            3.8
            /usr/bin/python
            3.9.0a4
            python3.8
        """
        python = self.python or "python"
        if os.path.isabs(python):
            return hash_path(python)
        return python

    def _ensure_clean(self, location: Path, force: bool = False) -> None:
        if not location.exists():
            return
        if not force:
            raise VirtualenvCreateError(f"The location {location} is not empty")
        self.project.core.ui.echo(
            f"Cleaning existing target directory {location}", err=True
        )
        shutil.rmtree(location)

    @property
    def name(self) -> str:
        return (
            f"{self.project.root.name}-{hash_path(self.project.root.as_posix())}"
            f"-{self.ident}"
        )

    def get_location(self) -> Path:
        venv_parent = Path(self.project.config["venv.location"])
        if not venv_parent.is_dir():
            venv_parent.mkdir(exist_ok=True, parents=True)
        return venv_parent / self.name

    def create(self, args: Tuple[str] = (), force: bool = False) -> Path:
        location = self.get_location()
        self._ensure_clean(location, force)
        return self.perform_create(location, args)

    @abc.abstractmethod
    def perform_create(self, location: Path, args: Tuple[str] = ()) -> Path:
        pass


class VirtualenvBackend(Backend):
    @property
    def _resolved_interpreter(self) -> str:
        if os.path.isabs(self.python or ""):
            return self.python
        finder = Finder()
        result = finder.find_python_version(self.python)
        if not result:
            raise VirtualenvCreateError(f"Can't find python interpreter {self.python}")
        return result.path.as_posix()

    def perform_create(self, location: Path, args: Tuple[str] = ()) -> Path:
        cmd = [sys.executable, "-m", "virtualenv", location]
        if self.python:
            interpreter = self._resolved_interpreter
        else:
            interpreter = self.project.python_executable
        cmd.extend(["-p", interpreter])
        cmd.extend(args)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            raise VirtualenvCreateError(e) from None


class VenvBackend(VirtualenvBackend):
    def perform_create(self, location: Path, args: Tuple[str]) -> Path:
        if self.python:
            interpreter = self._resolved_interpreter
        else:
            interpreter = self.project.python_executable
        cmd = [interpreter, "-m", "venv", location] + list(args)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            raise VirtualenvCreateError(e) from None


class CondaBackend(Backend):
    def perform_create(self, location: Path, args: Tuple[str]) -> Path:
        cmd = [
            "conda",
            "create",
            "--yes",
            "--prefix",
            location,
            # Ensure the pip package is installed.
            "pip",
        ]

        cmd.extend(args)

        if self.python:
            python_dep = "python={}".format(self.python)
        else:
            python_dep = "python"
        cmd.append(python_dep)


BACKENDS: Mapping[str, Type[Backend]] = {
    "virtualenv": VirtualenvBackend,
    "venv": VenvBackend,
    "conda": CondaBackend,
}
