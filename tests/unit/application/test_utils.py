import pytest
from sanic.exceptions import InvalidUsage

from heliotrope.application.utils import check_int32, check_int64


def test_check_int32_valid() -> None:
    check_int32(0)
    check_int32(2147483647)
    check_int32(-2147483648)
    check_int32(123456)


def test_check_int32_invalid() -> None:
    with pytest.raises(InvalidUsage):
        check_int32(2147483648)
    with pytest.raises(InvalidUsage):
        check_int32(-2147483649)


def test_check_int64_valid() -> None:
    check_int64(0)
    check_int64(9223372036854775807)
    check_int64(-9223372036854775808)
    check_int64(1234567890123456789)


def test_check_int64_invalid() -> None:
    with pytest.raises(InvalidUsage):
        check_int64(9223372036854775808)
    with pytest.raises(InvalidUsage):
        check_int64(-9223372036854775809)
