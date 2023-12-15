from pathlib import Path

import pytest


@pytest.fixture
def resources_dir_path() -> Path:
    """
    Fixture for the path to the resources directory.
    """
    return Path(__file__).parent / "resources"
