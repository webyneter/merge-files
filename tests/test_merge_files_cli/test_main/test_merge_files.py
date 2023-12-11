from asyncio import AbstractEventLoop
from pathlib import Path

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from merge_files_cli.__main__ import merge_files
from tests.conftest import parametrize_programming_language


@parametrize_programming_language
@pytest.mark.parametrize("output_relative_file_path", {False, True})
def test_merge_files(
    mocker: MockerFixture,
    event_loop: AbstractEventLoop,
    programming_language,
    output_relative_file_path: bool,
    cli_runner: CliRunner,
    tmp_test_dir_path: Path,
):
    output_chunk_beginning_template = "### BEGINNING"
    output_chunk_end_template = "### END"
    mock_merge = mocker.patch("merge_files_cli.__main__.merge")
    output_content = f"""{output_chunk_beginning_template}
merged content
{output_chunk_end_template}
"""
    mock_merge.return_value = output_content

    result = cli_runner.invoke(
        merge_files,
        [
            programming_language,
            str(tmp_test_dir_path),
            "--include-extension",
            ".json",
            "--output-chunk-beginning-template",
            output_chunk_beginning_template,
            "--output-chunk-end-template",
            output_chunk_end_template,
        ]
        + (["--output-relative-file-path"] if output_relative_file_path else []),
    )

    print(mock_merge.mock_calls)
    mock_merge.assert_called_once_with(
        programming_language.value,
        tmp_test_dir_path,
        {".json"},
        output_relative_file_path,
        output_chunk_beginning_template,
        output_chunk_end_template,
    )
    assert result.exit_code == 0
    output_file_path = tmp_test_dir_path / f"merged.{tmp_test_dir_path.name}.txt"
    assert output_file_path.read_text() == output_content


@pytest.mark.parametrize("output_relative_file_path", {False, True})
def test_merge_files_raises_given_unsupported_programming_language(
    cli_runner: CliRunner,
    tmp_test_dir_path: Path,
    output_relative_file_path: bool,
):
    """
    Test that merge_files raises an exception when given an unsupported programming language.
    """
    result = cli_runner.invoke(
        merge_files,
        [
            "brainfuck",
            str(tmp_test_dir_path),
            "--include-extension",
            *(".json",),
            "--output-chunk-beginning-template",
            "### BEGINNING",
            "--output-chunk-end-template",
            "### END",
        ]
        + (["--output-relative-file-path"] if output_relative_file_path else []),
    )

    assert isinstance(result.exception, SystemExit)
    assert "brainfuck is not supported" in str(result.output)
    assert result.exit_code != 0
