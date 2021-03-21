import argparse

from pdm import termui
from pdm.cli.commands.base import BaseCommand
from pdm.project import Project

from pdm_venv.utils import iter_venvs


class ListCommand(BaseCommand):
    """List all virtualenvs associated with this project"""

    arguments = []

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        project.core.ui.echo("Virtualenvs created with this project:\n")
        for ident, venv in iter_venvs(project):
            project.core.ui.echo(f"  {termui.green(ident)}: {venv}")
