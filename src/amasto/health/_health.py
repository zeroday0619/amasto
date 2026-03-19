from __future__ import annotations

from .._endpoint import Endpoint

__all__ = ("get_health",)

get_health: Endpoint[dict, None, None] = Endpoint("GET", "/health", dict, requires="2.5.0")
