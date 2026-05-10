from __future__ import annotations

import calendar as py_calendar
from datetime import date
from enum import StrEnum

from dateutil.relativedelta import relativedelta

from br_market_calendar.calendar import BrazilFinancialCalendar
from br_market_calendar.conventions import BusinessDayConvention
from br_market_calendar.formatters import parse_date
from br_market_calendar.types import DateLike


class Frequency(StrEnum):
    """
    Schedule generation frequencies.
    """

    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMIANNUAL = "semiannual"
    ANNUAL = "annual"


_FREQUENCY_TO_MONTHS: dict[Frequency, int] = {
    Frequency.MONTHLY: 1,
    Frequency.QUARTERLY: 3,
    Frequency.SEMIANNUAL: 6,
    Frequency.ANNUAL: 12,
}


def generate_schedule(
    start: DateLike,
    end: DateLike,
    frequency: Frequency | str = Frequency.MONTHLY,
    *,
    calendar: BrazilFinancialCalendar | None = None,
    convention: BusinessDayConvention | str = BusinessDayConvention.FOLLOWING,
    include_start: bool = True,
    include_end: bool = True,
    end_of_month: bool = False,
) -> list[date]:
    """
    Generate an adjusted financial date schedule.

    Parameters
    ----------
    start:
        Schedule start date.
    end:
        Schedule end date.
    frequency:
        Schedule frequency: monthly, quarterly, semiannual, annual.
    calendar:
        Financial calendar used for business day adjustment.
    convention:
        Business day adjustment convention.
    include_start:
        Whether to include the start date.
    include_end:
        Whether to include the end date.
    end_of_month:
        If True and the start date is the last calendar day of the month,
        generated intermediate dates are also moved to the last calendar day
        of their respective months before business-day adjustment.

    Returns
    -------
    list[date]
        Adjusted schedule dates.
    """
    start_date = parse_date(start)
    end_date = parse_date(end)

    if end_date < start_date:
        msg = "End date must be greater than or equal to start date."
        raise ValueError(msg)

    frequency = Frequency(frequency)
    months = _FREQUENCY_TO_MONTHS[frequency]
    cal = calendar or BrazilFinancialCalendar()

    raw_dates = _generate_raw_schedule_dates(
        start_date=start_date,
        end_date=end_date,
        months=months,
        include_start=include_start,
        include_end=include_end,
        end_of_month=end_of_month,
    )

    adjusted_dates = [cal.adjust(value, convention) for value in raw_dates]

    return _deduplicate_preserving_order(adjusted_dates)


def _generate_raw_schedule_dates(
    *,
    start_date: date,
    end_date: date,
    months: int,
    include_start: bool,
    include_end: bool,
    end_of_month: bool,
) -> list[date]:
    raw_dates: list[date] = []
    use_end_of_month = end_of_month and _is_end_of_month(start_date)

    if include_start:
        raw_dates.append(start_date)

    current = start_date + relativedelta(months=months)

    if use_end_of_month:
        current = _end_of_month(current)

    while current < end_date:
        raw_dates.append(current)
        current = current + relativedelta(months=months)

        if use_end_of_month:
            current = _end_of_month(current)

    if include_end:
        raw_dates.append(end_date)

    return raw_dates


def _is_end_of_month(value: date) -> bool:
    return value.day == py_calendar.monthrange(value.year, value.month)[1]


def _end_of_month(value: date) -> date:
    last_day = py_calendar.monthrange(value.year, value.month)[1]
    return value.replace(day=last_day)


def _deduplicate_preserving_order(values: list[date]) -> list[date]:
    seen: set[date] = set()
    result: list[date] = []

    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)

    return result
