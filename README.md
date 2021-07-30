# pdm-venv

[![Tests](https://github.com/pdm-project/pdm-venv/workflows/Tests/badge.svg)](https://github.com/pdm-project/pdm-venv/actions?query=workflow%3Aci)
[![pypi version](https://img.shields.io/pypi/v/pdm-venv.svg)](https://pypi.org/project/pdm-venv/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A plugin for pdm that enables virtualenv management

## Requirements

pdm-venv requires Python>=3.7

## Installation

On PDM 1.6.4+, you can install the plugin directly by:

```bash
$ pdm plugin add pdm-venv
```

If `pdm` is installed via [pipx](https://github.com/pipxproject/pipx)(the recommended way), run:

```bash
$ pipx inject pdm pdm-venv
```

Otherwise if `pdm` is installed via Homebrew, run:

```bash
$ $(brew --prefix pdm)/libexec/bin/pip install pdm-venv
```

Or install with `pip` to the user site:

```bash
$ python -m pip install --user pdm-venv
```

Note that `pdm-venv` must be installed to the same environment as `pdm`.

## Usage

`pdm-venv` enhances `pdm`'s CLI with the support of virtualenv creation and management. With `pdm-venv` installed,
the default value of `use_venv` will turn to `True`, you can disable the whole plugin by `pdm config use_venv false`.

### Create a virtualenv

```bash
# Create a virtualenv based on 3.8 interpreter
$ pdm venv create 3.8
# Assign a different name other than the version string
$ pdm venv create --name for-test 3.8
# Use venv as the backend to create, support 3 backends: virtualenv(default), venv, conda
$ pdm venv create --with venv 3.9
```

### List all virtualenv created with this project

```console
$ pdm venv list
Virtualenvs created with this project:

-  3.8.6: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-3.8.6
-  for-test: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test
-  3.9.1: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-3.9.1
```

The name before the colon(:) is the key of the virtualenv which is used in `remove` and `activate` commands below.

### Remove a virtualenv

```console
$ pdm venv remove for-test
Virtualenvs created with this project:
Will remove: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test, continue? [y/N]:y
Removed C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test
```

### Activate a virtualenv

Instead of spawning a subshell like what `pipenv` and `poetry` do, `pdm-venv` doesn't create the shell for you but print the activate command to the console.
In this way you won't lose the fancy shell features. You can then feed the output to `eval` to activate the virtualenv without leaving the current shell:

**Bash/csh/zsh**

```console
$ eval $(pdm venv activate for-test)
(test-project-8Sgn_62n-for-test) $  # Virtualenv entered
```

**Fish**

```console
$ eval (pdm venv activate for-test)
```

**Powershell**

```console
PS1> Invoke-Expression (pdm venv activate for-test)
```

You can make your own shell shortcut function to avoid the input of long command. Here is an example of Bash:

```bash
pdm_venv_activate() {
    eval $('pdm' 'venv' 'activate' "$1")
}
```

Then you can activate it by `pdm_venv_activate $venv_name` and deactivate by `deactivate` directly.

Additionally, if the saved Python interpreter is a venv Python, you can omit the name argument following `activate`.

### Switch Python interpreter

When `pdm-venv` is enabled, Python interpreters associated with the venvs will also show in the interpreter list of `pdm use` or `pdm init` command.

Additionally, if `pdm` detects it is inside an active virtualenv by examining `VIRTUAL_ENV` env var, it will reuse that virtualenv for later actions.

### Virtualenv auto creation

If no Python interpreter is selected for the project, `pdm-venv` will take charge to create one for you and select the venv interpreter automatically, just like
what `pipenv` and `poetry` do.

## Configuration

| Config Item     | Description                                    | Default Value                       | Available in Project | Env var |
| --------------- | ---------------------------------------------- | ----------------------------------- | -------------------- | ------- |
| `venv.location` | The root directory to store virtualenvs        | `appdirs.user_data_dir() / "venvs"` | No                   |         |
| `venv.backend`  | The default backend used to create virtualenvs | `virtualenv`                        | No                   |         |
