import asyncio
from pathlib import Path

import pytest

from merge_files.programming_languages import ProgrammingLanguage


parametrize_programming_language = pytest.mark.parametrize("programming_language", [pl for pl in ProgrammingLanguage])
parametrize_output_absolute_file_path = pytest.mark.parametrize("output_absolute_file_path", {False, True})
parametrize_output_preserve_blank_lines = pytest.mark.parametrize("output_preserve_blank_lines", {False, True})
parametrize_output_preserve_empty_files = pytest.mark.parametrize("output_preserve_empty_files", {False, True})


@pytest.fixture()
def event_loop() -> asyncio.AbstractEventLoop:
    """
    Use that fixture when parametrizing a test that involves asyncio event loop one way or the other.

    https://stackoverflow.com/a/72104554/1557013
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def tmp_test_dir_path(tmp_path: Path) -> Path:
    """
    Fixture for creating a mock directory for testing.
    """
    test_dir_path = tmp_path / "test_dir"
    test_dir_path.mkdir(parents=True)
    return test_dir_path
