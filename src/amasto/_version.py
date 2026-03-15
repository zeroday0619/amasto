from __future__ import annotations

from dataclasses import dataclass

from pydantic import GetCoreSchemaHandler
from pydantic.fields import FieldInfo
from pydantic_core import CoreSchema, PydanticCustomError, core_schema


@dataclass(frozen=True, slots=True)
class Since:
    """Metadata marker indicating the version in which a field was introduced."""

    version: str
    """The version string marking when the field was introduced."""


def since(
    version: str,
    /,
) -> FieldInfo:
    """Create a :class:`~pydantic.fields.FieldInfo` that marks a field as available since *version*.

    The returned field defaults to :data:`unsupported`, so models built from
    older payloads can be parsed even when the field is absent.  The supplied
    *version* string is stored as a :class:`Since` instance in the field's
    metadata.

    :param version: The version string in which the field was first introduced.
    :type version: str
    :returns: A :class:`~pydantic.fields.FieldInfo` whose default is :data:`unsupported` and
        whose metadata contains a :class:`Since` entry.
    :rtype: ~pydantic.fields.FieldInfo
    """
    field_info = _SinceFieldInfo(default=unsupported)
    field_info.metadata.append(Since(version))
    return field_info


class Unsupported:
    """Sentinel type representing a field that is not supported in the current version.

    Prefer the module-level :data:`unsupported` singleton over instantiating
    this class directly.
    """

    __slots__ = ()

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type[object], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return a Pydantic core schema that only accepts the :data:`unsupported` sentinel.

        :param source_type: The type being validated.
        :param handler: The Pydantic schema handler.
        :returns: A plain validator schema restricted to :class:`Unsupported` instances.
        :rtype: ~pydantic_core.CoreSchema
        """

        def validate(
            value: object,
            /,
        ) -> Unsupported:
            if type(value) is Unsupported:
                return value
            raise PydanticCustomError(
                "unsupported",
                "Only the sentinel value 'unsupported' is allowed for Unsupported.",
            )

        return core_schema.no_info_plain_validator_function(validate)

    def __init__(
        self,
        /,
    ) -> None:
        """Initialise the :class:`Unsupported` sentinel."""

    def __bool__(
        self,
        /,
    ) -> bool:
        """Return ``False``, allowing sentinel values to be used in boolean checks."""
        return False


unsupported = Unsupported()
"""Module-level singleton of :class:`Unsupported`.

Use this as the default value for fields annotated with :func:`since`
to indicate that the field is not available in older API versions.
"""


class _SinceFieldInfo(FieldInfo):  # ty:ignore[subclass-of-final-class]
    """A :class:`~pydantic.fields.FieldInfo` subclass used internally by :func:`since`."""

    __slots__ = ()

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: type[object],
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Delegate schema generation to the base :class:`~pydantic.fields.FieldInfo`.

        :param source_type: The type being validated.
        :param handler: The Pydantic schema handler.
        :returns: The core schema produced by the base :class:`~pydantic.fields.FieldInfo`.
        :rtype: ~pydantic_core.CoreSchema
        """
        return handler(FieldInfo)

    def __call__(self, cls: type[object], /) -> type[object]:
        """Return *cls* unchanged, making this instance usable as a class decorator.

        :param cls: The class to decorate.
        :returns: *cls* unmodified.
        """
        return cls
