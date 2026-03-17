from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

from ._account import Account
from ._status import Status

__all__ = ("NotificationRequest",)


@since("4.3.0")
class NotificationRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    created_at: str
    updated_at: str
    account: Account
    notifications_count: str
    last_status: Status | None = None
