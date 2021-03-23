import argparse

from pdm import Project
from pdm.cli.commands.base import BaseCommand

from pdm_venv.commands.activate import ActivateCommand
from pdm_venv.commands.create import CreateCommand
from pdm_venv.commands.list import ListCommand
from pdm_venv.commands.remove import RemoveCommand


class VenvCommand(BaseCommand):
    """Virtualenv management"""

    name = "venv"
    arguments = []

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        subparser = parser.add_subparsers()
        CreateCommand.register_to(subparser, "create")
        ListCommand.register_to(subparser, "list")
        RemoveCommand.register_to(subparser, "remove")
        ActivateCommand.register_to(subparser, "activate")
        self.parser = parser

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        self.parser.print_help()
