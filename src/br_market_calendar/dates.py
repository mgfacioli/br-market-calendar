from __future__ import annotations

from datetime import date, timedelta

from br_market_calendar.formatters import parse_date
from br_market_calendar.types import DateLike


def is_weekend(value: DateLike) -> bool:
    """
    Return True if the date falls on Saturday or Sunday.
    """
    parsed = parse_date(value)
    return parsed.weekday() >= 5


def is_weekday(value: DateLike) -> bool:
    """
    Return True if the date falls between Monday and Friday.
    """
    return not is_weekend(value)


def days_between(start: DateLike, end: DateLike, inclusive: bool = False) -> int:
    """
    Return the number of calendar days between two dates.

    By default, the result is exclusive of the end date, following the
    standard date subtraction behavior.
    """
    start_date = parse_date(start)
    end_date = parse_date(end)

    delta = (end_date - start_date).days

    if inclusive:
        if delta >= 0:
            return delta + 1
        return delta - 1

    return delta


def add_days(value: DateLike, days: int) -> date:
    """
    Add calendar days to a date-like value.
    """
    parsed = parse_date(value)
    return parsed + timedelta(days=days)
