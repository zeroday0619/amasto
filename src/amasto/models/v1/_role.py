from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

__all__ = ("Role",)


@since("4.0.0")
class Role(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    color: str
    permissions: str
    highlighted: bool
