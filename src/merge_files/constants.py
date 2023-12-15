from typing import AbstractSet
from typing import Final
from typing import Mapping

from merge_files.programming_languages import ProgrammingLanguage


PROGRAMMING_LANGUAGE_TO_FILE_EXTENSION: Final[Mapping[ProgrammingLanguage, AbstractSet[str]]] = {
    ProgrammingLanguage.PYTHON: {
        ".py",
        ".pyi",
    },
}
