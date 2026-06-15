from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

from br_market_calendar.conventions import BusinessDayConvention
from br_market_calendar.dates import date_range, first_day_of_month, is_weekday
from br_market_calendar.formatters import parse_date
from br_market_calendar.holidays import HolidayCalendar
from br_market_calendar.io import (
    ANBIMA_HOLIDAYS_URL,
    read_anbima_csv,
    read_anbima_excel,
    read_anbima_url,
)
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

    @classmethod
    def from_anbima_csv(cls, path: str | Path) -> BrazilFinancialCalendar:
        """
        Create a calendar from an ANBIMA-compatible CSV file.
        """
        return cls(holidays=read_anbima_csv(path))

    @classmethod
    def from_anbima_excel(cls, path: str | Path) -> BrazilFinancialCalendar:
        """
        Create a calendar from an ANBIMA Excel file.
        """
        return cls(holidays=read_anbima_excel(path))

    @classmethod
    def from_anbima_url(
        cls,
        url: str = ANBIMA_HOLIDAYS_URL,
    ) -> BrazilFinancialCalendar:
        """
        Create a calendar from the official ANBIMA holiday URL.
        """
        return cls(holidays=read_anbima_url(url))

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

    def calendar_days(
        self,
        start: DateLike,
        end: DateLike | None = None,
        *,
        days: int | None = None,
        inclusive: bool = True,
    ) -> list[date]:
        """
        Return calendar days in a period.
        """
        return date_range(start, end, days=days, inclusive=inclusive)

    def weekdays(
        self,
        start: DateLike,
        end: DateLike | None = None,
        *,
        days: int | None = None,
        inclusive: bool = True,
    ) -> list[date]:
        """
        Return Monday-Friday dates in a period, ignoring holidays.
        """
        return [
            current
            for current in self.calendar_days(
                start,
                end,
                days=days,
                inclusive=inclusive,
            )
            if is_weekday(current)
        ]

    def business_days(
        self,
        start: DateLike,
        end: DateLike | None = None,
        *,
        days: int | None = None,
        inclusive: bool = True,
    ) -> list[date]:
        """
        Return Brazilian financial business days in a period.
        """
        return [
            current
            for current in self.calendar_days(
                start,
                end,
                days=days,
                inclusive=inclusive,
            )
            if self.is_business_day(current)
        ]

    def holidays_between(
        self,
        start: DateLike,
        end: DateLike,
        *,
        inclusive: bool = True,
    ) -> OrderedDict[date, str]:
        """
        Return holidays in a period.

        If a holiday name is available, it is returned as the value. Otherwise,
        the ISO date is used as a fallback.
        """
        holidays = {
            current: self.holidays.holiday_name(current) or current.isoformat()
            for current in self.calendar_days(start, end, inclusive=inclusive)
            if self.is_holiday(current)
        }
        return OrderedDict(sorted(holidays.items(), key=lambda item: item[0]))

    def weekday_occurrences(
        self,
        start: DateLike,
        end: DateLike,
        weekday: int,
        *,
        inclusive: bool = True,
    ) -> list[date]:
        """
        Return all dates matching an ISO weekday in a period.

        Monday is 1 and Sunday is 7.
        """
        if weekday < 1 or weekday > 7:
            msg = "weekday must be an integer between 1 (Monday) and 7 (Sunday)."
            raise ValueError(msg)

        return [
            current
            for current in self.calendar_days(start, end, inclusive=inclusive)
            if current.isoweekday() == weekday
        ]

    def business_days_per_month(
        self,
        start: DateLike,
        end: DateLike,
        *,
        inclusive: bool = True,
    ) -> OrderedDict[str, int]:
        """
        Return the number of business days per month in a period.
        """
        counts: dict[str, int] = {}

        for current in self.business_days(start, end, inclusive=inclusive):
            key = first_day_of_month(current).strftime("%m/%Y")
            counts[key] = counts.get(key, 0) + 1

        return OrderedDict(sorted(counts.items(), key=lambda item: item[0]))

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
        self,
        value: DateLike,
        include_current: bool = False,
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

        By default, the start date is included and the end date is excluded.

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

    def adjust(
        self,
        value: DateLike,
        convention: BusinessDayConvention | str = BusinessDayConvention.FOLLOWING,
    ) -> date:
        """
        Adjust a date according to a business day convention.

        Supported conventions:

        - following
        - preceding
        - modified_following
        - modified_preceding
        - unadjusted
        """
        parsed = parse_date(value)
        convention = BusinessDayConvention(convention)

        if convention == BusinessDayConvention.UNADJUSTED:
            return parsed

        if self.is_business_day(parsed):
            return parsed

        if convention == BusinessDayConvention.FOLLOWING:
            return self.next_business_day(parsed)

        if convention == BusinessDayConvention.PRECEDING:
            return self.previous_business_day(parsed)

        if convention == BusinessDayConvention.MODIFIED_FOLLOWING:
            adjusted = self.next_business_day(parsed)

            if adjusted.month != parsed.month:
                return self.previous_business_day(parsed)

            return adjusted

        if convention == BusinessDayConvention.MODIFIED_PRECEDING:
            adjusted = self.previous_business_day(parsed)

            if adjusted.month != parsed.month:
                return self.next_business_day(parsed)

            return adjusted

        msg = f"Unsupported business day convention: {convention!r}"
        raise ValueError(msg)
