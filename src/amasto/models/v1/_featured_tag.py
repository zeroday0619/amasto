from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import Unsupported, since

__all__ = ("FeaturedTag",)


@since("3.0.0")
class FeaturedTag(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    url: str | Unsupported = since("3.3.0")
    statuses_count: int
    last_status_at: str | None
