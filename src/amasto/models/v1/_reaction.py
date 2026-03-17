from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

__all__ = ("Reaction",)


@since("3.1.0")
class Reaction(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    count: int
    me: bool | None = None
    url: str | None = None
    static_url: str | None = None
