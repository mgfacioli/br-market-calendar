from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime
from pathlib import Path
from typing import Any, TypeGuard

from br_market_calendar.formatters import parse_date
from br_market_calendar.holidays import HolidayCalendar
from br_market_calendar.types import DateLike

ANBIMA_HOLIDAYS_URL = "http://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls"


def _require_pandas() -> Any:
    try:
        import pandas as pd  # type: ignore[import-untyped]
    except ImportError as exc:
        msg = (
            "pandas is required for ANBIMA CSV/Excel readers. "
            "Install with: pip install br-market-calendar[pandas]"
        )
        raise ImportError(msg) from exc

    return pd


def _is_date_like(value: object) -> TypeGuard[DateLike]:
    return isinstance(value, (str, date, datetime))


def _holiday_calendar_from_values(values: Iterable[object]) -> HolidayCalendar:
    holidays = set()

    for value in values:
        if value is None or not _is_date_like(value) or not str(value).strip():
            continue

        try:
            holidays.add(parse_date(value))
        except ValueError:
            continue

    return HolidayCalendar(holidays)


def read_anbima_csv(
    path: str | Path,
    *,
    encoding: str = "latin1",
    separator: str = ";",
    date_column: str = "Data",
) -> HolidayCalendar:
    """
    Read an ANBIMA-compatible CSV holiday file.
    """
    pd = _require_pandas()

    df = pd.read_csv(path, encoding=encoding, sep=separator)

    if date_column not in df.columns:
        msg = f"Date column {date_column!r} not found in CSV file."
        raise ValueError(msg)

    return _holiday_calendar_from_values(df[date_column].dropna())


def read_anbima_excel(
    path: str | Path,
    *,
    date_column: str = "Data",
) -> HolidayCalendar:
    """
    Read an ANBIMA Excel holiday file.
    """
    pd = _require_pandas()

    df = pd.read_excel(path)

    if date_column not in df.columns:
        msg = f"Date column {date_column!r} not found in Excel file."
        raise ValueError(msg)

    return _holiday_calendar_from_values(df[date_column].dropna())


def read_anbima_url(
    url: str = ANBIMA_HOLIDAYS_URL,
    *,
    date_column: str = "Data",
) -> HolidayCalendar:
    """
    Read the official ANBIMA holiday Excel file from URL.
    """
    return read_anbima_excel(url, date_column=date_column)
