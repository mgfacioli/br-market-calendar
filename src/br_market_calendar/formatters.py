from __future__ import annotations

import re
from datetime import date, datetime

from br_market_calendar.types import DateLike

ISO_DATE_FORMAT = "%Y-%m-%d"
BR_DATE_FORMAT = "%d/%m/%Y"


def parse_date(value: DateLike, date_format: str | None = None) -> date:
    """
    Convert a string, date, or datetime object into a datetime.date.

    Parameters
    ----------
    value:
        Input value to convert.
    date_format:
        Optional explicit format for string parsing.

    Returns
    -------
    date
        Parsed date.

    Examples
    --------
    >>> parse_date("2026-01-31")
    datetime.date(2026, 1, 31)

    >>> parse_date("31/01/2026")
    datetime.date(2026, 1, 31)
    """
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if not isinstance(value, str):
        msg = f"Unsupported date value type: {type(value)!r}"
        raise TypeError(msg)

    text = value.strip()

    if not text:
        msg = "Date string cannot be empty."
        raise ValueError(msg)

    if date_format is not None:
        return datetime.strptime(text, date_format).date()

    for candidate_format in (ISO_DATE_FORMAT, BR_DATE_FORMAT):
        try:
            return datetime.strptime(text, candidate_format).date()
        except ValueError:
            continue

    if re.fullmatch(r"\d{2}\D+\d{2}\D+\d{4}", text):
        normalized = re.sub(r"\D+", "/", text)
        return datetime.strptime(normalized, BR_DATE_FORMAT).date()

    msg = (
        f"Could not parse date {value!r}. "
        f"Expected formats: {ISO_DATE_FORMAT!r}, {BR_DATE_FORMAT!r}, "
        "or a day-first date with a non-digit separator."
    )
    raise ValueError(msg)


def format_date(value: DateLike, date_format: str = ISO_DATE_FORMAT) -> str:
    """
    Format a date-like value as string.

    Parameters
    ----------
    value:
        Input value to format.
    date_format:
        strftime-compatible date format.

    Returns
    -------
    str
        Formatted date string.
    """
    parsed = parse_date(value)
    return parsed.strftime(date_format)


def to_iso(value: DateLike) -> str:
    """
    Format a date-like value as ISO date: YYYY-MM-DD.
    """
    return format_date(value, ISO_DATE_FORMAT)


def to_brazilian(value: DateLike) -> str:
    """
    Format a date-like value as Brazilian date: DD/MM/YYYY.
    """
    return format_date(value, BR_DATE_FORMAT)
