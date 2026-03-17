from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

__all__ = ("Filter",)


@since("2.4.3")
class Filter(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    phrase: str
    context: list[str]
    expires_at: str | None
    irreversible: bool
    whole_word: bool
