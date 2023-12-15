from pathlib import Path

import pytest
from click.testing import CliRunner


parametrize_directory_paths = pytest.mark.parametrize(
    ("directory_paths", "expected_common_dir_path"),
    (
        # Using relative paths here so that the caller can place them in any directory they want.
        ([Path("some/random/dir")], Path("some/random/dir")),
        ([Path("common/dir"), Path("common/another-dir")], Path("common")),
        ([Path("common/dir"), Path("common/another-dir/subdir")], Path("common")),
    ),
)


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()
