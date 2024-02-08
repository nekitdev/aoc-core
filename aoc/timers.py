from time import perf_counter_ns as default_clock
from typing import Final, final

from attrs import field, frozen
from typing_aliases import Nullary
from typing_extensions import Self

from aoc.constants import DEFAULT_ROUNDING

__all__ = ("Elapsed", "Clock", "Timer", "now")

FACTORS: Final = (("s", 1_000_000_000), ("ms", 1_000_000), ("us", 1_000), ("ns", 1))
INSTANT: Final = "instant"

Clock = Nullary[int]
"""The type representing clocks which return time in nanoseconds."""


@final
@frozen()
class Elapsed:
    """Represents elapsed time, in nanoseconds and human-readable format."""

    nanoseconds: int = field()
    """The time elapsed, in nanoseconds."""

    rounding: int = field(default=DEFAULT_ROUNDING)
    """The rounding to use when converting to human-readable format."""

    string: str = field(init=False)
    """The time elapsed, in human-readable format."""

    @string.default
    def default_string(self) -> str:
        nanoseconds = self.nanoseconds

        for name, factor in FACTORS:
            if nanoseconds > factor:
                return str(round(nanoseconds / factor, self.rounding)) + name

        return INSTANT

    def __str__(self) -> str:
        return self.string


@final
@frozen()
class Timer:
    """Represents timers."""

    clock: Clock = field(default=default_clock)
    """The clock to use."""

    created: int = field(init=False)
    """The creation time of the timer."""

    @created.default
    def default_created(self) -> int:
        return self.clock()

    def elapsed(self, rounding: int = DEFAULT_ROUNDING) -> Elapsed:
        """Returns the time elapsed since the creation of this timer.

        Returns:
            The time elapsed since the creation of this timer.
        """
        return Elapsed(self.clock() - self.created, rounding)

    def reset(self) -> Self:
        """Creates and returns a new timer of the same type with the same clock.

        Returns:
            The timer created.
        """
        return type(self)(self.clock)


def now(clock: Clock = default_clock) -> Timer:
    """Creates a new timer with the given (or default) clock.

    Arguments:
        clock: The clock to use.

    Returns:
        The timer created.
    """
    return Timer(clock)
