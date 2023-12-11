from enum import UNIQUE
from enum import StrEnum
from enum import verify


@verify(UNIQUE)
class ProgrammingLanguage(StrEnum):
    """
    An enumeration of programming languages.
    """

    PYTHON = "python"
