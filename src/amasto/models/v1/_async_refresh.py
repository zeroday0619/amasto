from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from amasto._version import since

__all__ = ("AsyncRefresh",)


@since("4.4.0")
class AsyncRefresh(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    status: Literal["running", "finished"]
    result_count: int | None
