from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

__all__ = ("StatusSource",)


@since("3.5.0")
class StatusSource(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    text: str
    spoiler_text: str
