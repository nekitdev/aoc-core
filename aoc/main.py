from asyncio import run
from pathlib import Path
from sys import exit
from typing import Tuple

import click
from aiohttp import ClientError

from aoc.constants import TOKEN_PATH
from aoc.http import HTTPClient
from aoc.primitives import Day, Key, Part, Year
from aoc.time import aoc_today, get_key_for_date
from aoc.tokens import dump_token, load_token, remove_token
from aoc.versions import version_info

ERROR = 1


@click.group()
@click.help_option("--help", "-h")
@click.version_option(str(version_info), "--version", "-V")
def aoc() -> None:
    pass


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

    today_string = today.to_date_string()  # type: ignore

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
@click.option(
    "--token-path",
    "-t",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
def download_today(token_path: Path) -> None:
    token = find_token(token_path)

    today = aoc_today()

    try:
        key = get_key_for_date(today)

    except ValueError:
        click.echo(NO_CURRENT_PROBLEM, err=True)

        exit(ERROR)

    client = HTTPClient(token)

    try:
        data = run(client.download_data(key))

    except ClientError:
        click.echo(FAILED_TO_DOWNLOAD_CURRENT)

        exit(ERROR)

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
    "-t",
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
        state = run(client.submit_answer(key, part_enum, answer))

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


FAILED_TO_FIND_TOKEN = "failed to find the token (path `{}`)"
failed_to_find_token = FAILED_TO_FIND_TOKEN.format


def find_token(path: Path) -> str:
    try:
        return load_token(path)

    except OSError:
        click.echo(failed_to_find_token(path), err=True)

        exit(ERROR)


@token.command(
    short_help="Print the token.",
    help="Print the token (if one is present).",
)
@click.help_option("--help", "-h")
@click.option(
    "--path",
    "-p",
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
    "-p",
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
    "-p",
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


def get_key_part_pair(
    year_value: int, day_value: int, part_value: int
) -> Tuple[Key, Part]:
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
@click.option(
    "--token-path",
    "-t",
    type=Path,
    default=TOKEN_PATH,
    show_default=True,
    help="The path to the token file.",
)
def download(year: int, day: int, token_path: Path) -> None:
    token = find_token(token_path)

    key = get_key(year, day)

    client = HTTPClient(token)

    try:
        data = run(client.download_data(key))

    except ClientError:
        click.echo(failed_to_download(key), err=True)

        exit(ERROR)

    click.echo(data)


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
    "-t",
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
        state = run(client.submit_answer(key, part_enum, answer))

    except ClientError as client_error:
        click.echo(client_error, err=True)

        exit(ERROR)

    click.echo(state.message)
