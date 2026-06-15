from __future__ import annotations

import calendar
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


def date_range(
    start: DateLike,
    end: DateLike | None = None,
    *,
    days: int | None = None,
    inclusive: bool = True,
) -> list[date]:
    """
    Return calendar dates in a period.

    Use either ``end`` or ``days``. When ``days`` is positive, the range starts
    at ``start``. When ``days`` is negative, the range ends at ``start``.
    """
    start_date = parse_date(start)

    if (end is None) == (days is None):
        msg = "Provide exactly one of 'end' or 'days'."
        raise ValueError(msg)

    if days is not None:
        if days == 0:
            return []

        length = abs(days)
        first = start_date if days > 0 else start_date - timedelta(days=length - 1)
        return [first + timedelta(days=offset) for offset in range(length)]

    if end is None:
        msg = "end cannot be None when days is not provided."
        raise ValueError(msg)

    end_date = parse_date(end)
    if start_date == end_date:
        return [start_date] if inclusive else []

    step = 1 if end_date > start_date else -1
    stop = end_date + timedelta(days=step) if inclusive else end_date

    result = []
    current = start_date
    while current != stop:
        result.append(current)
        current += timedelta(days=step)

    return result


def weekdays(
    start: DateLike,
    end: DateLike | None = None,
    *,
    days: int | None = None,
    inclusive: bool = True,
) -> list[date]:
    """
    Return Monday-Friday dates in a period.
    """
    return [
        current
        for current in date_range(start, end, days=days, inclusive=inclusive)
        if is_weekday(current)
    ]


def first_day_of_month(value: DateLike) -> date:
    """
    Return the first day of the month for a date-like value.
    """
    parsed = parse_date(value)
    return date(parsed.year, parsed.month, 1)


def last_day_of_month(value: DateLike) -> date:
    """
    Return the last day of the month for a date-like value.
    """
    parsed = parse_date(value)
    _, last_day = calendar.monthrange(parsed.year, parsed.month)
    return date(parsed.year, parsed.month, last_day)


def weekday_name(value: DateLike, language: str = "pt_BR") -> str:
    """
    Return the weekday name for a date-like value.
    """
    parsed = parse_date(value)

    if language in {"pt", "pt_BR", "pt-BR"}:
        names = (
            "segunda-feira",
            "terca-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sabado",
            "domingo",
        )
        return names[parsed.weekday()]

    if language in {"en", "en_US", "en-US"}:
        return calendar.day_name[parsed.weekday()]

    msg = f"Unsupported language: {language!r}."
    raise ValueError(msg)
