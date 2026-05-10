from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from br_market_calendar.dates import is_weekday
from br_market_calendar.formatters import parse_date
from br_market_calendar.holidays import HolidayCalendar
from br_market_calendar.types import DateLike


@dataclass(slots=True)
class BrazilFinancialCalendar:
    """
    Brazilian financial calendar.

    A business day is defined as a weekday that is not a holiday.
    """

    holidays: HolidayCalendar = field(default_factory=HolidayCalendar)

    @classmethod
    def from_holidays(cls, holidays: list[DateLike]) -> BrazilFinancialCalendar:
        """
        Create a calendar from a list of holidays.
        """
        return cls(holidays=HolidayCalendar.from_iterable(holidays))

    def is_holiday(self, value: DateLike) -> bool:
        """
        Return True if the date is a holiday.
        """
        return self.holidays.is_holiday(value)

    def is_business_day(self, value: DateLike) -> bool:
        """
        Return True if the date is a Brazilian financial business day.
        """
        return is_weekday(value) and not self.is_holiday(value)

    def is_non_business_day(self, value: DateLike) -> bool:
        """
        Return True if the date is not a business day.
        """
        return not self.is_business_day(value)

    def next_business_day(self, value: DateLike, include_current: bool = False) -> date:
        """
        Return the next business day.

        Parameters
        ----------
        value:
            Reference date.
        include_current:
            If True and value is already a business day, return value.
        """
        current = parse_date(value)

        if include_current and self.is_business_day(current):
            return current

        current += timedelta(days=1)

        while not self.is_business_day(current):
            current += timedelta(days=1)

        return current

    def previous_business_day(
        self, value: DateLike, include_current: bool = False
    ) -> date:
        """
        Return the previous business day.

        Parameters
        ----------
        value:
            Reference date.
        include_current:
            If True and value is already a business day, return value.
        """
        current = parse_date(value)

        if include_current and self.is_business_day(current):
            return current

        current -= timedelta(days=1)

        while not self.is_business_day(current):
            current -= timedelta(days=1)

        return current

    def add_business_days(self, value: DateLike, days: int) -> date:
        """
        Add business days to a date.

        If days is positive, move forward.
        If days is negative, move backward.
        If days is zero, return the parsed date unchanged.
        """
        current = parse_date(value)

        if days == 0:
            return current

        step = 1 if days > 0 else -1
        remaining = abs(days)

        while remaining:
            current += timedelta(days=step)

            if self.is_business_day(current):
                remaining -= 1

        return current

    def business_days_between(
        self,
        start: DateLike,
        end: DateLike,
        inclusive: bool = False,
    ) -> int:
        """
        Return the number of business days between two dates.

        By default, the start date is included and the end date is excluded,
        following the common convention used by Python date ranges.

        If inclusive=True, both start and end dates are considered.
        """
        start_date = parse_date(start)
        end_date = parse_date(end)

        if start_date == end_date:
            if inclusive and self.is_business_day(start_date):
                return 1
            return 0

        step = 1 if end_date > start_date else -1
        count = 0
        current = start_date

        while current != end_date:
            if self.is_business_day(current):
                count += step

            current += timedelta(days=step)

        if inclusive and self.is_business_day(end_date):
            count += step

        return count
