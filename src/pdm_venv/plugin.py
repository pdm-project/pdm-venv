from pdm import Project as PdmProject
from pdm.core import Core
from pdm.models.environment import Environment

from pdm_venv.commands import VenvCommand
from pdm_venv.config import venv_configs


class Project(PdmProject):
    def get_environment(self) -> Environment:
        return super().get_environment()


def entry_point(core: Core) -> None:
    core.register_command(VenvCommand)
    for name, item in venv_configs.items():
        core.add_config(name, item)
    core.project_class = Project
