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
) -> str:
    """
    Merge files in a directory into a single string.
    """
    file_extensions = (
        PROGRAMMING_LANGUAGE_TO_FILE_EXTENSION[programming_language]
        | extra_file_extensions
    )

    merged_file_contents = []
    for file_extension in file_extensions:
        for absolute_file_path in dir_path.rglob(f"*{file_extension}"):
            if not absolute_file_path.is_file():
                continue
            async with aiofiles.open(absolute_file_path, "r") as file:
                file_path = (
                    absolute_file_path
                    if output_absolute_file_path
                    else absolute_file_path.relative_to(dir_path)
                )
                merged_file_contents.append(
                    output_chunk_beginning_template.format(file_path=file_path)
                )
                merged_file_contents.append(await file.read())
                merged_file_contents.append(
                    output_chunk_end_template.format(file_path=file_path)
                )

    return linesep.join(merged_file_contents)
