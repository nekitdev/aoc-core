from __future__ import annotations

from typing import Any, Optional

from aiohttp import ClientError, ClientSession
from attrs import define, field, frozen
from typing_aliases import Headers, Parameters, Payload
from typing_extensions import Self

from aoc.constants import (
    ANSWER,
    BASE_URL,
    DEFAULT_RETRIES,
    EMPTY,
    GET,
    NAME,
    PART,
    POST,
    PYTHON,
    TOKEN_COOKIE_NAME,
)
from aoc.primitives import Key, Part
from aoc.states import State
from aoc.versions import python_version_info, version_info

__all__ = ("HTTPClient", "Route")

KEY = "{route.method} {route.path}"
key = KEY.format


@frozen()
class Route:
    """Represents routes."""

    method: str
    """The HTTP method of the route."""

    path: str
    """The path of the route."""

    @classmethod
    def with_parameters(cls, method: str, path: str, **parameters: Any) -> Self:
        """Constructs a route with `path` formatted using `parameters`.

        Arguments:
            method: The HTTP method of the route.
            path: The path template of the route.
            **parameters: The parameters to format `path` with.

        Returns:
            The route constructed.
        """
        return cls(method, path.format_map(parameters))

    @property
    def key(self) -> str:
        """The key of the route."""
        return key(route=self)


USER_AGENT_LITERAL = "User-Agent"
"""The user agent literal."""

USER_AGENT = f"{NAME}/{version_info} ({PYTHON}/{python_version_info})"
"""The user agent to use.

This is formatted using:

- [`NAME`][aoc.constants.NAME];
- [`version_info`][aoc.versions.version_info];
- [`PYTHON`][aoc.constants.PYTHON];
- [`python_version_info`][versions.meta.python_version_info].
"""

HEADERS = {USER_AGENT_LITERAL: USER_AGENT}
"""The default headers to use."""


@define()
class HTTPClient:
    """Represents HTTP clients interacting with the Advent of Code servers."""

    token: str = field()
    """The token to use."""

    retries: int = field(default=DEFAULT_RETRIES)
    """The amount of retries to use."""

    async def request(
        self,
        method: str,
        path: str,
        payload: Optional[Payload] = None,
        data: Optional[Parameters] = None,
        parameters: Optional[Parameters] = None,
        headers: Optional[Headers] = None,
    ) -> str:
        """Sends requests to the Advent of Code servers.

        This method sends additional data in the request:

        - `cookies`: The [`token`][aoc.http.HTTPClient.token] in the
          [`TOKEN_COOKIE_NAME`][aoc.constants.TOKEN_COOKIE_NAME] cookie.

        - `headers`: The [`HEADERS`][aoc.http.HEADERS].

        Arguments:
            method: The HTTP method to use.
            path: The path to send the request to, relative to [`BASE_URL`][aoc.constants.BASE_URL].
            payload: The payload to send (JSON).
            data: The data to send.
            parameters: The parameters to use.
            headers: The headers to use.

        Returns:
            The response string.

        Raises:
            ClientError: All request attempts failed.
        """
        attempts = self.retries + 1

        error: Optional[ClientError] = None

        session_cookies = {TOKEN_COOKIE_NAME: self.token}
        session_headers = HEADERS
        base_url = BASE_URL

        while attempts:
            try:
                async with ClientSession(
                    base_url=base_url, cookies=session_cookies, headers=session_headers
                ) as session:
                    response = await session.request(
                        method,
                        path,
                        params=parameters,
                        data=data,
                        json=payload,
                        headers=headers,
                    )

                    response.raise_for_status()

            except ClientError as origin:
                error = origin

            else:
                return await response.text()

            attempts -= 1

        if error:
            raise error

        return EMPTY  # pragma: never

    async def request_route(
        self,
        route: Route,
        payload: Optional[Payload] = None,
        data: Optional[Parameters] = None,
        parameters: Optional[Parameters] = None,
        headers: Optional[Headers] = None,
    ) -> str:
        """Sends requests to the Advent of Code servers using routes.

        ```python
        response = await client.request_route(
            route,
            payload=payload,
            data=data,
            parameters=parameters,
            headers=headers,
        )
        ```

        is equivalent to:

        ```python
        response = await client.request(
            route.method,
            route.path,
            payload=payload,
            data=data,
            parameters=parameters,
            headers=headers,
        )
        ```

        See [`request`][aoc.http.HTTPClient.request] for more information.

        Arguments:
            route: The route to send the request to.
            payload: The payload to send (JSON).
            data: The data to send.
            parameters: The parameters to use.
            headers: The headers to use.

        Returns:
            The response string.

        Raises:
            ClientError: All request attempts failed.
        """
        return await self.request(
            route.method,
            route.path,
            payload=payload,
            data=data,
            parameters=parameters,
            headers=headers,
        )

    async def download_data(self, key: Key) -> str:
        """Downloads the data for the problem for the given `key`.

        Arguments:
            key: The key to download the data for.

        Returns:
            The problem data downloaded.

        Raises:
            ClientError: All request attempts failed.
        """
        route = Route.with_parameters(
            GET, "/{year}/day/{day}/input", year=key.year.value, day=key.day.value
        )

        return await self.request_route(route)

    async def submit_answer(self, key: Key, part: Part, answer: Any) -> State:
        """Submits the `answer` for the problem `part` and the given `key`.

        Arguments:
            key: The key of the problem to submit the answer for.
            part: The part of the problem to submit the answer for.
            answer: The answer to submit.

        Returns:
            The state fetched from the response.

        Raises:
            ClientError: All request attempts failed.
        """
        route = Route.with_parameters(
            POST, "/{year}/day/{day}/answer", year=key.year.value, day=key.day.value
        )

        data = {PART: part.value, ANSWER: answer}

        response = await self.request_route(route, data=data)

        return State.match(response)
