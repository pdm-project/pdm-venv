import argparse
import shutil

import click
from pdm import Project, termui
from pdm.cli.commands.base import BaseCommand
from pdm.cli.options import verbose_option

from pdm_venv.utils import get_all_venvs


class PurgeCommand(BaseCommand):
    """Purge selected/all created Virtualenvs"""

    arguments = [verbose_option]

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Force purging without prompting for confirmation",
        )
        parser.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            help="Interatively purge selected Virtualenvs",
        )

    def handle(self, project: Project, options: argparse.Namespace) -> None:

        if not options.force:
            project.core.ui.echo(
                termui.red("The following Virtualenvs will be purged:")
            )
            for i, venv in enumerate(get_all_venvs(project)):
                project.core.ui.echo(f"{i}. {termui.green(venv[0])}")

        if not options.interactive and (
            options.force or click.confirm(termui.yellow("continue? "))
        ):
            self.del_all_venvs(project)

        if options.interactive:
            selection = click.prompt(
                "Please select",
                type=click.Choice(
                    [str(i) for i in range(len(list(get_all_venvs(project))))]
                    + ["all", "none"]
                ),
                default="none",
                show_choices=False,
            )

            if selection == "all":
                self.del_all_venvs(project)
            elif selection != "none":
                for i, venv in enumerate(get_all_venvs(project)):
                    if i == int(selection):
                        shutil.rmtree(venv[1])
                project.core.ui.echo("Purged successfully!")

    def del_all_venvs(self, project):
        for _, venv in get_all_venvs(project):
            shutil.rmtree(venv)
        project.core.ui.echo("Purged successfully!")
