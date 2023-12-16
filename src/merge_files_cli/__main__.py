import asyncio
import importlib.metadata
from collections.abc import Iterable
from os import linesep
from os.path import commonpath
from pathlib import Path
from typing import Tuple

import click

from merge_files.files import merge
from merge_files.programming_languages import ProgrammingLanguage
from merge_files_cli.utils import log_info
from merge_files_cli.utils import log_success


@click.command()
@click.version_option(importlib.metadata.version("merge-files"))
@click.argument(
    "programming-language",
)
@click.argument(
    "directory-path",
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
        allow_dash=False,
        path_type=Path,
        executable=False,
    ),
)
@click.option(
    "--include-extension",
    multiple=True,
    help="Process files with that extension as well. "
    "Can be specified multiple times. "
    "All extensions must be prefixed with a dot.",
)
@click.option(
    "--output-absolute-file-path",
    is_flag=True,
    show_default=True,
    default=False,
    help="Output absolute file path instead of relative.",
)
@click.option(
    "--output-chunk-beginning-template",
    default="### BEGINNING OF FILE {file_path}",
    help="The string (template) designating the beginning of a file chunk in the output file.",
)
@click.option(
    "--output-chunk-end-template",
    default="### END OF FILE {file_path}",
    help="The string (template) designating the end of a file chunk in the output file.",
)
@click.option(
    "--output-preserve-blank-lines",
    is_flag=True,
    show_default=True,
    default=False,
    help="Preserve blank lines from original files in the output file.",
)
@click.option(
    "--output-preserve-empty-files",
    is_flag=True,
    show_default=True,
    default=False,
    help="Preserve empty files in the output file.",
)
def merge_files(
    programming_language: str,
    directory_path: Tuple[Path, ...],
    include_extension: Tuple[str, ...],
    output_absolute_file_path: bool,
    output_chunk_beginning_template: str,
    output_chunk_end_template: str,
    output_preserve_blank_lines: bool,
    output_preserve_empty_files: bool,
):
    """
    Merge files in a directory into a single file.
    The resulting file will be placed in the same directory, named merged.txt

    Supported programming languages: python
    """
    programming_languages = [pl for pl in ProgrammingLanguage]
    if programming_language not in programming_languages:
        raise click.BadArgumentUsage(f"{programming_language} is not supported. Choose from: {programming_languages}")

    directory_paths = set(directory_path)
    if not directory_paths:
        raise click.BadArgumentUsage("At least one directory path must be specified.")

    include_extensions = set(include_extension)

    output_file_dir_path = Path(commonpath(directory_paths))  # type: ignore

    tasks = (
        merge(
            programming_language,
            dp,
            include_extensions,
            output_absolute_file_path,
            output_chunk_beginning_template,
            output_chunk_end_template,
            output_preserve_blank_lines,
            output_preserve_empty_files,
            output_relative_to_dir_path=output_file_dir_path,
        )
        for dp in directory_paths
    )

    log_info("Beginning to merge the matching files...")

    loop = asyncio.get_event_loop()
    task_results: Iterable[str] = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    output_file_extension = ".txt"
    output_file_name = f"merged{output_file_extension}"
    output_file_path = output_file_dir_path / output_file_name
    with output_file_path.open(mode="w") as output_file:
        output_file.write(linesep.join(task_results))

    log_success(f"The matching files were successfully merged into {output_file_path}")


if __name__ == "__main__":
    merge_files()
