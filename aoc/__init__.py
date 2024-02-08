"""Advent of Code in Python."""

__description__ = "Advent of Code in Python."
__url__ = "https://github.com/nekitdev/aoc-core"

__title__ = "aoc"
__author__ = "nekitdev"
__license__ = "MIT"
__version__ = "0.1.0"

from aoc.data import dump_data, get_path_for_key, load_data
from aoc.errors import DataNotFound, InternalError, TokenNotFound
from aoc.http import HTTPClient, Route
from aoc.names import get_key_by_name, get_name_by_key
from aoc.primitives import Day, Key, Year
from aoc.runners import Results, Runner, run_path
from aoc.solutions import FinalResult, FinalSolution, Result, Solution
from aoc.states import State
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
    # runners
    "Results",
    "Runner",
    "run_path",
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
    # errors
    "TokenNotFound",
    "DataNotFound",
    "InternalError",
    # tokens
    "load_token",
    "dump_token",
    "remove_token",
    # data
    "get_path_for_key",
    "load_data",
    "dump_data",
    # time
    "AOC_TIMEZONE",
    "aoc_today",
    "get_key_for_date",
    # states
    "State",
    # HTTP
    "HTTPClient",
    "Route",
    # versions
    "python_version_info",
    "version_info",
)
