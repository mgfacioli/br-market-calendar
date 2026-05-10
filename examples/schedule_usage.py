from __future__ import annotations

from br_market_calendar import (
    BrazilFinancialCalendar,
    BusinessDayConvention,
    DayCountConvention,
    Frequency,
    generate_schedule,
    year_fraction,
)


def main() -> None:
    cal = BrazilFinancialCalendar.from_holidays(
        [
            "2026-01-01",
            "2026-12-25",
        ]
    )

    schedule = generate_schedule(
        "2026-01-31",
        "2026-07-31",
        Frequency.MONTHLY,
        calendar=cal,
        convention=BusinessDayConvention.MODIFIED_FOLLOWING,
    )

    print("Schedule:")
    for schedule_date in schedule:
        print(schedule_date)

    print("ACT/252 year fractions between consecutive dates:")
    for start, end in zip(schedule, schedule[1:], strict=False):
        fraction = year_fraction(
            start,
            end,
            DayCountConvention.ACT_252,
            calendar=cal,
        )
        print(start, end, fraction)


if __name__ == "__main__":
    main()
