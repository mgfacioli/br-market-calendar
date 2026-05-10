from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date

from br_market_calendar.formatters import parse_date
from br_market_calendar.types import DateLike


@dataclass(slots=True)
class HolidayCalendar:
    """
    Immutable holiday calendar.

    Internally stores holidays as a set of datetime.date objects.
    """

    holidays: set[date] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.holidays = {parse_date(value) for value in self.holidays}

    @classmethod
    def from_iterable(cls, values: list[DateLike]) -> HolidayCalendar:
        """
        Create a HolidayCalendar from an iterable of date-like values.
        """
        return cls({parse_date(value) for value in values})

    def is_holiday(self, value: DateLike) -> bool:
        """
        Return True if the given date is a holiday.
        """
        parsed = parse_date(value)
        return parsed in self.holidays

    def add_holiday(self, value: DateLike) -> None:
        """
        Add a holiday to the calendar.
        """
        self.holidays.add(parse_date(value))

    def remove_holiday(self, value: DateLike) -> None:
        """
        Remove a holiday from the calendar.

        Raises
        ------
        KeyError
            If the holiday does not exist.
        """
        self.holidays.remove(parse_date(value))

    def __contains__(self, value: object) -> bool:
        """
        Support usage like:

        '2026-01-01' in holidays
        """
        if isinstance(value, (str, date)):
            return self.is_holiday(value)

        return False

    def __len__(self) -> int:
        return len(self.holidays)

    def __iter__(self) -> Iterator[date]:
        return iter(sorted(self.holidays))
