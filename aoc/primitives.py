from __future__ import annotations

from enum import Enum
from typing import final

from attrs import Attribute, field, frozen

from aoc.constants import FIRST_DAY, FIRST_YEAR, LAST_DAY

__all__ = ("Year", "Day", "Key", "Part")

EXPECTED_YEAR = f"expected `year >= {FIRST_YEAR}`"

YEAR = "{:04d}"
year = YEAR.format


@final
@frozen()
class Year:
    """The year of the problem (starts from `2015`)."""

    value: int = field()
    """The contained value."""

    @value.validator
    def check_value(self, attribute: Attribute[int], value: int) -> None:
        if value < FIRST_YEAR:
            raise ValueError(EXPECTED_YEAR)

    def __str__(self) -> str:
        return year(self.value)


EXPECTED_DAY = f"expected `{FIRST_DAY} <= day <= {LAST_DAY}`"


DAY = "{:02d}"
day = DAY.format


@final
@frozen()
class Day:
    """The day of the problem (in `[1, 25]` range)."""

    value: int = field()
    """The contained value."""

    @value.validator
    def check_value(self, attribute: Attribute[int], value: int) -> None:
        if value < FIRST_DAY:
            raise ValueError(EXPECTED_DAY)

        if value > LAST_DAY:
            raise ValueError(EXPECTED_DAY)

    def __str__(self) -> str:
        return day(self.value)


KEY = "{}-{}"
key = KEY.format


@final
@frozen()
class Key:
    """The key of the problem.

    This is essentially the `(year, day)` combination of
    [`Year`][aoc.primitives.Year] and [`Day`][aoc.primitives.Day].
    """

    year: Year
    """The year of the problem."""

    day: Day
    """The day of the problem."""

    def __str__(self) -> str:
        return key(self.year, self.day)


class Part(Enum):
    """The part of the problem."""

    ONE = 1
    """Part one of the problem."""

    TWO = 2
    """Part two of the problem."""

    ONLY = ONE
    """The only part of the problem."""
