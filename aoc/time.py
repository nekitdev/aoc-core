from pendulum import Date, timezone, today

from aoc.primitives import Day, Key, Year

__all__ = ("AOC_TIMEZONE", "aoc_today", "get_key_for_date")

AOC_TIMEZONE_NAME = "EST"
"""The Advent of Code timezone name."""

AOC_TIMEZONE = timezone(AOC_TIMEZONE_NAME)
"""The Advent of Code timezone."""


def aoc_today() -> Date:
    """Returns the current date in the [`AOC_TIMEZONE`][aoc.time.AOC_TIMEZONE]."""
    return today(AOC_TIMEZONE)


def get_key_for_date(date: Date) -> Key:
    """Returns the key for the given `date`.

    Raises:
        ValueError: The `date` does not represent the Advent of Code day.
    """
    return Key(Year(date.year), Day(date.day))
