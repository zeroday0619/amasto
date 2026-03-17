from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

from ._account import Account
from ._status import Status

__all__ = ("Conversation",)


@since("2.6.0")
class Conversation(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    unread: bool
    accounts: list[Account]
    last_status: Status | None
