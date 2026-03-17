from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from amasto._version import Unsupported, since

from ._account import Account

__all__ = ("Report",)


class Report(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    action_taken: bool
    action_taken_at: str | None | Unsupported = since("4.0.0")
    category: (
        Literal["spam", "legal", "violation", "other"] | Unsupported
    ) = since("4.0.0")
    comment: str | Unsupported = since("4.0.0")
    forwarded: bool | Unsupported = since("4.0.0")
    created_at: str | Unsupported = since("4.0.0")
    status_ids: list[str] | None | Unsupported = since("4.0.0")
    rule_ids: list[str] | None | Unsupported = since("4.0.0")
    target_account: Account | Unsupported = since("4.0.0")
