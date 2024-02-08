from typing import List

from typing_aliases import Parse

from aoc.ext.constants import DOUBLE_NEW_LINE, NEW_LINE

__all__ = (
    "Split",
    "split_at",
    "split_lines",
    "split_double_lines",
    "split_whitespace",
)

Split = Parse[List[str]]
"""Represents split functions."""


def split_at(separator: str) -> Split:
    """Creates `split` functions that split the `string` by `separator`.

    Arguments:
        separator: The separator to split the string by.

    Returns:
        The `split` function created.
    """

    def split(string: str) -> List[str]:
        return string.split(separator)

    return split


split_lines = split_at(NEW_LINE)
"""Splits the `string` by [`NEW_LINE`][aoc.ext.constants.NEW_LINE]."""

split_double_lines = split_at(DOUBLE_NEW_LINE)
"""Splits the `string` by [`DOUBLE_NEW_LINE`][aoc.ext.constants.DOUBLE_NEW_LINE]."""


def split_whitespace(string: str) -> List[str]:
    """Splits the `string` by whitespace.

    This is equivalent to:

    ```python
    string.split()
    ```

    Arguments:
        string: The string to split.

    Returns:
        The split result.
    """
    return string.split()
