from __future__ import annotations

from br_market_calendar import BrazilFinancialCalendar


def main() -> None:
    cal = BrazilFinancialCalendar.from_holidays(
        [
            "2026-01-01",
            "2026-12-25",
        ]
    )

    print("Is 2026-01-02 a business day?")
    print(cal.is_business_day("2026-01-02"))

    print("Is 2026-01-01 a business day?")
    print(cal.is_business_day("2026-01-01"))

    print("Next business day after 2026-01-01:")
    print(cal.next_business_day("2026-01-01"))

    print("Previous business day before 2026-01-03:")
    print(cal.previous_business_day("2026-01-03"))

    print("Add 10 business days to 2026-01-02:")
    print(cal.add_business_days("2026-01-02", 10))

    print("Business days between 2026-01-01 and 2026-01-31:")
    print(cal.business_days_between("2026-01-01", "2026-01-31"))


if __name__ == "__main__":
    main()
