from pathlib import Path

from aoc.constants import DATA_PATH, DEFAULT_ENCODING, DEFAULT_ERRORS
from aoc.errors import DataNotFound
from aoc.primitives import Key

__all__ = ("get_path_for_key", "load_data", "dump_data")


def get_path_for_key(key: Key, data_path: Path = DATA_PATH) -> Path:
    """Gets the path to the file in `data_path` for the given `key`.

    Arguments:
        key: The key to get the path for.
        data_path: The path to the data directory.

    Returns:
        The path to the file in `data_path` for the given `key`.
    """
    return data_path / str(key.year) / str(key.day)


def load_data(
    key: Key,
    data_path: Path = DATA_PATH,
    encoding: str = DEFAULT_ENCODING,
    errors: str = DEFAULT_ERRORS,
) -> str:
    """Loads the data for the given `key`.

    Arguments:
        key: The key to load the data for.
        data_path: The path to the data directory.
        encoding: The encoding to use.
        errors: The error handling of the encoding to use.

    Returns:
        The data for the given `key`.

    Raises:
        DataNotFound: [`OSError`][OSError] occured.
    """
    try:
        return get_path_for_key(key, data_path).read_text(encoding, errors)

    except OSError as origin:
        raise DataNotFound(key, data_path) from origin


def dump_data(
    data: str,
    key: Key,
    data_path: Path = DATA_PATH,
    encoding: str = DEFAULT_ENCODING,
    errors: str = DEFAULT_ERRORS,
) -> None:
    """Dumps the `data` for the given `key`.

    Arguments:
        data: The data to dump.
        key: The key to dump the data for.
        data_path: The path to the data directory.
        encoding: The encoding to use.
        errors: The error handling of the encoding to use.
    """
    path = get_path_for_key(key, data_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(data, encoding, errors)
