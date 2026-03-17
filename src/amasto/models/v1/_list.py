from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from amasto._version import Unsupported, since

__all__ = ("List",)


@since("2.1.0")
class List(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    title: str
    replies_policy: Literal["followed", "list", "none"] | Unsupported = since("3.3.0")
    exclusive: bool | Unsupported = since("4.2.0")
