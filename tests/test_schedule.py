from __future__ import annotations

from datetime import date

import pytest

from br_market_calendar import (
    BrazilFinancialCalendar,
    BusinessDayConvention,
    Frequency,
    generate_schedule,
)


def test_generate_monthly_schedule() -> None:
    result = generate_schedule(
        "2026-01-01",
        "2026-04-01",
        Frequency.MONTHLY,
    )

    assert result == [
        date(2026, 1, 1),
        date(2026, 2, 2),
        date(2026, 3, 2),
        date(2026, 4, 1),
    ]


def test_generate_quarterly_schedule() -> None:
    result = generate_schedule(
        "2026-01-01",
        "2026-10-01",
        Frequency.QUARTERLY,
    )

    assert result == [
        date(2026, 1, 1),
        date(2026, 4, 1),
        date(2026, 7, 1),
        date(2026, 10, 1),
    ]


def test_generate_semiannual_schedule() -> None:
    result = generate_schedule(
        "2026-01-01",
        "2027-01-01",
        Frequency.SEMIANNUAL,
    )

    assert result == [
        date(2026, 1, 1),
        date(2026, 7, 1),
        date(2027, 1, 1),
    ]


def test_generate_annual_schedule() -> None:
    result = generate_schedule(
        "2026-01-01",
        "2028-01-01",
        Frequency.ANNUAL,
    )

    assert result == [
        date(2026, 1, 1),
        date(2027, 1, 1),
        date(2028, 1, 3),
    ]


def test_generate_schedule_accepts_string_frequency() -> None:
    result = generate_schedule(
        "2026-01-01",
        "2026-04-01",
        "monthly",
    )

    assert result == [
        date(2026, 1, 1),
        date(2026, 2, 2),
        date(2026, 3, 2),
        date(2026, 4, 1),
    ]


def test_generate_schedule_without_start() -> None:
    result = generate_schedule(
        "2026-01-01",
        "2026-04-01",
        Frequency.MONTHLY,
        include_start=False,
    )

    assert result == [
        date(2026, 2, 2),
        date(2026, 3, 2),
        date(2026, 4, 1),
    ]


def test_generate_schedule_without_end() -> None:
    result = generate_schedule(
        "2026-01-01",
        "2026-04-01",
        Frequency.MONTHLY,
        include_end=False,
    )

    assert result == [
        date(2026, 1, 1),
        date(2026, 2, 2),
        date(2026, 3, 2),
    ]


def test_generate_schedule_with_holiday_calendar() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-04-01"])

    result = generate_schedule(
        "2026-01-01",
        "2026-04-01",
        Frequency.QUARTERLY,
        calendar=cal,
    )

    assert result == [
        date(2026, 1, 1),
        date(2026, 4, 2),
    ]


def test_generate_schedule_with_preceding_convention() -> None:
    result = generate_schedule(
        "2026-01-01",
        "2026-02-01",
        Frequency.MONTHLY,
        convention=BusinessDayConvention.PRECEDING,
    )

    assert result == [
        date(2026, 1, 1),
        date(2026, 1, 30),
    ]


def test_generate_schedule_with_modified_following() -> None:
    result = generate_schedule(
        "2026-01-31",
        "2026-04-30",
        Frequency.MONTHLY,
        convention=BusinessDayConvention.MODIFIED_FOLLOWING,
    )

    assert result == [
        date(2026, 1, 30),
        date(2026, 2, 27),
        date(2026, 3, 30),
        date(2026, 4, 28),
        date(2026, 4, 30),
    ]


def test_generate_schedule_raises_when_end_before_start() -> None:
    with pytest.raises(ValueError, match="End date must be greater"):
        generate_schedule("2026-04-01", "2026-01-01")
