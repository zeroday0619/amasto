from __future__ import annotations

from .._endpoint import Endpoint

__all__ = ("get_userinfo",)

get_userinfo: Endpoint[dict, None, None] = Endpoint("GET", "/oauth/userinfo", dict)
