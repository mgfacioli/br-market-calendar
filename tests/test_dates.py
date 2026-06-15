from __future__ import annotations

from datetime import date

from br_market_calendar.dates import (
    add_days,
    date_range,
    days_between,
    first_day_of_month,
    is_weekday,
    is_weekend,
    last_day_of_month,
    weekday_name,
    weekdays,
)


def test_is_weekend_for_saturday() -> None:
    assert is_weekend("2026-01-03") is True


def test_is_weekend_for_sunday() -> None:
    assert is_weekend("2026-01-04") is True


def test_is_weekend_for_monday() -> None:
    assert is_weekend("2026-01-05") is False


def test_is_weekday_for_monday() -> None:
    assert is_weekday("2026-01-05") is True


def test_is_weekday_for_saturday() -> None:
    assert is_weekday("2026-01-03") is False


def test_days_between_forward_exclusive() -> None:
    result = days_between("2026-01-01", "2026-01-10")

    assert result == 9


def test_days_between_forward_inclusive() -> None:
    result = days_between("2026-01-01", "2026-01-10", inclusive=True)

    assert result == 10


def test_days_between_same_day_exclusive() -> None:
    result = days_between("2026-01-01", "2026-01-01")

    assert result == 0


def test_days_between_same_day_inclusive() -> None:
    result = days_between("2026-01-01", "2026-01-01", inclusive=True)

    assert result == 1


def test_days_between_backward_exclusive() -> None:
    result = days_between("2026-01-10", "2026-01-01")

    assert result == -9


def test_days_between_backward_inclusive() -> None:
    result = days_between("2026-01-10", "2026-01-01", inclusive=True)

    assert result == -10


def test_add_days_positive() -> None:
    result = add_days("2026-01-01", 10)

    assert result == date(2026, 1, 11)


def test_add_days_negative() -> None:
    result = add_days("2026-01-10", -9)

    assert result == date(2026, 1, 1)


def test_add_days_zero() -> None:
    result = add_days("2026-01-10", 0)

    assert result == date(2026, 1, 10)


def test_date_range_forward_inclusive() -> None:
    result = date_range("2026-01-01", "2026-01-03")

    assert result == [
        date(2026, 1, 1),
        date(2026, 1, 2),
        date(2026, 1, 3),
    ]


def test_date_range_forward_exclusive() -> None:
    result = date_range("2026-01-01", "2026-01-03", inclusive=False)

    assert result == [date(2026, 1, 1), date(2026, 1, 2)]


def test_date_range_backward_inclusive() -> None:
    result = date_range("2026-01-03", "2026-01-01")

    assert result == [
        date(2026, 1, 3),
        date(2026, 1, 2),
        date(2026, 1, 1),
    ]


def test_date_range_positive_days() -> None:
    result = date_range("2026-01-01", days=3)

    assert result == [
        date(2026, 1, 1),
        date(2026, 1, 2),
        date(2026, 1, 3),
    ]


def test_date_range_negative_days() -> None:
    result = date_range("2026-01-03", days=-3)

    assert result == [
        date(2026, 1, 1),
        date(2026, 1, 2),
        date(2026, 1, 3),
    ]


def test_weekdays() -> None:
    result = weekdays("2026-01-02", "2026-01-05")

    assert result == [date(2026, 1, 2), date(2026, 1, 5)]


def test_first_day_of_month() -> None:
    assert first_day_of_month("2026-02-15") == date(2026, 2, 1)


def test_last_day_of_month() -> None:
    assert last_day_of_month("2026-02-15") == date(2026, 2, 28)


def test_weekday_name_in_portuguese() -> None:
    assert weekday_name("2026-01-07") == "quarta-feira"
