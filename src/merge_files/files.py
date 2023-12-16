from os import linesep
from pathlib import Path
from typing import AbstractSet

import aiofiles

from merge_files.constants import PROGRAMMING_LANGUAGE_TO_FILE_EXTENSION
from merge_files.programming_languages import ProgrammingLanguage


async def merge(
    programming_language: ProgrammingLanguage,
    dir_path: Path,
    extra_file_extensions: AbstractSet[str],
    output_absolute_file_path: bool,
    output_chunk_beginning_template: str,
    output_chunk_end_template: str,
    output_preserve_blank_lines: bool,
    output_preserve_empty_files: bool,
    output_relative_to_dir_path: Path | None = None,
) -> str:
    """
    Merge files in a directory into a single string.
    """
    output_relative_to_dir_path = output_relative_to_dir_path or dir_path

    file_extensions = PROGRAMMING_LANGUAGE_TO_FILE_EXTENSION[programming_language] | extra_file_extensions

    merged_file_contents = []
    for file_extension in file_extensions:
        for absolute_file_path in dir_path.rglob(f"*{file_extension}"):
            if not absolute_file_path.is_file():
                continue

            async with aiofiles.open(absolute_file_path, mode="r") as file:
                file_content = await file.read()

                if not output_preserve_blank_lines:
                    non_blank_lines = []
                    for line in file_content.split(linesep):
                        if line.strip():
                            non_blank_lines.append(line)
                    file_content = linesep.join(non_blank_lines)

                if not output_preserve_empty_files and not file_content.strip():
                    # This check comes AFTER every other check that can potentially affect file_content.
                    continue

                absolute_or_relative_file_path = (
                    absolute_file_path
                    if output_absolute_file_path
                    else absolute_file_path.relative_to(output_relative_to_dir_path)
                )
                merged_file_contents.append(
                    output_chunk_beginning_template.format(file_path=absolute_or_relative_file_path)
                )
                merged_file_contents.append(file_content)
                merged_file_contents.append(output_chunk_end_template.format(file_path=absolute_or_relative_file_path))

    return linesep.join(merged_file_contents)
