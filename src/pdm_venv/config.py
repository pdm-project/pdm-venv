import os

import appdirs
from pdm.project import ConfigItem
from pdm.project.config import ensure_boolean

venv_configs = {
    "venv.location": ConfigItem(
        "Parent directory for virtualenvs",
        os.path.join(appdirs.user_data_dir("pdm"), "venvs"),
        global_only=True,
    ),
    "venv.backend": ConfigItem(
        "Default backend to create virtualenv", default="virtualenv"
    ),
    # Override the default use_venv value to True
    "use_venv": ConfigItem(
        "Install packages into the activated venv site packages instead of PEP 582",
        True,
        env_var="PDM_USE_VENV",
        coerce=ensure_boolean,
    ),
}
