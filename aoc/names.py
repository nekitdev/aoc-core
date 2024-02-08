from re import compile
from typing import Literal

from aoc.errors import InternalError
from aoc.primitives import Day, Key, Year

__all__ = ("get_key_by_name", "get_name_by_key")

YEAR: Literal["year"] = "year"
DAY: Literal["day"] = "day"

NAME_PATTERN = r"^Year(?P<year>[0-9]{4})Day(?P<day>[0-9]{2})$"

NAME = compile(NAME_PATTERN)

NAME_EXAMPLE = "YearYYYYDayDD"
"""The example of the name format."""

INVALID_NAME = f"invalid name `{{}}`; expected `{NAME_EXAMPLE}` format"
invalid_name = INVALID_NAME.format

INVALID_NAME_WITH_REASON = "invalid name `{}` ({})"
invalid_name_with_reason = INVALID_NAME_WITH_REASON.format

NAME_MATCHED_BUT_NO_YEAR = "name matched but the year group is not set"
NAME_MATCHED_BUT_NO_DAY = "name matched but the day group is not set"


def get_key_by_name(name: str) -> Key:
    """Gets the key representing the problem by the name of the solution type.

    Note:
        The `name` must match the format of [`NAME_EXAMPLE`][aoc.names.NAME_EXAMPLE].

    Arguments:
        name: The name of the solution type.

    Returns:
        The key representing the problem.

    Raises:
        TypeError: The `name` does not match the expected format.
        ValueError: The year or the day is not valid.
        InternalError: The pattern was matched but `year` or `day` group is not set.
    """
    match = NAME.match(name)

    if match is None:
        raise TypeError(invalid_name(name))

    year_option = match.group(YEAR)

    if year_option is None:
        raise InternalError  # TODO: message?

    year_value = int(year_option)

    day_option = match.group(DAY)

    if day_option is None:
        raise InternalError  # TODO: message?

    day_value = int(day_option)

    try:
        year = Year(year_value)

    except ValueError as invalid_year:
        raise TypeError(invalid_name_with_reason(name, invalid_year)) from invalid_year

    try:
        day = Day(day_value)

    except ValueError as invalid_day:
        raise TypeError(invalid_name_with_reason(name, invalid_day)) from invalid_day

    return Key(year, day)


NAME_FORMAT = "Year{:04d}Day{:02d}"
create_name = NAME_FORMAT.format


def get_name_by_key(key: Key) -> str:
    """The inverse of [`get_key_by_name`][aoc.names.get_key_by_name].

    Arguments:
        key: The key to create the name for.

    Returns:
        The name created.
    """
    return create_name(key.year.value, key.day.value)
