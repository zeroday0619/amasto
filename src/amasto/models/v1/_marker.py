from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

__all__ = ("Marker",)


@since("3.0.0")
class Marker(BaseModel):
    model_config = ConfigDict(frozen=True)

    last_read_id: str
    version: int
    updated_at: str
