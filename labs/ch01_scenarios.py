"""CH01：假设数据下的经营现金流、有限寿命估值与敏感性。

金额单位：亿元；股数单位：亿股；每股价值单位：元。
本模块不估计任何真实政策效应或投资收益。
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def finite_number(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def load_case(path=None):
    path = Path(path) if path is not None else ROOT / "data/ch01_scenarios.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def operating_cashflows(years, initial_nwc, tax_rate):
    """逐年计算 EBIT、NOPAT、ΔNWC、FCFF；仅适用于本章正EBIT税制。"""
    tax_rate = finite_number(tax_rate, "tax_rate")
    if not 0 <= tax_rate <= 1:
        raise ValueError("tax_rate must be in [0, 1]")
    previous_nwc = finite_number(initial_nwc, "initial_nwc")
    if not years:
        raise ValueError("At least one year is required")
    results = []
    for expected_year, row in enumerate(years, start=1):
        if row["year"] != expected_year:
            raise ValueError("Years must be consecutive and begin at 1")
        revenue = finite_number(row["revenue"], "revenue")
        margin = finite_number(row["ebit_margin"], "ebit_margin")
        depreciation = finite_number(row["depreciation"], "depreciation")
        capex = finite_number(row["capex"], "capex")
        nwc = finite_number(row["operating_nwc"], "operating_nwc")
        if revenue < 0 or depreciation < 0 or capex < 0:
            raise ValueError("Revenue, depreciation and capex must be nonnegative")
        ebit = revenue * margin
        if ebit < 0:
            raise ValueError("Negative EBIT needs an explicit loss-tax model")
        nopat = ebit * (1 - tax_rate)
        delta_nwc = nwc - previous_nwc
        fcff = nopat + depreciation - capex - delta_nwc
        results.append({"year": expected_year, "ebit": ebit, "nopat": nopat,
                        "delta_nwc": delta_nwc, "fcff": fcff})
        previous_nwc = nwc
    return results


def present_value(cashflows, discount_rate, terminal_recovery=0.0):
    """各年末现金流现值；回收只在最后一年加一次，无持续经营终值。"""
    cashflows = [finite_number(x, "cashflow") for x in cashflows]
    if not cashflows:
        raise ValueError("Cashflows cannot be empty")
    discount_rate = finite_number(discount_rate, "discount_rate")
    if discount_rate <= -1:
        raise ValueError("discount_rate must be greater than -1")
    recovery = finite_number(terminal_recovery, "terminal_recovery")
    value = math.fsum(cf / (1 + discount_rate) ** year
                      for year, cf in enumerate(cashflows, start=1))
    return value + recovery / (1 + discount_rate) ** len(cashflows)


def equity_value(operating_value, debt, excess_cash):
    return (finite_number(operating_value, "operating_value")
            - finite_number(debt, "debt") + finite_number(excess_cash, "cash"))


def evaluate(case, scenario_name, discount_rate=None):
    common = case["common"]
    scenario = case["scenarios"][scenario_name]
    rows = operating_cashflows(scenario["years"], common["initial_operating_nwc"],
                               common["tax_rate"])
    rate = scenario["discount_rate"] if discount_rate is None else discount_rate
    value = present_value([row["fcff"] for row in rows], rate,
                          common["terminal_recovery"])
    equity = equity_value(value, common["debt_at_valuation"],
                          common["excess_cash_at_valuation"])
    shares = finite_number(common["shares"], "shares")
    if shares <= 0:
        raise ValueError("shares must be positive")
    return {"scenario": scenario_name, "rate": rate, "years": rows,
            "operating_value": value, "equity_value": equity,
            "value_per_share": equity / shares}


def main():
    case = load_case()
    print("假设数据；Y0估值；现金流于Y1—Y3年末；金额亿元，每股元。")
    for name in case["scenarios"]:
        result = evaluate(case, name)
        cashflows = ", ".join(f"{row['fcff']:.4f}" for row in result["years"])
        print(f"{name}: FCFF=[{cashflows}], "
              f"V={result['operating_value']:.6f}, "
              f"E={result['equity_value']:.6f}, "
              f"per_share={result['value_per_share']:.6f}")
    base = evaluate(case, "base")["operating_value"]
    rate_only = evaluate(case, "base", 0.09)["operating_value"]
    weak = evaluate(case, "weakness")["operating_value"]
    print(f"先利率后经营归因：利率={rate_only-base:.6f}, "
          f"经营={weak-rate_only:.6f}, 总变化={weak-base:.6f}")
    for rate in (0.08, 0.09, 0.10, 0.11, 0.12):
        print(f"基准经营、k={rate:.0%}: V={evaluate(case, 'base', rate)['operating_value']:.6f}")


if __name__ == "__main__":
    main()
