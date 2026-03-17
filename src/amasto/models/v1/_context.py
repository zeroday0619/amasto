from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

from ._status import Status

__all__ = ("Context",)


@since("0.6.0")
class Context(BaseModel):
    model_config = ConfigDict(frozen=True)

    ancestors: list[Status]
    descendants: list[Status]
