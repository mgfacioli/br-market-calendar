from __future__ import annotations

from datetime import date

from br_market_calendar.calendar import BrazilFinancialCalendar
from br_market_calendar.conventions import BusinessDayConvention
from br_market_calendar.types import DateLike


def settlement_date(
    trade_date: DateLike,
    lag: int = 1,
    *,
    calendar: BrazilFinancialCalendar | None = None,
    convention: BusinessDayConvention | str = BusinessDayConvention.FOLLOWING,
) -> date:
    """
    Calculate settlement date from a trade date and a business-day lag.

    Parameters
    ----------
    trade_date:
        Trade date.
    lag:
        Number of business days after trade date. Use 0 for D+0.
    calendar:
        Financial calendar used for business-day calculation.
    convention:
        Adjustment convention applied when lag is 0.

    Returns
    -------
    date
        Settlement date.
    """
    if lag < 0:
        msg = "Settlement lag cannot be negative."
        raise ValueError(msg)

    cal = calendar or BrazilFinancialCalendar()

    if lag == 0:
        return cal.adjust(trade_date, convention)

    return cal.add_business_days(trade_date, lag)
