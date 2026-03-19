from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v2 import Instance

__all__ = ("get_instance",)

get_instance = Endpoint("GET", "/api/v2/instance", Instance, requires="3.4.0")
