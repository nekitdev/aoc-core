from pathlib import Path
from runpy import run_path as run_python_path
from typing import Dict, Type, final

from attrs import frozen

from aoc.constants import DATA_PATH
from aoc.data import load_data
from aoc.names import get_key_by_name
from aoc.primitives import Key
from aoc.solutions import FINAL_SOLUTIONS, SOLUTIONS, AnyFinalResult, AnyResult

__all__ = ("Results", "Runner", "run_path")


@final
@frozen()
class Results:
    """Represents the results of running modules."""

    results: Dict[Key, AnyResult]
    """The results of running [`Solution`][aoc.solutions.Solution] instances."""

    final_results: Dict[Key, AnyFinalResult]
    """The results of running [`FinalSolution`][aoc.solutions.FinalSolution] instances."""


# TODO: here


@frozen()
class Runner:
    """Represents runners for python paths containing modules."""

    def run_path(self, path: Path, data_path: Path = DATA_PATH) -> Results:
        """Runs the module from the `path` and returns the results.

        Arguments:
            path: The path to the module.
            data_path: The path to the data directory.

        Returns:
            The results of running the module.

        Raises:
            AnyError: Any error that occurs while running.
        """
        namespace = run_python_path(str(path))

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


def run_path(
    path: Path, data_path: Path = DATA_PATH, runner_type: Type[Runner] = Runner
) -> Results:
    """Runs the module with the given `name` and returns the results.

    This is equivalent to:

    ```python
    runner_type().run_path(path, data_path)
    ```

    Arguments:
        path: The path to the module.
        data_path: The path to the data directory.
        runner_type: The runner type to use.

    Returns:
        The results of running the module.

    Raises:
        AnyError: Any error that occurs while running.
    """
    return runner_type().run_path(path, data_path)
