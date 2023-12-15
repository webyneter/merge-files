from pathlib import Path

import aiofiles
import pytest

from merge_files.files import merge
from merge_files.programming_languages import ProgrammingLanguage
from tests.conftest import parametrize_programming_language
from tests.test_merge_files.constants import JSONL_FILE_EXTENSION
from tests.test_merge_files.constants import TXT_FILE_EXTENSION
from tests.test_merge_files.constants import YAML_FILE_EXTENSION
from tests.test_merge_files.utils import create_directory_structure


@parametrize_programming_language
@pytest.mark.parametrize("output_absolute_file_path", {False, True})
@pytest.mark.parametrize("output_preserve_blank_lines", {False, True})
@pytest.mark.parametrize("num_nested_dirs", range(3))
@pytest.mark.parametrize("jsonl_present", {False, True})
@pytest.mark.parametrize("txt_present", {False, True})
@pytest.mark.parametrize("yaml_present", {False, True})
async def test_merge(
    tmp_test_dir_path: Path,
    resources_dir_path: Path,
    programming_language: ProgrammingLanguage,
    output_absolute_file_path: bool,
    output_preserve_blank_lines: bool,
    num_nested_dirs: int,
    jsonl_present: bool,
    txt_present: bool,
    yaml_present: bool,
):
    extra_extensions = set()
    if jsonl_present:
        extra_extensions.add(JSONL_FILE_EXTENSION)
    if txt_present:
        extra_extensions.add(TXT_FILE_EXTENSION)
    if yaml_present:
        extra_extensions.add(YAML_FILE_EXTENSION)
    output_chunk_beginning_template = "# BEGIN {file_path}"
    output_chunk_end_template = "# END {file_path}"
    paths_to_files_with_expected_contents = create_directory_structure(
        tmp_test_dir_path,
        resources_dir_path,
        programming_language,
        output_absolute_file_path,
        extra_extensions,
        num_nested_dirs,
        remove_blank_lines=not output_preserve_blank_lines,
    )

    merged_file_contents = await merge(
        programming_language,
        tmp_test_dir_path,
        extra_extensions,
        output_absolute_file_path,
        output_chunk_beginning_template,
        output_chunk_end_template,
        output_preserve_blank_lines,
    )

    for path_to_file_with_expected_contents in paths_to_files_with_expected_contents:
        async with aiofiles.open(path_to_file_with_expected_contents, "r") as file_with_expected_contents:
            assert await file_with_expected_contents.read() in merged_file_contents
