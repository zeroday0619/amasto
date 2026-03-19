from __future__ import annotations

from ._endpoint import Endpoint
from ._nodeinfo import NodeInfo
from asyncio import Event, Task
import httpx
from semver import Version
from typing import Any, overload


class Amasto:
    __slots__ = (
        "_api_key",
        "_base_url",
        "_http",
        "_initialization_event",
        "_mastodon_version",
    )

    _base_url: str
    _api_key: str
    _mastodon_version: Version | None
    _initialization_event: Event
    _http: httpx.AsyncClient

    def __init__(
        self,
        base_url: str,
        api_key: str,
        /,
        *,
        mastodon_version: Version | None = None,
    ) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._mastodon_version = None
        self._http = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self._initialization_event = Event()
        if mastodon_version is not None:
            self._mastodon_version = mastodon_version
            self._initialization_event.set()
        else:
            Task(self._initialize())

    async def _initialize(
        self,
        /,
    ) -> None:
        if self._initialization_event.is_set():
            return
        nodeinfo = await NodeInfo.fetch(self._base_url)
        if nodeinfo.software.name == "mastodon":
            self._mastodon_version = Version.parse(nodeinfo.software.version)
        self._initialization_event.set()

    # ------------------------------------------------------------------
    # fetch
    # ------------------------------------------------------------------

    @overload
    async def fetch[T, P, B](
        self,
        endpoint: Endpoint[T, P, B],
        /,
        *,
        params: P | None = None,
        body: B | None = None,
        raw: dict[str, Any] | None = None,
    ) -> T: ...

    @overload
    async def fetch(
        self,
        method: str,
        path: str,
        /,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        raw: dict[str, Any] | None = None,
    ) -> Any: ...  # noqa: ANN401

    async def fetch[T, P, B](
        self,
        endpoint_or_method: Endpoint[T, P, B] | str,
        path: str | None = None,
        /,
        *,
        params: P | dict[str, Any] | None = None,
        body: B | dict[str, Any] | None = None,
        raw: dict[str, Any] | None = None,
    ) -> T | Any:
        await self._initialization_event.wait()

        if isinstance(endpoint_or_method, Endpoint):
            method = endpoint_or_method.method
            request_path = endpoint_or_method.path
        else:
            if path is None:
                raise TypeError("path is required when the first argument is a method string")
            method = endpoint_or_method
            request_path = path

        response = await self._http.request(
            method,
            request_path,
            params=params,  # type: ignore[arg-type]
            json=body,
        )
        response.raise_for_status()

        data: Any = response.json()

        if raw is not None and isinstance(data, dict):
            raw.update(data)

        if isinstance(endpoint_or_method, Endpoint):
            return endpoint_or_method.parse(data)
        return data
