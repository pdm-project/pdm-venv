# Changelog

<!-- insertion marker -->
[v0.3.1](https://github.com/pdm-project/pdm-venv/releases/tag/0.3.1) (2021-08-23)
---------------------------------------------------------------------------------

### Bug Fixes

- Ensure the location is string when calling subprocesses. This is for the compatibility of Python 3.8-. [#18](https://github.com/pdm-project/pdm-venv/issues/18)


[v0.3.0](https://github.com/pdm-project/pdm-venv/releases/tag/0.3.0) (2021-07-30)
---------------------------------------------------------------------------------

### Bug Fixes

- Add support for powershell version>=6.0 as [executable name](https://powershellexplained.com/2017-12-29-Powershell-what-is-pwsh/#:~:text=The%20pwsh.exe%20process%20is%20the%20new%20name%20for%20PowerShell%20Core%20starting%20with%20version%206.0.%20The%20executable%20changed%20names%20from%20powershell.exe%20to%20pwsh.exe.%20Let%E2%80%99s%20take%20a%20look%20at%20this%20executable.) has changed starting with version 6.0. [##10](https://github.com/pdm-project/pdm-venv/issues/#10)
- Fix the activate script of conda env. Now the output should be eval'd rather than source'd [#14](https://github.com/pdm-project/pdm-venv/issues/14)


[v0.2.0](https://github.com/pdm-project/pdm-venv/releases/tag/0.2.0) (2021-04-12)
---------------------------------------------------------------------------------

### Features & Improvements

- Update per the changes of PDM 1.5.0 prerelease. [#2](https://github.com/pdm-project/pdm-venv/issues/2)


[v0.1.1](https://github.com/pdm-project/pdm-venv/releases/tag/0.1.1) (2021-03-25)
---------------------------------------------------------------------------------

### Features & Improvements

- Honor the virtualenv in active for reuse. This however won't store the interpreter path in `.pdm.toml`. [#1](https://github.com/pdm-project/pdm-venv/issues/1)
