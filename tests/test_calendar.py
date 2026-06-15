from __future__ import annotations

from datetime import date

from br_market_calendar import BrazilFinancialCalendar


def test_create_empty_calendar() -> None:
    cal = BrazilFinancialCalendar()

    assert cal.holidays is not None


def test_create_calendar_from_holidays() -> None:
    cal = BrazilFinancialCalendar.from_holidays(
        [
            "2026-01-01",
            "2026-12-25",
        ]
    )

    assert cal.is_holiday("2026-01-01") is True
    assert cal.is_holiday("2026-01-02") is False


def test_is_business_day_for_regular_weekday() -> None:
    cal = BrazilFinancialCalendar()

    assert cal.is_business_day("2026-01-02") is True


def test_is_business_day_for_saturday() -> None:
    cal = BrazilFinancialCalendar()

    assert cal.is_business_day("2026-01-03") is False


def test_is_business_day_for_sunday() -> None:
    cal = BrazilFinancialCalendar()

    assert cal.is_business_day("2026-01-04") is False


def test_is_business_day_for_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

    assert cal.is_business_day("2026-01-01") is False


def test_is_non_business_day() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

    assert cal.is_non_business_day("2026-01-01") is True
    assert cal.is_non_business_day("2026-01-02") is False


def test_calendar_days() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.calendar_days("2026-01-01", "2026-01-03")

    assert result == [
        date(2026, 1, 1),
        date(2026, 1, 2),
        date(2026, 1, 3),
    ]


def test_weekdays_list_ignores_holidays() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-02"])

    result = cal.weekdays("2026-01-01", "2026-01-04")

    assert result == [date(2026, 1, 1), date(2026, 1, 2)]


def test_business_days_list_excludes_weekends_and_holidays() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

    result = cal.business_days("2026-01-01", "2026-01-05")

    assert result == [date(2026, 1, 2), date(2026, 1, 5)]


def test_holidays_between() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01", "2026-12-25"])

    result = cal.holidays_between("2026-01-01", "2026-01-31")

    assert dict(result) == {date(2026, 1, 1): "2026-01-01"}


def test_holidays_between_uses_names_when_available() -> None:
    cal = BrazilFinancialCalendar()
    cal.holidays.add_holiday("2026-02-16", "Carnaval")

    result = cal.holidays_between("2026-02-01", "2026-02-28")

    assert dict(result) == {date(2026, 2, 16): "Carnaval"}


def test_weekday_occurrences() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.weekday_occurrences("2026-01-01", "2026-01-15", 2)

    assert result == [date(2026, 1, 6), date(2026, 1, 13)]


def test_business_days_per_month() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

    result = cal.business_days_per_month("2026-01-01", "2026-02-03")

    assert dict(result) == {"01/2026": 21, "02/2026": 2}


def test_next_business_day_from_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

    result = cal.next_business_day("2026-01-01")

    assert result == date(2026, 1, 2)


def test_next_business_day_from_friday() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.next_business_day("2026-01-02")

    assert result == date(2026, 1, 5)


def test_next_business_day_include_current() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.next_business_day("2026-01-02", include_current=True)

    assert result == date(2026, 1, 2)


def test_previous_business_day_from_sunday() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.previous_business_day("2026-01-04")

    assert result == date(2026, 1, 2)


def test_previous_business_day_include_current() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.previous_business_day("2026-01-02", include_current=True)

    assert result == date(2026, 1, 2)


def test_add_business_days_positive() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.add_business_days("2026-01-02", 1)

    assert result == date(2026, 1, 5)


def test_add_business_days_positive_with_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-05"])

    result = cal.add_business_days("2026-01-02", 1)

    assert result == date(2026, 1, 6)


def test_add_business_days_negative() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.add_business_days("2026-01-05", -1)

    assert result == date(2026, 1, 2)


def test_add_business_days_zero() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.add_business_days("2026-01-05", 0)

    assert result == date(2026, 1, 5)


def test_business_days_between_forward_exclusive() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.business_days_between("2026-01-01", "2026-01-08")

    assert result == 5


def test_business_days_between_forward_inclusive() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.business_days_between("2026-01-01", "2026-01-08", inclusive=True)

    assert result == 6


def test_business_days_between_with_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

    result = cal.business_days_between("2026-01-01", "2026-01-08")

    assert result == 4


def test_business_days_between_same_day_exclusive() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.business_days_between("2026-01-05", "2026-01-05")

    assert result == 0


def test_business_days_between_same_day_inclusive_business_day() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.business_days_between("2026-01-05", "2026-01-05", inclusive=True)

    assert result == 1


def test_business_days_between_same_day_inclusive_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-05"])

    result = cal.business_days_between("2026-01-05", "2026-01-05", inclusive=True)

    assert result == 0


def test_business_days_between_backward_exclusive() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.business_days_between("2026-01-08", "2026-01-01")

    assert result == -5


def test_business_days_between_backward_inclusive() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.business_days_between("2026-01-08", "2026-01-01", inclusive=True)

    assert result == -6
