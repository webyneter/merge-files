from pathlib import Path
from typing import AbstractSet

from merge_files.constants import PROGRAMMING_LANGUAGE_TO_FILE_EXTENSION
from merge_files.programming_languages import ProgrammingLanguage


def create_directory_structure(
    root_dir_path: Path,
    resources_dir_path: Path,
    programming_language: ProgrammingLanguage,
    output_absolute_file_path: bool,
    extra_extensions: AbstractSet[str],
    num_nested_dirs: int,
) -> AbstractSet[Path]:
    pl_file_extensions = PROGRAMMING_LANGUAGE_TO_FILE_EXTENSION[programming_language]
    file_extensions = extra_extensions | pl_file_extensions

    file_paths = set()

    file_paths |= _create_files_in_directory(
        root_dir_path,
        resources_dir_path,
        file_extensions,
        output_absolute_file_path,
    )

    nested_dir_path = root_dir_path
    for depth in range(1, num_nested_dirs + 1):
        nested_dir_path = nested_dir_path / f"subdir_depth_{depth}"
        nested_dir_path.mkdir()

        file_paths |= _create_files_in_directory(
            nested_dir_path,
            resources_dir_path,
            file_extensions,
            output_absolute_file_path,
        )

    return file_paths


def _create_files_in_directory(
    dir_path: Path,
    resources_dir_path: Path,
    file_extensions: AbstractSet[str],
    output_absolute_file_path: bool,
) -> AbstractSet[Path]:
    file_paths = set()

    for file_extension in file_extensions:
        file_path = dir_path / f"file{file_extension}"
        file_paths.add(file_path)
        file_path.touch()

        tpl_file_path = resources_dir_path / f"tpl.file{file_extension}"
        tpl_file_contents = tpl_file_path.read_text()
        file_contents = (
            tpl_file_contents.replace(
                "{file_path}",
                str(file_path.relative_to(dir_path))
                if output_absolute_file_path
                else str(file_path),
            )
            .replace("{name_1}", "John")
            .replace("{age_1}", "30")
            .replace("{city_1}", "New York")
            .replace("{name_2}", "Jane")
            .replace("{age_2}", "25")
            .replace("{city_2}", "Los Angeles")
        )
        file_path.write_text(file_contents)

    return file_paths
