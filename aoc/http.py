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
from aoc.enums import State
from aoc.primitives import Key, Part
from aoc.versions import python_version_info, version_info

__all__ = ("HTTPClient", "Route")

KEY = "{route.method} {route.path}"
key = KEY.format


@frozen()
class Route:
    method: str
    path: str

    @classmethod
    def with_parameters(cls, method: str, path: str, **parameters: Any) -> Self:  # type: ignore
        return cls(method, path.format_map(parameters))

    @property
    def key(self) -> str:
        return key(route=self)


USER_AGENT_LITERAL = "User-Agent"
USER_AGENT = f"{NAME}/{version_info} ({PYTHON}/{python_version_info})"

HEADERS = {USER_AGENT_LITERAL: USER_AGENT}


@define()
class HTTPClient:
    token: str = field()

    retries: int = field(default=DEFAULT_RETRIES)

    async def request(
        self,
        method: str,
        path: str,
        payload: Optional[Payload] = None,
        data: Optional[Parameters] = None,
        parameters: Optional[Parameters] = None,
        headers: Optional[Headers] = None,
    ) -> str:
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
        return await self.request(
            route.method,
            route.path,
            payload=payload,
            data=data,
            parameters=parameters,
            headers=headers,
        )

    async def download_data(self, key: Key) -> str:
        route = Route.with_parameters(
            GET, "/{year}/day/{day}/input", year=key.year.value, day=key.day.value
        )

        return await self.request_route(route)

    async def submit_answer(self, key: Key, part: Part, answer: Any) -> State:
        route = Route.with_parameters(
            POST, "/{year}/day/{day}/answer", year=key.year.value, day=key.day.value
        )

        data = {PART: part.value, ANSWER: answer}

        response = await self.request_route(route, data=data)

        return State.match(response)
