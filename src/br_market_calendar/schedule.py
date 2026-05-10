from __future__ import annotations

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

    raw_dates: list[date] = []

    if include_start:
        raw_dates.append(start_date)

    current = start_date + relativedelta(months=months)

    while current < end_date:
        raw_dates.append(current)
        current = current + relativedelta(months=months)

    if include_end:
        raw_dates.append(end_date)

    adjusted_dates = [cal.adjust(value, convention) for value in raw_dates]

    return _deduplicate_preserving_order(adjusted_dates)


def _deduplicate_preserving_order(values: list[date]) -> list[date]:
    seen: set[date] = set()
    result: list[date] = []

    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)

    return result
