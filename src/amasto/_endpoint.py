from __future__ import annotations

from pydantic import TypeAdapter
import re
from typing import Any, cast

__all__ = ("Endpoint", "EndpointTemplate", "SubscriptableEndpoint")

_PATH_PARAM = re.compile(r"\{[^}]+\}")


def _sub(template: str, value: str) -> str:
    """Substitute the first ``{…}`` placeholder in *template* with *value*."""
    return _PATH_PARAM.sub(lambda _: value, template, count=1)


class Endpoint[T, P = None, B = None]:
    """Typed API endpoint descriptor.

    Bundles an HTTP method, a path, and the response type so that
    ``Amasto.fetch`` can return a fully-typed ``T`` value.

    Type parameters
    ---------------
    T
        The response type (a Pydantic model or ``list[Model]``).
    P : TypedDict | None
        Query parameter shape.  ``None`` (default) means no query params.
    B : TypedDict | None
        JSON body shape.  ``None`` (default) means no body.

    The *params* and *body* keyword arguments exist solely for type
    inference — they are not stored or used at runtime.
    """

    __slots__ = ("_adapter", "method", "path", "requires")

    method: str
    path: str
    requires: str | None

    def __init__(
        self,
        method: str,
        path: str,
        model: type[T],
        /,
        *,
        params: type[P] | None = None,
        body: type[B] | None = None,
        requires: str | None = None,
    ) -> None:
        self.method = method
        self.path = path
        self._adapter: TypeAdapter[T] = TypeAdapter(model)
        self.requires = requires

    def parse(self, data: Any) -> T:  # noqa: ANN401
        """Validate *data* against the endpoint's response type."""
        return self._adapter.validate_python(data)


class EndpointTemplate[T, P = None, B = None]:
    """Endpoint whose path contains a ``{param}`` that must be resolved via ``[key]``.

    ``self[key]`` substitutes the first placeholder and returns a concrete
    :class:`Endpoint`.
    """

    __slots__ = ("_model", "method", "path", "requires")

    method: str
    path: str
    requires: str | None

    def __init__(
        self,
        method: str,
        path: str,
        model: type[T],
        /,
        *,
        params: type[P] | None = None,
        body: type[B] | None = None,
        requires: str | None = None,
    ) -> None:
        self.method = method
        self.path = path
        self._model = model
        self.requires = requires

    def __getitem__(self, key: str) -> Endpoint[T, P, B]:
        return cast(
            "Endpoint[T, P, B]",
            Endpoint(self.method, _sub(self.path, key), self._model, requires=self.requires),
        )


class SubscriptableEndpoint[T_coll, P_coll, B_coll, T_item](Endpoint[T_coll, P_coll, B_coll]):
    """Endpoint usable both as a flat collection and subscripted for a single item.

    The flat form behaves as ``Endpoint[T_coll, P_coll, B_coll]``.
    ``self[key]`` returns ``Endpoint[T_item, None, None]`` with *key*
    substituted into the item path template.
    """

    __slots__ = ("_item_model", "_item_path", "_item_requires")

    def __init__(
        self,
        method: str,
        path: str,
        model: type[T_coll],
        item_path: str,
        item_model: type[T_item],
        /,
        *,
        params: type[P_coll] | None = None,
        body: type[B_coll] | None = None,
        requires: str | None = None,
        item_requires: str | None = None,
    ) -> None:
        super().__init__(method, path, model, params=params, body=body, requires=requires)
        self._item_path = item_path
        self._item_model = item_model
        self._item_requires = item_requires

    def __getitem__(self, key: str) -> Endpoint[T_item, None, None]:
        return Endpoint(self.method, _sub(self._item_path, key), self._item_model, requires=self._item_requires)
