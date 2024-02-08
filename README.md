# `aoc-core`

[![License][License Badge]][License]
[![Version][Version Badge]][Package]
[![Downloads][Downloads Badge]][Package]
[![Discord][Discord Badge]][Discord]

[![Documentation][Documentation Badge]][Documentation]
[![Check][Check Badge]][Actions]
[![Test][Test Badge]][Actions]
[![Coverage][Coverage Badge]][Coverage]

> *Advent of Code in Python.*

## Installing

**Python 3.8 or above is required.**

### pip

Installing the library with `pip` is quite simple:

```console
$ pip install aoc-core
```

Alternatively, the library can be installed from source:

```console
$ git clone https://github.com/nekitdev/aoc-core.git
$ cd aoc-core
$ python -m pip install .
```

### poetry

You can add `aoc-core` as a dependency with the following command:

```console
$ poetry add aoc-core
```

Or by directly specifying it in the configuration like so:

```toml
[tool.poetry.dependencies]
aoc-core = "^0.1.0"
```

Alternatively, you can add it directly from the source:

```toml
[tool.poetry.dependencies.aoc-core]
git = "https://github.com/nekitdev/aoc-core.git"
```

## Extras

`aoc-core` provides an extra `ext`, which installs modules like [`iters`][iters], [`funcs`][funcs]
and [`wraps`][wraps] which can help solving problems in functional style.

## Example

This example assumes `aoc` is installed and in `PATH`.

We will be solving problem the first ever problem of Advent of Code, that is, [`2015-01`][2015-01].

Firstly, we need to make sure we have the token configured:

```console
$ aoc token print
token not found (path `/home/nekit/.aoc`)
```

Note that the token is placed in `~/.aoc` by default.

Heading over to the [Advent of Code][Advent of Code] website, we need to trace the requests
and find the `session` cookie. This is the token we need to add:

```console
$ aoc token set {TOKEN}
```

And now recheck:

```console
$ aoc token print
{TOKEN}
```

Secondly, we need to download the data for the problem:

```console
$ aoc download
Year: 2015
Day: 01
(... lots of brackets ...)
```

And we are met by our input data! In order to run the solutions, we need to save this.

```console
$ aoc download --year 2015 --day 01 --save
```

Or, if you want to be quicker:

```console
$ aoc download -y 2015 -d 01 -s
```

Now we have everything ready to solve the problem!

In order to define solutions, we need to figure out three types to use:

- `I`, the input type that we parse the data into;
- `T`, the answer type for the first part of the problem;
- `U`, the answer type for the second part of the problem.

Since the problem is about navigating the given string and we return integers,
our types will be: `I = str`, `T = int` and possibly `U = int`.

To define the solution, we need to derive from [`Solution`][aoc.solutions.Solution]:

```python
# example.py

from aoc.solutions import Solution


class Year2015Day01(Solution[str, int, int]):
    ...
```

Note the class name, `Year2015Day01`. This is the convention for naming solutions,
and all solutions must have their name in the `YearYYYYDayDD` format.

We also need to define three methods:

- `parse`, which takes the data string and returns `I`;
- `solve_one`, which takes `I` and returns `T`;
- `solve_two`, which takes `I` and returns `U`.

Part one is rather simple, we need to count the occurrences of `(` and `)`,
and subtract the latter from the former:

```python
from typing import Final

from aoc.solutions import Solution

UP: Final = "("
DOWN: Final = ")"


class Year2015Day01(Solution[str, int, int]):
    def parse(self, data: str) -> str:
        return data

    def solve_one(self, input: str) -> int:
        return input.count(UP) - input.count(DOWN)

    def solve_two(self, input: str) -> int:
        return 0
```

Since we don't yet know what part two is about, let's return `0` for now.

Time to run!

```console
$ aoc run example.py
result for `2015-01`
    answer one: {ONE}
    answer two: 0
    parse time: 1.018us
    solve one time: 41.401us
    solve two time: 245.0ns
```

We have our answer for part one, let's submit it!

```console
$ aoc submit --year 2015 --day 01 --part 1 {ONE}
the answer is correct
```

By the way, we can submit the answer directly after running the solution,
using the `--submit (-s)` flag.

Now onto part two! We need to find the first position where the floor is `-1`.

Nothing too difficult, here is the solution for part two included:

```python
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
```

And let's run the solution again:

```console
$ aoc run example.py
result for `2015-01`
    answer one: {ONE}
    answer two: {TWO}
    parse time: 989.0ns
    solve one time: 41.607us
    solve two time: 59.411us
```

We have our answer for part two, let's submit it!

```console
$ aoc submit -y 2015 -d 01 -p 2 {TWO}
the answer is correct
```

And there we go, we have solved the first ever problem in the Advent of Code!

## Documentation

You can find the documentation [here][Documentation].

## Support

If you need support with the library, you can send an [email][Email]
or refer to the official [Discord server][Discord].

## Changelog

You can find the changelog [here][Changelog].

## Security Policy

You can find the Security Policy of `aoc-core` [here][Security].

## Contributing

If you are interested in contributing to `aoc-core`, make sure to take a look at the
[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].

## License

`aoc-core` is licensed under the MIT License terms. See [License][License] for details.

[Email]: mailto:support@nekit.dev

[Discord]: https://nekit.dev/discord

[Actions]: https://github.com/nekitdev/aoc-core/actions

[Changelog]: https://github.com/nekitdev/aoc-core/blob/main/CHANGELOG.md
[Code of Conduct]: https://github.com/nekitdev/aoc-core/blob/main/CODE_OF_CONDUCT.md
[Contributing Guide]: https://github.com/nekitdev/aoc-core/blob/main/CONTRIBUTING.md
[Security]: https://github.com/nekitdev/aoc-core/blob/main/SECURITY.md

[License]: https://github.com/nekitdev/aoc-core/blob/main/LICENSE

[Package]: https://pypi.org/project/aoc-core
[Coverage]: https://codecov.io/gh/nekitdev/aoc-core
[Documentation]: https://nekitdev.github.io/aoc-core

[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2
[License Badge]: https://img.shields.io/pypi/l/aoc-core
[Version Badge]: https://img.shields.io/pypi/v/aoc-core
[Downloads Badge]: https://img.shields.io/pypi/dm/aoc-core

[Documentation Badge]: https://github.com/nekitdev/aoc-core/workflows/docs/badge.svg
[Check Badge]: https://github.com/nekitdev/aoc-core/workflows/check/badge.svg
[Test Badge]: https://github.com/nekitdev/aoc-core/workflows/test/badge.svg
[Coverage Badge]: https://codecov.io/gh/nekitdev/aoc-core/branch/main/graph/badge.svg

[iters]: https://github.com/nekitdev/iters
[funcs]: https://github.com/nekitdev/funcs
[wraps]: https://github.com/nekitdev/wraps

[Advent of Code]: https://adventofcode.com/

[2015-01]: https://adventofcode.com/2015/day/1

[aoc.solutions.Solution]: https://nekitdev.github.io/aoc-core/reference/solutions#aoc.solutions.Solution
