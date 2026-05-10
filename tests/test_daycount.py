from __future__ import annotations

from br_market_calendar import (
    BrazilFinancialCalendar,
    DayCountConvention,
    day_count,
    year_fraction,
)


def test_day_count_act_252() -> None:
    result = day_count("2026-01-01", "2026-01-08", DayCountConvention.ACT_252)

    assert result == 5


def test_day_count_act_252_with_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

    result = day_count(
        "2026-01-01",
        "2026-01-08",
        DayCountConvention.ACT_252,
        calendar=cal,
    )

    assert result == 4


def test_day_count_act_360() -> None:
    result = day_count("2026-01-01", "2026-01-31", DayCountConvention.ACT_360)

    assert result == 30


def test_day_count_act_365() -> None:
    result = day_count("2026-01-01", "2026-01-31", DayCountConvention.ACT_365)

    assert result == 30


def test_day_count_30_360() -> None:
    result = day_count("2026-01-01", "2026-02-01", DayCountConvention.THIRTY_360)

    assert result == 30


def test_day_count_accepts_string_convention() -> None:
    result = day_count("2026-01-01", "2026-01-31", "ACT/360")

    assert result == 30


def test_year_fraction_act_252() -> None:
    result = year_fraction("2026-01-01", "2026-01-08", DayCountConvention.ACT_252)

    assert result == 5 / 252


def test_year_fraction_act_252_with_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

    result = year_fraction(
        "2026-01-01",
        "2026-01-08",
        DayCountConvention.ACT_252,
        calendar=cal,
    )

    assert result == 4 / 252


def test_year_fraction_act_360() -> None:
    result = year_fraction("2026-01-01", "2026-01-31", DayCountConvention.ACT_360)

    assert result == 30 / 360


def test_year_fraction_act_365() -> None:
    result = year_fraction("2026-01-01", "2026-01-31", DayCountConvention.ACT_365)

    assert result == 30 / 365


def test_year_fraction_30_360() -> None:
    result = year_fraction(
        "2026-01-01",
        "2026-02-01",
        DayCountConvention.THIRTY_360,
    )

    assert result == 30 / 360


def test_day_count_30_360_end_of_month_adjustment() -> None:
    result = day_count(
        "2026-01-30",
        "2026-01-31",
        DayCountConvention.THIRTY_360,
    )

    assert result == 0
