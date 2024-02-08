"""Commonly used constants."""

from typing import Literal

__all__ = (
    # integers
    "ZERO",
    "ONE",
    "NEGATIVE_ONE",
    # strings
    "EMPTY",
    "NEW_LINE",
    "DOUBLE_NEW_LINE",
)

ZERO: Literal[0] = 0
"""Zero (`0`) literal."""
ONE: Literal[1] = 1
"""One (`1`) literal."""
NEGATIVE_ONE: Literal[-1] = -1
"""Negative one (`-1`) literal."""

EMPTY = str()
"""The empty string."""

NEW_LINE = "\n"
"""One new line character."""

DOUBLE_NEW_LINE = NEW_LINE + NEW_LINE
"""Two new line characters."""
