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
HOME = Path.home()

# tokens

TOKEN_NAME = ".aoc"
TOKEN_PATH = HOME / TOKEN_NAME

CACHE_NAME = ".cache"
AOC_NAME = "aoc"
DATA_NAME = "data"

DATA_PATH = HOME / CACHE_NAME / AOC_NAME / DATA_NAME

# bounds

FIRST_YEAR: Literal[2015] = 2015

FIRST_DAY: Literal[1] = 1
LAST_DAY: Literal[25] = 25

# strings

EMPTY = str()

NEW_LINE = "\n"

# rounding

DEFAULT_ROUNDING = 5

# names

NAME = "aoc.py"
PYTHON = "python"

# HTTP methods

HEAD = "HEAD"
GET = "GET"

POST = "POST"
PUT = "PUT"
PATCH = "PATCH"

DELETE = "DELETE"

CONNECT = "CONNECT"
OPTIONS = "OPTIONS"
TRACE = "TRACE"

# HTTP client-related

TOKEN_COOKIE_NAME = "session"

BASE_URL = URL("https://adventofcode.com/")

DEFAULT_RETRIES = 3

# payloads

PART = "level"

ANSWER = "answer"

# encodings

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"
