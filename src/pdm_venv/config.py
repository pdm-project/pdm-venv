import os

import appdirs
from pdm.project import ConfigItem

venv_configs = {
    "venv.location": ConfigItem(
        "Parent directory for virtualenvs",
        os.path.join(appdirs.user_data_dir("pdm"), "venvs"),
        global_only=True,
    ),
    "venv.backend": ConfigItem(
        "Default backend to create virtualenv", default="virtualenv"
    ),
}
