from __future__ import annotations

from enum import Enum, auto

from typing_extensions import assert_never

__all__ = ("State",)

CORRECT_MATCH = "that's the right answer"
SOLVED_MATCH = "did you already complete it"
LOW_MATCH = "your answer is too low"
HIGH_MATCH = "your answer is too high"
WRONG_MATCH = "that's not the right answer"
TIMEOUT_MATCH = "you gave an answer too recently"

CORRECT_MESSAGE = "the answer is correct"
SOLVED_MESSAGE = "the problem part was already solved"
LOW_MESSAGE = "the answer is too low"
HIGH_MESSAGE = "the answer is too high"
WRONG_MESSAGE = "the answer is wrong"
TIMEOUT_MESSAGE = "the answer was submitted too recently"
UNKNOWN_MESSAGE = "the answer state is unknown"

case_fold = str.casefold


class State(Enum):
    """Represents the state of answers."""

    CORRECT = auto()
    """The answer is correct."""

    SOLVED = auto()
    """The problem part was already solved."""

    LOW = auto()
    """The answer is too low."""

    HIGH = auto()
    """The answer is too high."""

    WRONG = auto()
    """The answer is wrong."""

    TIMEOUT = auto()
    """The answer was submitted too recently (timeout)."""

    UNKNOWN = auto()
    """The answer state is unknown."""

    @classmethod
    def match(cls, string: str) -> State:
        """Matches the given `string` and returns the corresponding state.

        Arguments:
            string: The string to match.

        Returns:
            The corresponding state ([`UNKNOWN`][aoc.states.State.UNKNOWN] if no match is found).
        """
        string = case_fold(string)

        if CORRECT_MATCH in string:
            return cls.CORRECT

        if SOLVED_MATCH in string:
            return cls.SOLVED

        if LOW_MATCH in string:
            return cls.LOW

        if HIGH_MATCH in string:
            return cls.HIGH

        if WRONG_MATCH in string:
            return cls.WRONG

        if TIMEOUT_MATCH in string:
            return cls.TIMEOUT

        return cls.UNKNOWN

    @property
    def message(self) -> str:
        """Returns the message for this state.

        Returns:
            The message for this state.
        """
        cls = type(self)

        if self is cls.CORRECT:
            return CORRECT_MESSAGE

        if self is cls.SOLVED:
            return SOLVED_MESSAGE

        if self is cls.LOW:
            return LOW_MESSAGE

        if self is cls.HIGH:
            return HIGH_MESSAGE

        if self is cls.WRONG:
            return WRONG_MESSAGE

        if self is cls.TIMEOUT:
            return TIMEOUT_MESSAGE

        if self is cls.UNKNOWN:
            return UNKNOWN_MESSAGE

        assert_never(self)  # pragma: never
