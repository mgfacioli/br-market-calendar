from __future__ import annotations

from datetime import date

import pytest

from br_market_calendar.holidays import HolidayCalendar


def test_create_empty_calendar() -> None:
    holidays = HolidayCalendar()

    assert len(holidays) == 0


def test_create_calendar_from_iterable() -> None:
    holidays = HolidayCalendar.from_iterable(
        [
            "2026-01-01",
            "2026-12-25",
        ]
    )

    assert len(holidays) == 2


def test_is_holiday_true() -> None:
    holidays = HolidayCalendar.from_iterable(
        [
            "2026-01-01",
        ]
    )

    assert holidays.is_holiday("2026-01-01") is True


def test_is_holiday_false() -> None:
    holidays = HolidayCalendar.from_iterable(
        [
            "2026-01-01",
        ]
    )

    assert holidays.is_holiday("2026-01-02") is False


def test_add_holiday() -> None:
    holidays = HolidayCalendar()

    holidays.add_holiday("2026-04-21")

    assert holidays.is_holiday("2026-04-21") is True


def test_add_holiday_with_name() -> None:
    holidays = HolidayCalendar()

    holidays.add_holiday("2026-04-21", "Tiradentes")

    assert holidays.is_holiday("2026-04-21") is True
    assert holidays.holiday_name("2026-04-21") == "Tiradentes"


def test_remove_holiday() -> None:
    holidays = HolidayCalendar()
    holidays.add_holiday("2026-04-21", "Tiradentes")

    holidays.remove_holiday("2026-04-21")

    assert holidays.is_holiday("2026-04-21") is False
    assert holidays.holiday_name("2026-04-21") is None


def test_remove_missing_holiday_raises() -> None:
    holidays = HolidayCalendar()

    with pytest.raises(KeyError):
        holidays.remove_holiday("2026-04-21")


def test_contains_operator() -> None:
    holidays = HolidayCalendar.from_iterable(
        [
            "2026-01-01",
        ]
    )

    assert "2026-01-01" in holidays


def test_contains_operator_false() -> None:
    holidays = HolidayCalendar.from_iterable(
        [
            "2026-01-01",
        ]
    )

    assert "2026-01-02" not in holidays


def test_iter_returns_sorted_dates() -> None:
    holidays = HolidayCalendar.from_iterable(
        [
            "2026-12-25",
            "2026-01-01",
        ]
    )

    result = list(holidays)

    assert result == [
        date(2026, 1, 1),
        date(2026, 12, 25),
    ]
