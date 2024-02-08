from pathlib import Path

from aoc.primitives import Key

__all__ = (
    # normal errors
    "TokenNotFound",
    "DataNotFound",
    # internal errors
    "InternalError",
)

TOKEN_NOT_FOUND = "token not found (path `{}`)"
token_not_found = TOKEN_NOT_FOUND.format


class TokenNotFound(RuntimeError):
    """The token was not found."""

    def __init__(self, path: Path) -> None:
        super().__init__(token_not_found(path.as_posix()))

        self._path = path

    @property
    def path(self) -> Path:
        """The token path."""
        return self._path


DATA_NOT_FOUND = "data not found for problem `{}` (path `{}`)"
data_not_found = DATA_NOT_FOUND.format


class DataNotFound(RuntimeError):
    """The data for the problem was not found."""

    def __init__(self, key: Key, path: Path) -> None:
        super().__init__(data_not_found(key, path.as_posix()))

        self._key = key
        self._path = path

    @property
    def key(self) -> Key:
        """The key of the problem."""
        return self._key

    @property
    def path(self) -> Path:
        """The path to the problem's data file."""
        return self._path


class InternalError(RuntimeError):
    """Represents internal errors in the library."""
