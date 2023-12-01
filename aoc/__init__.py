"""Advent of Code in Python."""

__description__ = "Advent of Code in Python."
__url__ = "https://github.com/nekitdev/aoc.py"

__title__ = "aoc"
__author__ = "nekitdev"
__license__ = "MIT"
__version__ = "0.1.0"

from aoc.errors import InternalError
from aoc.names import get_key_by_name, get_name_by_key
from aoc.primitives import Day, Key, Year
from aoc.solutions import FinalResult, FinalSolution, Result, Solution
from aoc.time import AOC_TIMEZONE, aoc_today, get_key_for_date
from aoc.timers import Clock, Elapsed, Timer, now
from aoc.tokens import dump_token, load_token, remove_token
from aoc.versions import python_version_info, version_info

__all__ = (
    # solutions
    "Result",
    "Solution",
    "FinalResult",
    "FinalSolution",
    # timers
    "Elapsed",
    "Clock",
    "Timer",
    "now",
    # primitives
    "Year",
    "Day",
    "Key",
    # names
    "get_key_by_name",
    "get_name_by_key",
    # tokens
    "load_token",
    "dump_token",
    "remove_token",
    # time
    "AOC_TIMEZONE",
    "aoc_today",
    "get_key_for_date",
    # versions
    "python_version_info",
    "version_info",
    # errors
    "InternalError",
)
