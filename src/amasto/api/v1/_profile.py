from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import CredentialAccount

__all__ = ("profile",)


class _ProfileNamespace:
    __slots__ = ()

    delete_avatar = Endpoint("DELETE", "/api/v1/profile/avatar", CredentialAccount, requires="4.2.0")
    delete_header = Endpoint("DELETE", "/api/v1/profile/header", CredentialAccount, requires="4.2.0")


profile = _ProfileNamespace()
