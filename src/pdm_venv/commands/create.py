import argparse

from pdm import BaseCommand, Project, termui
from pdm.cli.options import verbose_option

from pdm_venv.backends import BACKENDS


class CreateCommand(BaseCommand):
    """Create a virtualenv

    pdm venv create <python> [-other args]
    """

    description = "Create a virtualenv"
    arguments = [verbose_option]

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-w",
            "--with",
            dest="backend",
            choices=BACKENDS.keys(),
            help="Speicify the backend to create the virtualenv",
        )
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Recreate if the virtualenv already exists",
        )
        parser.add_argument("-n", "--name", help="Specify the name of the virtualenv")
        parser.add_argument(
            "python",
            nargs="?",
            help="Specify which python should be used to create the virtualenv",
        )
        parser.add_argument(
            "venv_args",
            nargs=argparse.REMAINDER,
            help="Additional arguments that will be passed to the backend",
        )

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        backend: str = options.backend or project.config["venv.backend"]
        venv_backend = BACKENDS[backend](project, options.python)
        with project.core.ui.open_spinner(
            f"Creating virtualenv using {backend}..."
        ) as spinner:
            path = venv_backend.create(options.name, options.venv_args, options.force)
            spinner.succeed(
                f"Virtualenv {termui.green(str(path))} is created successfully"
            )
