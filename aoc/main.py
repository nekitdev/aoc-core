from asyncio import run as run_coroutine
from pathlib import Path
from sys import exit
from typing import TYPE_CHECKING, Tuple

import click
from aiohttp import ClientError
from trogon import tui  # type: ignore
from typing_aliases import DynamicTuple, NormalError
from wraps import Panic

from aoc.constants import DATA_PATH, TOKEN_PATH
from aoc.data import dump_data
from aoc.errors import DataNotFound, TokenNotFound
from aoc.http import HTTPClient
from aoc.primitives import Day, Key, Part, Year
from aoc.runners import Runner
from aoc.solutions import AnyFinalResult, AnyResult
from aoc.time import aoc_today, get_key_for_date
from aoc.tokens import dump_token, load_token, remove_token
from aoc.versions import version_info

ERROR = 1
ALL = -1


@click.group()
@click.help_option("--help", "-h")
@click.version_option(str(version_info), "--version", "-V")
def aoc() -> None:
    pass


if not TYPE_CHECKING:
    UI = "ui"
    UI_HELP = "Open UI."

    aoc = tui(command=UI, help=UI_HELP)(aoc)


INDENT = "    "

ANSWER = "answer: {}"
answer = ANSWER.format

ANSWER_ONE = "answer one: {}"
answer_one = ANSWER_ONE.format

ANSWER_TWO = "answer two: {}"
answer_two = ANSWER_TWO.format

PARSE_TIME = "parse time: {}"
parse_time = PARSE_TIME.format

SOLVE_TIME = "solve time: {}"
solve_time = SOLVE_TIME.format

SOLVE_ONE_TIME = "solve one time: {}"
solve_one_time = SOLVE_ONE_TIME.format

SOLVE_TWO_TIME = "solve two time: {}"
solve_two_time = SOLVE_TWO_TIME.format


def print_result(result: AnyResult, indent: str = INDENT) -> None:
    click.echo(indent + answer_one(result.answer_one))
    click.echo(indent + answer_two(result.answer_two))
    click.echo(indent + parse_time(result.parse_time))
    click.echo(indent + solve_one_time(result.solve_one_time))
    click.echo(indent + solve_two_time(result.solve_two_time))


def print_final_result(final_result: AnyFinalResult, indent: str = INDENT) -> None:
    click.echo(indent + answer(final_result.answer))
    click.echo(indent + parse_time(final_result.parse_time))
    click.echo(indent + solve_time(final_result.solve_time))


PART_ONE = "part one: {}"
part_one = PART_ONE.format

PART_TWO = "part two: {}"
part_two = PART_TWO.format


async def submit_result(
    result: AnyResult, key: Key, client: HTTPClient, indent: str = INDENT
) -> None:
    one = Part.ONE
    two = Part.TWO

    try:
        result_one = await client.submit_answer(key, one, result.answer_one)

    except ClientError:
        click.echo(failed_to_submit(key, one.value), err=True)

    else:
        click.echo(indent + part_one(result_one.message))

    try:
        result_two = await client.submit_answer(key, two, result.answer_two)

    except ClientError:
        click.echo(failed_to_submit(key, two.value), err=True)

    else:
        click.echo(indent + part_two(result_two.message))


async def submit_final_result(
    final_result: AnyFinalResult, key: Key, client: HTTPClient, indent: str = INDENT
) -> None:
    only = Part.ONLY

    try:
        result = await client.submit_answer(key, only, final_result.answer)

    except ClientError:
        click.echo(failed_to_submit(key, only.value), err=True)

    else:
        click.echo(indent + result.message)


RESULT_FOR = "result for `{}`"
result_for = RESULT_FOR.format

FINAL_RESULT_FOR = "final result for `{}`"
final_result_for = FINAL_RESULT_FOR.format

SOLUTION_DATA_NOT_FOUND = "data not found for solution `{}` ({})"
solution_data_not_found = SOLUTION_DATA_NOT_FOUND.format

SOLUTION_ERRORED = "solution `{}` errored ({})"
solution_errored = SOLUTION_ERRORED.format

SOLUTION_PANICKED = "solution `{}` panicked ({})"
solution_panicked = SOLUTION_PANICKED.format


@aoc.command(
    help="Runs the solutions provided in the paths.",
    short_help="Runs the solutions provided in the paths.",
)
@click.help_option("--help", "-h")
@click.option("--submit", "-S", is_flag=True, help="Whether to submit the answers.")
@click.option(
    "--data-path",
    "-D",
    type=Path,
    default=DATA_PATH,
    show_default=True,
    help="The path to the data cache directory.",
)
@click.option(
    "--token-path",
    "-T",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
@click.argument("paths", type=Path, nargs=ALL)
def run(submit: bool, data_path: Path, token_path: Path, paths: DynamicTuple[Path]) -> None:
    if paths:
        runner = Runner()

        if submit:
            token = find_token(token_path)

            client = HTTPClient(token)

    for path in paths:
        try:
            results = runner.run_path(path, data_path)

        except DataNotFound as data_not_found:
            click.echo(solution_data_not_found(path, data_not_found), err=True)

            continue

        except Panic as panic:
            click.echo(solution_panicked(path, panic), err=True)
            continue

        except NormalError as error:
            click.echo(solution_errored(path, error), err=True)
            continue

        for key, result in results.results.items():
            click.echo(result_for(key))

            print_result(result)

            if submit:
                run_coroutine(submit_result(result, key, client))

        for key, final_result in results.final_results.items():
            click.echo(final_result_for(key))

            print_final_result(final_result)

            if submit:
                run_coroutine(submit_final_result(final_result, key, client))


NO_PROBLEM = "no problem"
PROBLEM = "problem `{}`"
DATE = "{} ({})"


@aoc.group(
    short_help="Provide utilities for the current Advent of Code day.",
    help="Provide utilities for the current Advent of Code day.",
)
@click.help_option("--help", "-h")
def today() -> None:
    pass


@today.command(
    short_help="Show the current date in the Advent of Code timezone.",
    help=(
        "Show the current date in the Advent of Code timezone along with the current problem "
        "(if the Advent of Code is running)."
    ),
)
@click.help_option("--help", "-h")
def show() -> None:
    today = aoc_today()

    try:
        key = get_key_for_date(today)

    except ValueError:
        problem = NO_PROBLEM

    else:
        problem = PROBLEM.format(key)

    today_string = today.to_date_string()

    click.echo(DATE.format(today_string, problem))


DOWNLOAD = "download"

NO_CURRENT_PROBLEM = "no current problem"

FAILED_TO_DOWNLOAD_CURRENT = "failed to download the current problem data"


@today.command(
    name=DOWNLOAD,
    short_help="Download the input for the current Advent of Code problem.",
    help=(
        "Download the input for the current Advent fo Code problem "
        "(if the Advent of Code is running)."
    ),
)
@click.help_option("--help", "-h")
@click.option("--save", "-s", is_flag=True, help="Whether to save the data to cache.")
@click.option(
    "--data-path",
    "-D",
    type=Path,
    default=DATA_PATH,
    show_default=True,
    help="The path to the data cache directory.",
)
@click.option(
    "--token-path",
    "-T",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
def download_today(save: bool, data_path: Path, token_path: Path) -> None:
    token = find_token(token_path)

    today = aoc_today()

    try:
        key = get_key_for_date(today)

    except ValueError:
        click.echo(NO_CURRENT_PROBLEM, err=True)

        exit(ERROR)

    client = HTTPClient(token)

    try:
        data = run_coroutine(client.download_data(key))

    except ClientError:
        click.echo(FAILED_TO_DOWNLOAD_CURRENT)

        exit(ERROR)

    if save:
        dump_data(data, key, data_path)

    else:
        click.echo(data)


SUBMIT = "submit"


@today.command(
    name=SUBMIT,
    short_help="Submit the answer for the current Advent of Code problem.",
    help=(
        "Submit the answer for the current Advent fo Code problem "
        "(if the Advent of Code is running)."
    ),
)
@click.help_option("--help", "-h")
@click.option("--part", "-p", type=int, required=True, prompt=True, help="The part of the problem.")
@click.option(
    "--token-path",
    "-T",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
@click.argument("answer", type=str)
def submit_today(part: int, token_path: Path, answer: str) -> None:
    token = find_token(token_path)

    part_enum = get_part(part)

    today = aoc_today()

    try:
        key = get_key_for_date(today)

    except ValueError:
        click.echo(NO_CURRENT_PROBLEM, err=True)

        exit(ERROR)

    client = HTTPClient(token)

    try:
        state = run_coroutine(client.submit_answer(key, part_enum, answer))

    except ClientError as client_error:
        click.echo(client_error, err=True)

        exit(ERROR)

    click.echo(state.message)


@aoc.group(
    short_help="Manage the token used in interactions with the Advent of Code server.",
    help="Manage the token used in interactions with the Advent of Code server.",
)
@click.help_option("--help", "-h")
def token() -> None:
    pass


def find_token(path: Path) -> str:
    try:
        return load_token(path)

    except TokenNotFound as token_not_found:
        click.echo(token_not_found, err=True)

        exit(ERROR)


@token.command(
    short_help="Print the token.",
    help="Print the token (if one is present).",
)
@click.help_option("--help", "-h")
@click.option(
    "--path",
    "-P",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
def print(path: Path) -> None:
    click.echo(find_token(path))


@token.command(
    short_help="Set the token.",
    help="Set the token.",
)
@click.help_option("--help", "-h")
@click.option(
    "--path",
    "-P",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
@click.argument("token", type=str)
def set(token: str, path: Path) -> None:
    dump_token(token, path)


@token.command(
    short_help="Remove the token.",
    help="Remove the token via removing the token file.",
)
@click.help_option("--help", "-h")
@click.option(
    "--path",
    "-P",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
def remove(path: Path) -> None:
    remove_token(path)


def get_key(year_value: int, day_value: int) -> Key:
    try:
        year = Year(year_value)

    except ValueError as invalid_year:
        click.echo(invalid_year, err=True)

        exit(ERROR)

    try:
        day = Day(day_value)

    except ValueError as invalid_day:
        click.echo(invalid_day, err=True)

        exit(ERROR)

    return Key(year, day)


def get_part(part_value: int) -> Part:
    try:
        return Part(part_value)

    except ValueError as invalid_part:
        click.echo(invalid_part, err=True)

        exit(ERROR)


def get_key_part_pair(year_value: int, day_value: int, part_value: int) -> Tuple[Key, Part]:
    return (get_key(year_value, day_value), get_part(part_value))


FAILED_TO_DOWNLOAD = "failed to download data for problem `{}`"
failed_to_download = FAILED_TO_DOWNLOAD.format


@aoc.command(
    short_help="Download the input from the Advent of Code server.",
    help="Download the input from the Advent of Code server.",
)
@click.help_option("--help", "-h")
@click.option("--year", "-y", type=int, required=True, prompt=True, help="The year of the problem.")
@click.option("--day", "-d", type=int, required=True, prompt=True, help="The day of the problem.")
@click.option("--save", "-s", is_flag=True, help="Whether to save the data to cache.")
@click.option(
    "--data-path",
    "-D",
    type=Path,
    default=DATA_PATH,
    show_default=True,
    help="The path to the data cache directory.",
)
@click.option(
    "--token-path",
    "-T",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
def download(year: int, day: int, save: bool, data_path: Path, token_path: Path) -> None:
    token = find_token(token_path)

    key = get_key(year, day)

    client = HTTPClient(token)

    try:
        data = run_coroutine(client.download_data(key))

    except ClientError:
        click.echo(failed_to_download(key), err=True)

        exit(ERROR)

    if save:
        dump_data(data, key, data_path)

    else:
        click.echo(data)


FAILED_TO_SUBMIT = "failed to submit the answer for problem `{}` part `{}`"
failed_to_submit = FAILED_TO_SUBMIT.format


@aoc.command(
    short_help="Submit the answer to the Advent of Code server.",
    help="Submit the answer to the Advent of Code server.",
)
@click.help_option("--help", "-h")
@click.option("--year", "-y", type=int, required=True, prompt=True, help="The year of the problem.")
@click.option("--day", "-d", type=int, required=True, prompt=True, help="The day of the problem.")
@click.option("--part", "-p", type=int, required=True, prompt=True, help="The part of the problem.")
@click.option(
    "--token-path",
    "-T",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
@click.argument("answer", type=str)
def submit(year: int, day: int, part: int, token_path: Path, answer: str) -> None:
    token = find_token(token_path)

    key, part_enum = get_key_part_pair(year, day, part)

    client = HTTPClient(token)

    try:
        state = run_coroutine(client.submit_answer(key, part_enum, answer))

    except ClientError:
        click.echo(failed_to_submit(key, part_enum.value), err=True)

        exit(ERROR)

    click.echo(state.message)
