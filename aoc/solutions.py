from __future__ import annotations

from abc import abstractmethod as required
from typing import Any, Dict, Generic, Protocol, Type, TypeVar, final

from attrs import frozen
from named import get_name

from aoc.names import get_key_by_name
from aoc.primitives import Key
from aoc.timers import Elapsed, now

__all__ = ("Result", "Solution", "FinalResult", "FinalSolution")

I = TypeVar("I")  # input
T = TypeVar("T", covariant=True)  # part one (can be the only part)
U = TypeVar("U", covariant=True)  # part two


@final
@frozen()
class Result(Generic[T, U]):
    """Represents the result of the problem solution."""

    answer_one: T
    """The answer to the part one of the problem."""

    answer_two: U
    """The answer to the part two of the problem."""

    parse_time: Elapsed
    """The time it took to parse the data."""

    solve_one_time: Elapsed
    """The time it took to solve part one."""

    solve_two_time: Elapsed
    """The time it took to solve part two."""


AnyResult = Result[Any, Any]

MUST_IMPLEMENT = "solutions must implement the `{}` method"
must_implement = MUST_IMPLEMENT.format

PARSE = "parse"
SOLVE = "solve"
SOLVE_ONE = "solve_one"
SOLVE_TWO = "solve_two"

MUST_IMPLEMENT_PARSE = must_implement(PARSE)
MUST_IMPLEMENT_SOLVE = must_implement(SOLVE)
MUST_IMPLEMENT_SOLVE_ONE = must_implement(SOLVE_ONE)
MUST_IMPLEMENT_SOLVE_TWO = must_implement(SOLVE_TWO)


SOLUTIONS: Dict[Key, AnySolutionType] = {}


class Solution(Protocol[I, T, U]):
    """Represents problem solutions."""

    def __init_subclass__(cls, **keywords: Any) -> None:
        super().__init_subclass__(**keywords)

        SOLUTIONS[get_key_by_name(get_name(cls))] = cls

    @required
    def parse(self, data: str) -> I:
        """Parses the data into the input type.

        Arguments:
            data: The data to parse.

        Returns:
            The input of the problem.
        """
        raise NotImplementedError(MUST_IMPLEMENT_PARSE)

    @required
    def solve_one(self, input: I) -> T:
        """Solves part one of the problem.

        Arguments:
            input: The input of the problem, as returned by [`parse`][aoc.solutions.Solution.parse].

        Returns:
            The answer to part one of the problem.
        """
        raise NotImplementedError(MUST_IMPLEMENT_SOLVE_ONE)

    @required
    def solve_two(self, input: I) -> U:
        """Solves part two of the problem.

        Arguments:
            input: The input of the problem, as returned by [`parse`][aoc.solutions.Solution.parse].

        Returns:
            The answer to part two of the problem.
        """
        raise NotImplementedError(MUST_IMPLEMENT_SOLVE_TWO)

    def execute(self, data: str) -> Result[T, U]:
        """Executes the problem solution on the given data.

        Arguments:
            data: The data to parse and solve the problem for.

        Returns:
            The result of the solution.
        """
        parse = self.parse
        solve_one = self.solve_one
        solve_two = self.solve_two

        timer = now()

        input = parse(data)

        parse_time = timer.elapsed()

        timer = timer.reset()

        answer_one = solve_one(input)

        solve_one_time = timer.elapsed()

        timer = timer.reset()

        answer_two = solve_two(input)

        solve_two_time = timer.elapsed()

        return Result(answer_one, answer_two, parse_time, solve_one_time, solve_two_time)


AnySolution = Solution[Any, Any, Any]
AnySolutionType = Type[AnySolution]


@final
@frozen()
class FinalResult(Generic[T]):
    """Represents the result of the final problem solution."""

    answer: T
    """The answer to the problem."""

    parse_time: Elapsed
    """The time it took to parse the data."""

    solve_time: Elapsed
    """The time it took to solve the problem."""


AnyFinalResult = FinalResult[Any]

FINAL_SOLUTIONS: Dict[Key, AnyFinalSolutionType] = {}


class FinalSolution(Protocol[I, T]):
    """Represents final problem solutions."""

    def __init_subclass__(cls, **keywords: Any) -> None:
        super().__init_subclass__(**keywords)

        FINAL_SOLUTIONS[get_key_by_name(get_name(cls))] = cls

    @required
    def parse(self, data: str) -> I:
        """Parses the data into the input type.

        Arguments:
            data: The data to parse.

        Returns:
            The input of the problem.
        """
        raise NotImplementedError(MUST_IMPLEMENT_PARSE)

    @required
    def solve(self, input: I) -> T:
        """Solves the problem.

        Arguments:
            input: The input of the problem, as returned by
                [`parse`][aoc.solutions.FinalSolution.parse].

        Returns:
            The answer to the problem.
        """
        raise NotImplementedError(MUST_IMPLEMENT_SOLVE)

    def execute(self, data: str) -> FinalResult[T]:
        """Executes the problem solution on the given data.

        Arguments:
            data: The data to parse and solve the problem for.

        Returns:
            The result of the solution.
        """
        parse = self.parse
        solve = self.solve

        timer = now()

        input = parse(data)

        parse_time = timer.elapsed()

        timer = timer.reset()

        answer = solve(input)

        solve_time = timer.elapsed()

        return FinalResult(answer, parse_time, solve_time)


AnyFinalSolution = FinalSolution[Any, Any]
AnyFinalSolutionType = Type[AnyFinalSolution]
