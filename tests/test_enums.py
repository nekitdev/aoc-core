import pytest

from aoc.states import (
    CORRECT_MESSAGE,
    HIGH_MESSAGE,
    LOW_MESSAGE,
    SOLVED_MESSAGE,
    TIMEOUT_MESSAGE,
    UNKNOWN_MESSAGE,
    WRONG_MESSAGE,
    State,
)

CORRECT = "That's the right answer!"
SOLVED = "Did you already complete it?"
LOW = "Your answer is too low."
HIGH = "Your answer is too high."
WRONG = "That's not the right answer."
TIMEOUT = "You gave an answer too recently."

UNKNOWN = "This string should never be matched."


@pytest.mark.parametrize(
    ("string", "message"),
    (
        (CORRECT, CORRECT_MESSAGE),
        (SOLVED, SOLVED_MESSAGE),
        (LOW, LOW_MESSAGE),
        (HIGH, HIGH_MESSAGE),
        (WRONG, WRONG_MESSAGE),
        (TIMEOUT, TIMEOUT_MESSAGE),
        (UNKNOWN, UNKNOWN_MESSAGE),
    ),
)
def test_match_message(string: str, message: str) -> None:
    assert State.match(string).message == message
