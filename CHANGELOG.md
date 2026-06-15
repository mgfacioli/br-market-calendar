# Changelog

All notable changes to this project will be documented in this file.

## [0.2.2] - 2026-06-15

### Fixed

- Ignore non-date footer rows in ANBIMA CSV and Excel readers.
- Include `xlrd` in the `excel` extra for `.xls` files such as the official
  ANBIMA holiday URL.

## [0.2.1] - 2026-06-15

### Fixed

- Declare `python-dateutil` as a runtime dependency so fresh installations can
  import scheduling utilities successfully.

## [0.2.0] - 2026-06-15

### Added

- Calendar day range helpers inspired by the older FinDt project.
- Weekday range helpers for Monday-Friday periods.
- Brazilian financial business day range helper.
- Holiday lookup for a period.
- ISO weekday occurrence lookup for a period.
- Business day counts grouped by month.
- First day, last day, and weekday name helpers.
- Root package exports for the new date helpers.
- README examples for calendar days, business days, and monthly business day counts.

### Changed

- Date parsing now accepts day-first strings with non-digit separators, such as
  `31-01-2026`, `31:01:2026`, and `31 01 2026`.

## [0.1.0] - 2026-05-10

### Added

- Core date parsing and formatting utilities.
- Brazilian financial calendar.
- Holiday calendar abstraction.
- ANBIMA-compatible CSV, Excel, and URL holiday readers.
- Business day conventions:
  - following
  - preceding
  - modified following
  - modified preceding
  - unadjusted
- Day count conventions:
  - ACT/252
  - BUS/252
  - ACT/360
  - ACT/365
  - 30/360
- Financial schedule generation.
- End-of-month schedule rule.
- Settlement date calculation.
- Usage examples and initial README documentation.
- Test suite with pytest.
- Type checking with mypy.
- Linting and formatting with ruff.
