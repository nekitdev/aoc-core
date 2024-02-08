from pathlib import Path
from typing import Literal

from yarl import URL

__all__ = (
    # paths
    "ROOT",
    "HOME",
    "TOKEN_PATH",
    "DATA_PATH",
    # bounds
    "FIRST_YEAR",
    "FIRST_DAY",
    "LAST_DAY",
    # strings
    "EMPTY",
    "NEW_LINE",
    # timers
    "DEFAULT_ROUNDING",
    # name and python
    "NAME",
    "PYTHON",
    # HTTP methods
    "HEAD",
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    # HTTP client
    "DEFAULT_RETRIES",
    "BASE_URL",
    "TOKEN_COOKIE_NAME",
    # payloads
    "PART",
    "ANSWER",
    # encoding
    "DEFAULT_ENCODING",
    "DEFAULT_ERRORS",
)

# paths

ROOT = Path(__file__).parent
"""The root of the library."""

HOME = Path.home()
"""The user's home directory (`~/`)."""

# tokens

TOKEN_NAME = ".aoc"
"""The name of the token file."""

TOKEN_PATH = HOME / TOKEN_NAME
"""The path to the token file."""

CACHE_NAME = ".cache"
"""The name of the cache directory."""

AOC_NAME = "aoc"
"""The name of the Advent of Code directory."""

DATA_NAME = "data"
"""The name of the data directory."""

DATA_PATH = HOME / CACHE_NAME / AOC_NAME / DATA_NAME
"""The path to the data directory."""

# bounds

FIRST_YEAR: Literal[2015] = 2015
"""The first year of the Advent of Code."""

FIRST_DAY: Literal[1] = 1
"""The first day of the Advent of Code."""
LAST_DAY: Literal[25] = 25
"""The last day of the Advent of Code."""

# strings

EMPTY = str()
"""The empty string."""

NEW_LINE = "\n"
"""The new line character."""

# rounding

DEFAULT_ROUNDING = 5
"""The default rounding for timers."""

# names

NAME = "aoc-core"
"""The name of the library."""

PYTHON = "python"
"""The `python` literal."""

# HTTP methods

HEAD = "HEAD"
"""The `HEAD` HTTP method."""

GET = "GET"
"""The `GET` HTTP method."""

POST = "POST"
"""The `POST` HTTP method."""

PUT = "PUT"
"""The `PUT` HTTP method."""

PATCH = "PATCH"
"""The `PATCH` HTTP method."""

DELETE = "DELETE"
"""The `DELETE` HTTP method."""

CONNECT = "CONNECT"
"""The `CONNECT` HTTP method."""

OPTIONS = "OPTIONS"
"""The `OPTIONS` HTTP method."""

TRACE = "TRACE"
"""The `TRACE` HTTP method."""

# HTTP client-related

TOKEN_COOKIE_NAME = "session"
"""The cookie name to send the token in."""

BASE_URL = URL("https://adventofcode.com/")
"""The Advent of Code base URL."""

DEFAULT_RETRIES = 3
"""The default amount of retries to use."""

# payloads

PART = "level"
"""The part of the problem to solve (for payloads)."""

ANSWER = "answer"
"""The answer to the problem (for payloads)."""

# encodings

DEFAULT_ENCODING = "utf-8"
"""The default encoding to use."""

DEFAULT_ERRORS = "strict"
"""The default error handling of the encoding to use."""
