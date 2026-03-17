from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from amasto._version import since

from ._account import Account

__all__ = ("FamiliarFollowers",)


@since("3.5.0")
class FamiliarFollowers(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    accounts: list[Account]
