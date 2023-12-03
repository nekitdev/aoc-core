from pathlib import Path

from aoc.constants import DEFAULT_ENCODING, DEFAULT_ERRORS, NEW_LINE, TOKEN_PATH
from aoc.errors import TokenNotFound

__all__ = ("load_token", "dump_token", "remove_token")


def load_token(
    path: Path = TOKEN_PATH, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
) -> str:
    try:
        return path.read_text(encoding, errors).strip()

    except OSError as origin:
        raise TokenNotFound(path) from origin


def dump_token(
    token: str,
    path: Path = TOKEN_PATH,
    encoding: str = DEFAULT_ENCODING,
    errors: str = DEFAULT_ERRORS,
) -> None:
    path.write_text(token + NEW_LINE, encoding, errors)


def remove_token(path: Path = TOKEN_PATH) -> None:
    path.unlink(missing_ok=True)
