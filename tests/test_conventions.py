from __future__ import annotations

from datetime import date

from br_market_calendar import BrazilFinancialCalendar, BusinessDayConvention


def test_adjust_following_from_business_day() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-01-02", BusinessDayConvention.FOLLOWING)

    assert result == date(2026, 1, 2)


def test_adjust_following_from_saturday() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-01-03", BusinessDayConvention.FOLLOWING)

    assert result == date(2026, 1, 5)


def test_adjust_preceding_from_saturday() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-01-03", BusinessDayConvention.PRECEDING)

    assert result == date(2026, 1, 2)


def test_adjust_unadjusted_from_saturday() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-01-03", BusinessDayConvention.UNADJUSTED)

    assert result == date(2026, 1, 3)


def test_adjust_accepts_string_convention() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-01-03", "following")

    assert result == date(2026, 1, 5)


def test_adjust_modified_following_same_month() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-01-03", BusinessDayConvention.MODIFIED_FOLLOWING)

    assert result == date(2026, 1, 5)


def test_adjust_modified_following_changes_month() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-01-31", BusinessDayConvention.MODIFIED_FOLLOWING)

    assert result == date(2026, 1, 30)


def test_adjust_modified_preceding_same_month() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-01-03", BusinessDayConvention.MODIFIED_PRECEDING)

    assert result == date(2026, 1, 2)


def test_adjust_modified_preceding_changes_month() -> None:
    cal = BrazilFinancialCalendar()

    result = cal.adjust("2026-02-01", BusinessDayConvention.MODIFIED_PRECEDING)

    assert result == date(2026, 2, 2)


def test_adjust_following_with_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-05"])

    result = cal.adjust("2026-01-03", BusinessDayConvention.FOLLOWING)

    assert result == date(2026, 1, 6)


def test_adjust_preceding_with_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-02"])

    result = cal.adjust("2026-01-03", BusinessDayConvention.PRECEDING)

    assert result == date(2026, 1, 1)
