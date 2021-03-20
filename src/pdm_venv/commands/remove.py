import argparse
import shutil

import click
from pdm import project
from pdm.cli.commands.base import BaseCommand
from pdm.iostream import stream

from pdm_venv.utils import iter_venvs


class RemoveCommand(BaseCommand):
    """Remove the virtualenv with the given name"""

    arguments = []

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            help="Answer yes on the following question",
        )
        parser.add_argument("env", help="The key of the virtualenv")

    def handle(self, project: project, options: argparse.Namespace) -> None:
        stream.echo("Virtualenvs created with this project:")
        for ident, venv in iter_venvs(project):
            if ident == options.env:
                if options.yes or click.confirm(f"Will remove: {venv}, continue?"):
                    shutil.rmtree(venv)
                    stream.echo("Removed successfully!")
                break
        else:
            stream.echo(
                stream.yellow(f"No virtualenv with key {options.env} is found"),
                err=True,
            )
            raise SystemExit(1)
