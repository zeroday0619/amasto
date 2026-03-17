from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import Unsupported, since

__all__ = ("CustomEmoji",)


@since("2.0.0")
class CustomEmoji(BaseModel):
    model_config = ConfigDict(frozen=True)

    shortcode: str
    url: str
    static_url: str
    visible_in_picker: bool
    category: str | None | Unsupported = since("3.0.0")
