from __future__ import annotations

from ..._endpoint import Endpoint
from ...models.v1 import MediaAttachment

__all__ = ("post_media",)

post_media = Endpoint("POST", "/api/v2/media", MediaAttachment, requires="3.2.0")
