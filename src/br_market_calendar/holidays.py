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
    holiday_names: dict[date, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.holidays = {parse_date(value) for value in self.holidays}
        self.holiday_names = {
            parse_date(value): name for value, name in self.holiday_names.items()
        }
        self.holidays.update(self.holiday_names)

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

    def add_holiday(self, value: DateLike, name: str | None = None) -> None:
        """
        Add a holiday to the calendar.
        """
        parsed = parse_date(value)
        self.holidays.add(parsed)

        if name is not None:
            self.holiday_names[parsed] = name

    def remove_holiday(self, value: DateLike) -> None:
        """
        Remove a holiday from the calendar.

        Raises
        ------
        KeyError
            If the holiday does not exist.
        """
        parsed = parse_date(value)
        self.holidays.remove(parsed)
        self.holiday_names.pop(parsed, None)

    def holiday_name(self, value: DateLike) -> str | None:
        """
        Return the holiday name, if one is available.
        """
        parsed = parse_date(value)
        return self.holiday_names.get(parsed)

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
