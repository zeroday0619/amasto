from __future__ import annotations

from typing import TypedDict

__all__ = ("PaginationParams",)


class PaginationParams(TypedDict, total=False):
    """Pagination parameters shared by many list endpoints."""

    max_id: str
    since_id: str
    min_id: str
    limit: int
