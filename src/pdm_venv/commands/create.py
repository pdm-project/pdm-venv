import argparse

from pdm import BaseCommand, Project, stream

from pdm_venv.backends import BACKENDS


class CreateCommand(BaseCommand):
    """Create a virtualenv

    pdm venv create <python> [-other args]
    """

    description = "Create a virtualenv"
    arguments = []

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
            help="Clean the target location in case it already exists",
        )
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
        path = venv_backend.create(options.venv_args, options.force)
        stream.echo(f"Virtualenv {path} is created successfully")
