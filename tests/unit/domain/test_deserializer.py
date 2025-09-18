from dataclasses import dataclass

import pytest

from heliotrope.domain.deserializer import Deserializer


@dataclass
class Child(Deserializer):
    foo: str


@dataclass
class Parent(Deserializer):
    foo: str
    bar: list[Child]


def test_deserialize_exception():
    with pytest.raises(ValueError):
        Parent.from_dict(
            {
                "foo": "hello",
                "bar": [
                    {"foo": 123},
                ],
                "baz": "extra",
            }
        )


def test_deserialize_child_is_none():
    parent = Parent.from_dict(
        {
            "foo": "hello",
            "bar": None,
        }
    )
    assert parent.foo == "hello"
    assert parent.bar == []
