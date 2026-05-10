from __future__ import annotations

from pathlib import Path

from br_market_calendar import BrazilFinancialCalendar


def main() -> None:
    csv_path = Path("data/feriados_nacionais.csv")

    if csv_path.exists():
        cal = BrazilFinancialCalendar.from_anbima_csv(csv_path)
    else:
        cal = BrazilFinancialCalendar.from_anbima_url()

    print("Is 2026-01-01 a business day?")
    print(cal.is_business_day("2026-01-01"))

    print("Next business day after 2026-01-01:")
    print(cal.next_business_day("2026-01-01"))


if __name__ == "__main__":
    main()
