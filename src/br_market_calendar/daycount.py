from __future__ import annotations

from enum import StrEnum

from br_market_calendar.calendar import BrazilFinancialCalendar
from br_market_calendar.dates import days_between
from br_market_calendar.formatters import parse_date
from br_market_calendar.types import DateLike


class DayCountConvention(StrEnum):
    """
    Financial day count conventions.
    """

    ACT_252 = "ACT/252"
    ACT_360 = "ACT/360"
    ACT_365 = "ACT/365"
    THIRTY_360 = "30/360"


def day_count(
    start: DateLike,
    end: DateLike,
    convention: DayCountConvention | str = DayCountConvention.ACT_252,
    calendar: BrazilFinancialCalendar | None = None,
) -> int:
    """
    Count days according to a financial day count convention.
    """
    convention = DayCountConvention(convention)

    if convention == DayCountConvention.ACT_252:
        cal = calendar or BrazilFinancialCalendar()
        return cal.business_days_between(start, end)

    if convention in (DayCountConvention.ACT_360, DayCountConvention.ACT_365):
        return days_between(start, end)

    if convention == DayCountConvention.THIRTY_360:
        return _day_count_30_360(start, end)

    msg = f"Unsupported day count convention: {convention!r}"
    raise ValueError(msg)


def year_fraction(
    start: DateLike,
    end: DateLike,
    convention: DayCountConvention | str = DayCountConvention.ACT_252,
    calendar: BrazilFinancialCalendar | None = None,
) -> float:
    """
    Calculate year fraction according to a financial day count convention.
    """
    convention = DayCountConvention(convention)
    days = day_count(start, end, convention, calendar)

    if convention == DayCountConvention.ACT_252:
        return days / 252

    if convention == DayCountConvention.ACT_360:
        return days / 360

    if convention == DayCountConvention.ACT_365:
        return days / 365

    if convention == DayCountConvention.THIRTY_360:
        return days / 360

    msg = f"Unsupported day count convention: {convention!r}"
    raise ValueError(msg)


def _day_count_30_360(start: DateLike, end: DateLike) -> int:
    """
    Calculate 30/360 day count using a simple US/NASD-like convention.

    This first version intentionally keeps the implementation simple.
    """
    start_date = parse_date(start)
    end_date = parse_date(end)

    d1 = min(start_date.day, 30)
    d2 = end_date.day

    if d1 == 30 and d2 == 31:
        d2 = 30

    return (
        360 * (end_date.year - start_date.year)
        + 30 * (end_date.month - start_date.month)
        + (d2 - d1)
    )
