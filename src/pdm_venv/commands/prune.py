import argparse
import shutil

import click
from pdm import Project, termui
from pdm.cli.commands.base import BaseCommand
from pdm.cli.options import verbose_option

from pdm_venv.utils import get_all_venvs


class PruneCommand(BaseCommand):
    """Remove all virtualenv created (danger)"""

    arguments = [verbose_option]

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Force pruning without prompting for confirmation",
        )

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        project.core.ui.echo(
            termui.red("All the following Virtualenvs will be deleted:")
        )

        if options.force or click.confirm(
            termui.yellow("Will remove: \n-{}\ncontinue? ").format(
                "\n-".join([ident for ident, venv in get_all_venvs(project)])
            )
        ):
            for ident, venv in get_all_venvs(project):
                shutil.rmtree(venv)
            project.core.ui.echo("Removed successfully!")
