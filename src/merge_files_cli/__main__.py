import asyncio
from pathlib import Path
from typing import Tuple

import click

from merge_files.files import merge
from merge_files.programming_languages import ProgrammingLanguage
from merge_files_cli.utils import log_info
from merge_files_cli.utils import log_success


@click.command()
@click.version_option()
@click.argument(
    "programming-language",
)
@click.argument(
    "directory-path",
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
    "--output-relative-file-path",
    is_flag=True,
    help="Output relative file path instead of absolute file path.",
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
def merge_files(
    programming_language: str,
    directory_path: Path,
    include_extension: Tuple[str, ...],
    output_relative_file_path: bool,
    output_chunk_beginning_template: str,
    output_chunk_end_template: str,
):
    """
    Merge files in a directory into a single file.
    The resulting file will be placed in the same directory, named merged.<directory-name>.txt

    Supported programming languages: python
    """
    log_info(f"Beginning to merge the matching {directory_path} files...")

    programming_languages = [pl for pl in ProgrammingLanguage]
    if programming_language not in programming_languages:
        raise click.BadArgumentUsage(
            f"{programming_language} is not supported. Choose from: {programming_languages}"
        )

    loop = asyncio.get_event_loop()
    output_content = loop.run_until_complete(
        merge(
            programming_language,
            directory_path,
            set(include_extension),
            output_relative_file_path,
            output_chunk_beginning_template,
            output_chunk_end_template,
        )
    )
    loop.close()

    output_file_extension = ".txt"
    output_file_name = f"merged.{directory_path.name}{output_file_extension}"
    output_file_path = directory_path / output_file_name
    with output_file_path.open(mode="w") as output_file:
        output_file.write(output_content)

    log_success(
        f"The matching {directory_path} files were successfully merged into {output_file_path}"
    )


if __name__ == "__main__":
    merge_files()
