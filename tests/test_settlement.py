from __future__ import annotations

from datetime import date

import pytest

from br_market_calendar import (
    BrazilFinancialCalendar,
    BusinessDayConvention,
    settlement_date,
)


def test_settlement_d0_business_day() -> None:
    result = settlement_date("2026-01-02", lag=0)

    assert result == date(2026, 1, 2)


def test_settlement_d0_non_business_day_following() -> None:
    result = settlement_date("2026-01-03", lag=0)

    assert result == date(2026, 1, 5)


def test_settlement_d0_non_business_day_preceding() -> None:
    result = settlement_date(
        "2026-01-03",
        lag=0,
        convention=BusinessDayConvention.PRECEDING,
    )

    assert result == date(2026, 1, 2)


def test_settlement_d1_from_friday() -> None:
    result = settlement_date("2026-01-02", lag=1)

    assert result == date(2026, 1, 5)


def test_settlement_d2_from_friday() -> None:
    result = settlement_date("2026-01-02", lag=2)

    assert result == date(2026, 1, 6)


def test_settlement_with_holiday() -> None:
    cal = BrazilFinancialCalendar.from_holidays(["2026-01-05"])

    result = settlement_date(
        "2026-01-02",
        lag=1,
        calendar=cal,
    )

    assert result == date(2026, 1, 6)


def test_settlement_negative_lag_raises() -> None:
    with pytest.raises(ValueError, match="Settlement lag cannot be negative"):
        settlement_date("2026-01-02", lag=-1)
