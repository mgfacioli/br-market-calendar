# br-market-calendar

Brazilian financial market calendar utilities for Python.

`br-market-calendar` provides a simple, explicit, and well-tested API for working
with Brazilian financial market dates, business days, holidays, day count
conventions, and financial schedules.

The project is designed for both Brazilian users and international users who
need reliable date utilities for the Brazilian market.

## Features

- Brazilian financial business day calendar
- ANBIMA-compatible holiday readers
- CSV, Excel, and URL holiday loading
- Business day adjustment conventions
- Day count conventions
- Financial schedule generation
- Date parsing and formatting helpers
- Calendar day and weekday ranges
- Business day ranges and business days per month
- First/last day of month and weekday name helpers
- Typed, tested, and lightweight core

## Installation

```bash
pip install br-market-calendar
```

## Quick examples

```python
from br_market_calendar import BrazilFinancialCalendar, date_range, days_between

cal = BrazilFinancialCalendar.from_holidays(["2026-01-01"])

# Calendar days
date_range("01/01/2026", "05/01/2026")

# Number of calendar days
days_between("2026-01-01", "2026-01-05", inclusive=True)

# Business days, excluding weekends and holidays
cal.business_days("2026-01-01", "2026-01-05")

# Number of business days
cal.business_days_between("2026-01-01", "2026-01-05", inclusive=True)

# Business days grouped by month
cal.business_days_per_month("2026-01-01", "2026-02-03")
```
