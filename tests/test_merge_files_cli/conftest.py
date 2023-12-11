import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()
