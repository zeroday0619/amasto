from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ("Error",)


class Error(BaseModel):
    model_config = ConfigDict(frozen=True)

    error: str
    error_description: str | None = None
