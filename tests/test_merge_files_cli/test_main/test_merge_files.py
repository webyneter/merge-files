import importlib.metadata
from asyncio import AbstractEventLoop
from collections.abc import Sequence
from os import linesep
from pathlib import Path

from click.testing import CliRunner
from pytest_mock import MockerFixture

from merge_files.programming_languages import ProgrammingLanguage
from merge_files_cli.__main__ import merge_files
from tests.conftest import parametrize_programming_language
from tests.test_merge_files_cli.conftest import parametrize_directory_paths
from tests.test_merge_files_cli.conftest import parametrize_output_absolute_file_path


def test_version(cli_runner: CliRunner):
    """
    Test that merge_files prints the correct version.
    """
    result = cli_runner.invoke(merge_files, ["--version"])

    assert result.exit_code == 0
    assert result.output.startswith(f"merge-files, version {importlib.metadata.version('merge-files')}")


@parametrize_output_absolute_file_path
@parametrize_directory_paths
@parametrize_programming_language
def test_merge_files(
    mocker: MockerFixture,
    event_loop: AbstractEventLoop,
    cli_runner: CliRunner,
    tmp_test_dir_path: Path,
    programming_language,
    directory_paths: Sequence[Path],
    expected_common_dir_path: Path,
    output_absolute_file_path: bool,
):
    """
    Test that merge_files merges files correctly.
    """
    tmp_directory_paths = {tmp_test_dir_path / dp for dp in directory_paths}
    for tmp_directory_path in tmp_directory_paths:
        tmp_directory_path.mkdir(parents=True, exist_ok=True)
    tmp_expected_common_dir_path = tmp_test_dir_path / expected_common_dir_path
    output_chunk_beginning_template = "### BEGINNING"
    output_chunk_end_template = "### END"
    mock_merge = mocker.patch("merge_files_cli.__main__.merge")
    mock_merge_output = f"""{output_chunk_beginning_template}
merged content
{output_chunk_end_template}"""
    mock_merge.return_value = mock_merge_output

    result = cli_runner.invoke(
        merge_files,
        [
            programming_language,
            *(str(dp) for dp in tmp_directory_paths),
            "--include-extension",
            ".json",
            "--output-chunk-beginning-template",
            output_chunk_beginning_template,
            "--output-chunk-end-template",
            output_chunk_end_template,
        ]
        + (["--output-absolute-file-path"] if output_absolute_file_path else []),
    )

    for tmp_directory_path in tmp_directory_paths:
        mock_merge.assert_any_call(
            programming_language.value,
            tmp_directory_path,
            {".json"},
            output_absolute_file_path,
            output_chunk_beginning_template,
            output_chunk_end_template,
        )
    assert result.exit_code == 0
    output_file_path = tmp_expected_common_dir_path / "merged.txt"
    assert output_file_path.read_text() == linesep.join([mock_merge_output] * len(directory_paths))


def test_merge_files_raises_given_unsupported_programming_language(
    cli_runner: CliRunner,
    tmp_test_dir_path: Path,
):
    """
    Test that merge_files raises given an unsupported programming language.
    """
    result = cli_runner.invoke(
        merge_files,
        [
            "nobody-would-name-pl-like-that",
            str(tmp_test_dir_path),
        ],
    )

    assert result.exit_code != 0
    assert isinstance(result.exception, SystemExit)
    assert "nobody-would-name-pl-like-that is not supported" in str(result.output)


@parametrize_programming_language
def test_merge_files_raises_given_no_directory_paths(
    cli_runner: CliRunner,
    programming_language: ProgrammingLanguage,
):
    """
    Test that merge_files raises given no directory paths.
    """
    result = cli_runner.invoke(
        merge_files,
        [
            programming_language,
        ],
    )

    assert result.exit_code != 0
    assert isinstance(result.exception, SystemExit)
    assert "At least one directory path must be specified" in str(result.output)
