from __future__ import annotations

from datetime import date

import pandas as pd
import pytest

from br_market_calendar.io import read_anbima_csv, read_anbima_excel


def test_read_anbima_csv(tmp_path) -> None:
    path = tmp_path / "feriados.csv"

    df = pd.DataFrame(
        {
            "Data": ["01/01/2026", "25/12/2026"],
            "Feriado": ["Confraternização Universal", "Natal"],
        }
    )
    df.to_csv(path, sep=";", encoding="latin1", index=False)

    holidays = read_anbima_csv(path)

    assert holidays.is_holiday(date(2026, 1, 1)) is True
    assert holidays.is_holiday(date(2026, 12, 25)) is True
    assert holidays.is_holiday(date(2026, 1, 2)) is False


def test_read_anbima_csv_ignores_footer_rows(tmp_path) -> None:
    path = tmp_path / "feriados.csv"

    df = pd.DataFrame(
        {
            "Data": ["01/01/2026", "Fonte: ANBIMA"],
            "Feriado": ["ConfraternizaÃ§Ã£o Universal", None],
        }
    )
    df.to_csv(path, sep=";", encoding="latin1", index=False)

    holidays = read_anbima_csv(path)

    assert holidays.is_holiday(date(2026, 1, 1)) is True
    assert len(holidays) == 1


def test_read_anbima_csv_missing_date_column(tmp_path) -> None:
    path = tmp_path / "feriados.csv"

    df = pd.DataFrame({"Wrong": ["01/01/2026"]})
    df.to_csv(path, sep=";", encoding="latin1", index=False)

    with pytest.raises(ValueError, match="Date column"):
        read_anbima_csv(path)


def test_read_anbima_excel(tmp_path) -> None:
    path = tmp_path / "feriados.xlsx"

    df = pd.DataFrame(
        {
            "Data": ["01/01/2026", "25/12/2026"],
            "Feriado": ["Confraternização Universal", "Natal"],
        }
    )
    df.to_excel(path, index=False)

    holidays = read_anbima_excel(path)

    assert holidays.is_holiday(date(2026, 1, 1)) is True
    assert holidays.is_holiday(date(2026, 12, 25)) is True


def test_read_anbima_excel_ignores_footer_rows(tmp_path) -> None:
    path = tmp_path / "feriados.xlsx"

    df = pd.DataFrame(
        {
            "Data": ["01/01/2026", "Fonte: ANBIMA"],
            "Feriado": ["ConfraternizaÃ§Ã£o Universal", None],
        }
    )
    df.to_excel(path, index=False)

    holidays = read_anbima_excel(path)

    assert holidays.is_holiday(date(2026, 1, 1)) is True
    assert len(holidays) == 1


def test_read_anbima_excel_missing_date_column(tmp_path) -> None:
    path = tmp_path / "feriados.xlsx"

    df = pd.DataFrame({"Wrong": ["01/01/2026"]})
    df.to_excel(path, index=False)

    with pytest.raises(ValueError, match="Date column"):
        read_anbima_excel(path)
