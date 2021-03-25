import base64
import hashlib
import sys
from pathlib import Path
from typing import Iterable, Tuple

from pdm.project import Project
from pdm.utils import get_in_project_venv_python

IS_WIN = sys.platform == "win32"
BIN_DIR = "Scripts" if IS_WIN else "bin"


def hash_path(path: str) -> str:
    """Generate a hash for the given path."""
    return base64.urlsafe_b64encode(hashlib.md5(path.encode()).digest()).decode()[:8]


def get_venv_prefix(project: Project) -> str:
    """Get the venv prefix for the project"""
    path = project.root
    name_hash = hash_path(path.as_posix())
    return f"{path.name}-{name_hash}-"


def iter_venvs(project: Project) -> Iterable[Tuple[str, Path]]:
    """Return an iterable of venv paths associated with the project"""
    in_project_venv_python = get_in_project_venv_python(project.root)
    if in_project_venv_python is not None:
        yield "in-project", Path(in_project_venv_python).parent.parent
    venv_prefix = get_venv_prefix(project)
    venv_parent = Path(project.config["venv.location"])
    for venv in venv_parent.glob(f"{venv_prefix}*"):
        ident = venv.name[len(venv_prefix) :]
        yield ident, venv


def get_venv_python(venv: Path) -> Path:
    """Get the interpreter path inside the given venv."""
    suffix = ".exe" if IS_WIN else ""
    return venv / BIN_DIR / f"python{suffix}"
