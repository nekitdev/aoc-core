from pendulum import Date, timezone, today

from aoc.primitives import Day, Key, Year

__all__ = ("AOC_TIMEZONE", "aoc_today", "get_key_for_date")

AOC_TIMEZONE_NAME = "EST"

AOC_TIMEZONE = timezone(AOC_TIMEZONE_NAME)


def aoc_today() -> Date:
    return today(AOC_TIMEZONE)


def get_key_for_date(date: Date) -> Key:
    return Key(Year(date.year), Day(date.day))
