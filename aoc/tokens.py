from pathlib import Path

from aoc.constants import DEFAULT_ENCODING, DEFAULT_ERRORS, NEW_LINE, TOKEN_PATH
from aoc.errors import TokenNotFound

__all__ = ("load_token", "dump_token", "remove_token")


def load_token(
    path: Path = TOKEN_PATH, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
) -> str:
    """Loads the token from the given `path`.

    Arguments:
        path: The path to the token file.
        encoding: The encoding to use.
        errors: The error handling of the encoding to use.

    Returns:
        The loaded token.

    Raises:
        TokenNotFound: [`OSError`][OSError] occured."""
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
    """Dumps the `token` to the given `path`.

    Arguments:
        token: The token to dump.
        path: The path to the token file.
        encoding: The encoding to use.
        errors: The error handling of the encoding to use.
    """
    path.write_text(token + NEW_LINE, encoding, errors)


def remove_token(path: Path = TOKEN_PATH) -> None:
    """Removes the token at the given `path`.

    This function does nothing if the `path` does not exist.

    Arguments:
        path: The path to the token file.
    """
    path.unlink(missing_ok=True)
