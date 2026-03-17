from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

__all__ = ("PrivacyPolicy",)


@since("4.0.0")
class PrivacyPolicy(BaseModel):
    model_config = ConfigDict(frozen=True)

    updated_at: str
    content: str
