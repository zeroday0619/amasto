from __future__ import annotations

from pydantic import BaseModel

from amasto._version import Unsupported, since, unsupported


def test_since() -> None:

    @since("0.1.0")
    class Foo(BaseModel):
        foo: str | Unsupported = since("0.1.0")
        bar: str | Unsupported = since("0.2.0")

    foo = Foo(foo="foo")
    assert foo.foo == "foo"
    assert foo.bar is unsupported
