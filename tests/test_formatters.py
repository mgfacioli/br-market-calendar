from __future__ import annotations

from datetime import date, datetime

import pytest

from br_market_calendar import (
    BR_DATE_FORMAT,
    ISO_DATE_FORMAT,
    format_date,
    parse_date,
    to_brazilian,
    to_iso,
)


def test_parse_date_from_date() -> None:
    value = date(2026, 1, 31)

    result = parse_date(value)

    assert result == date(2026, 1, 31)


def test_parse_date_from_datetime() -> None:
    value = datetime(2026, 1, 31, 15, 45, 30)

    result = parse_date(value)

    assert result == date(2026, 1, 31)


def test_parse_date_from_iso_string() -> None:
    result = parse_date("2026-01-31")

    assert result == date(2026, 1, 31)


def test_parse_date_from_brazilian_string() -> None:
    result = parse_date("31/01/2026")

    assert result == date(2026, 1, 31)


def test_parse_date_strips_spaces() -> None:
    result = parse_date(" 2026-01-31 ")

    assert result == date(2026, 1, 31)


def test_parse_date_with_explicit_format() -> None:
    result = parse_date("20260131", "%Y%m%d")

    assert result == date(2026, 1, 31)


def test_parse_date_rejects_empty_string() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        parse_date("")


def test_parse_date_rejects_invalid_string() -> None:
    with pytest.raises(ValueError, match="Could not parse date"):
        parse_date("31-01-2026")


def test_parse_date_rejects_unsupported_type() -> None:
    with pytest.raises(TypeError, match="Unsupported date value type"):
        parse_date(20260131)  # type: ignore[arg-type]


def test_format_date_uses_iso_by_default() -> None:
    result = format_date(date(2026, 1, 31))

    assert result == "2026-01-31"


def test_format_date_with_brazilian_format() -> None:
    result = format_date(date(2026, 1, 31), BR_DATE_FORMAT)

    assert result == "31/01/2026"


def test_to_iso() -> None:
    result = to_iso("31/01/2026")

    assert result == "2026-01-31"


def test_to_brazilian() -> None:
    result = to_brazilian("2026-01-31")

    assert result == "31/01/2026"


def test_format_constants() -> None:
    assert ISO_DATE_FORMAT == "%Y-%m-%d"
    assert BR_DATE_FORMAT == "%d/%m/%Y"
