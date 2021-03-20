import argparse

from pdm.cli.commands.base import BaseCommand
from pdm.iostream import stream
from pdm.project import Project

from pdm_venv.utils import iter_venvs


class ListCommand(BaseCommand):
    """List all virtualenvs associated with this project"""

    arguments = []

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        stream.echo("Virtualenvs created with this project:")
        for ident, venv in iter_venvs(project):
            stream.echo(f"{stream.green(ident)}: {venv}")
