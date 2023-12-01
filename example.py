from typing import Final

from aoc.solutions import Solution

UP: Final = "("
DOWN: Final = ")"

NEVER_REACHED_BASEMENT: Final = "the basement was never reached"


class Year2015Day01(Solution[str, int, int]):
    def parse(self, data: str) -> str:
        return data

    def solve_one(self, input: str) -> int:
        return input.count(UP) - input.count(DOWN)

    def solve_two(self, input: str) -> int:
        up = UP
        down = DOWN

        floor = 0

        for position, character in enumerate(input, 1):  # one-based indexing
            if character == up:
                floor += 1

            if character == down:
                floor -= 1

            if floor < 0:
                return position

        raise ValueError(NEVER_REACHED_BASEMENT)
