from pathlib import Path

from aoc.constants import DATA_PATH, DEFAULT_ENCODING, DEFAULT_ERRORS
from aoc.primitives import Key


def get_path_for_key(key: Key, data_path: Path = DATA_PATH) -> Path:
    return data_path / str(key.year) / str(key.day)


def load_data(
    key: Key,
    data_path: Path = DATA_PATH,
    encoding: str = DEFAULT_ENCODING,
    errors: str = DEFAULT_ERRORS,
) -> str:
    return get_path_for_key(key, data_path).read_text(encoding, errors)


def dump_data(
    data: str,
    key: Key,
    data_path: Path = DATA_PATH,
    encoding: str = DEFAULT_ENCODING,
    errors: str = DEFAULT_ERRORS,
) -> None:
    path = get_path_for_key(key, data_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(data, encoding, errors)
