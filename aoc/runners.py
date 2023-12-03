from pathlib import Path
from runpy import run_module
from typing import Dict, final

from attrs import frozen

from aoc.constants import DATA_PATH
from aoc.data import load_data
from aoc.names import get_key_by_name
from aoc.primitives import Key
from aoc.solutions import FINAL_SOLUTIONS, SOLUTIONS, AnyFinalResult, AnyResult

__all__ = ("Results", "Runner")


@final
@frozen()
class Results:
    results: Dict[Key, AnyResult]
    final_results: Dict[Key, AnyFinalResult]


@final
@frozen()
class Runner:
    def run_module(self, name: str, data_path: Path = DATA_PATH) -> Results:
        namespace = run_module(name)

        solutions = SOLUTIONS
        final_solutions = FINAL_SOLUTIONS

        results = {}
        final_results = {}

        for name in namespace:
            try:
                key = get_key_by_name(name)

            except TypeError:
                pass

            else:
                if key in solutions:
                    solution = solutions[key]()

                    data = load_data(key, data_path)

                    results[key] = solution.execute(data)

                if key in final_solutions:
                    final_solution = final_solutions[key]()

                    data = load_data(key, data_path)

                    final_results[key] = final_solution.execute(data)

        return Results(results, final_results)
