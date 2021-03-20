import pdm_venv


def test_import_package():
    assert isinstance(pdm_venv.__all__, list)
