from typing import List
from typing_aliases import Unary

from aoc.ext.constants import DOUBLE_NEW_LINE, NEW_LINE

__all__ = (
    "SplitResult",
    "Split",
    "split_at",
    "split_lines",
    "split_double_lines",
    "split_whitespace",
)

SplitResult = List[str]

Split = Unary[str, SplitResult]


def split_at(separator: str) -> Split:
    def split(string: str) -> SplitResult:
        return string.split(separator)

    return split


split_lines = split_at(NEW_LINE)
split_double_lines = split_at(DOUBLE_NEW_LINE)

split_whitespace = str.split
