from __future__ import annotations

from datetime import date

import pandas as pd

from br_market_calendar import BrazilFinancialCalendar


def test_calendar_from_anbima_csv(tmp_path) -> None:
    path = tmp_path / "feriados.csv"

    df = pd.DataFrame(
        {
            "Data": ["01/01/2026"],
            "Feriado": ["Confraternização Universal"],
        }
    )
    df.to_csv(path, sep=";", encoding="latin1", index=False)

    cal = BrazilFinancialCalendar.from_anbima_csv(path)

    assert cal.is_business_day(date(2026, 1, 1)) is False
    assert cal.is_business_day(date(2026, 1, 2)) is True


def test_calendar_from_anbima_excel(tmp_path) -> None:
    path = tmp_path / "feriados.xlsx"

    df = pd.DataFrame(
        {
            "Data": ["01/01/2026"],
            "Feriado": ["Confraternização Universal"],
        }
    )
    df.to_excel(path, index=False)

    cal = BrazilFinancialCalendar.from_anbima_excel(path)

    assert cal.is_business_day(date(2026, 1, 1)) is False
    assert cal.is_business_day(date(2026, 1, 2)) is True
