from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

__all__ = ("ExtendedDescription",)


@since("4.0.0")
class ExtendedDescription(BaseModel):
    model_config = ConfigDict(frozen=True)

    updated_at: str
    content: str
