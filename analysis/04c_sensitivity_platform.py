#!/usr/bin/env python3
"""Sensitivity analysis: Platform migration adjustment.

Younger Korean users have increasingly migrated from Naver to Google/YouTube/
Instagram/TikTok. This script adjusts Young RSV upward by assumed annual
attrition rates (3%, 5%, 7%) and re-fits the interaction model to test
whether the maturation finding is robust to platform migration.

Logic:
  If young users leave Naver at rate r per year, their true search interest
  is underestimated. We inflate Young RSV by (1 + r)^(year - 2016) and
  re-run Approach A to see if β₃ remains negative.
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "rsv_by_keyword_agegroup_month.csv")
OUT_DIR = os.path.join(BASE_DIR, "output", "tables")

ATTRITION_RATES = [0.03, 0.05, 0.07]


def adjust_for_migration(df, attrition_rate):
    """Inflate Young RSV to compensate for assumed Naver attrition."""
    d = df.copy()
    d["period"] = pd.to_datetime(d["period"])
    d["year"] = d["period"].dt.year

    mask = d["age_group"] == "Young"
    years_elapsed = d.loc[mask, "year"] - 2016
    correction = (1 + attrition_rate) ** years_elapsed
    d.loc[mask, "mean_rsv"] = d.loc[mask, "mean_rsv"] * correction

    return d


def fit_model(df_kw, keyword_name):
    """Fit interaction model (same specification as primary analysis)."""
    d = df_kw[(df_kw["age_group"].isin(["Young", "Traditional"])) &
              (df_kw["gender"] == "all")].copy()

    d["period"] = pd.to_datetime(d["period"])
    d = d.sort_values(["age_group", "period"])

    min_date = d["period"].min()
    d["time"] = ((d["period"] - min_date).dt.days / 30.44).round().astype(int)
    d["young"] = (d["age_group"] == "Young").astype(int)
    d["time_x_young"] = d["time"] * d["young"]
    d["month"] = d["period"].dt.month
    month_dummies = pd.get_dummies(d["month"], prefix="m", drop_first=True, dtype=float)

    X = pd.concat([
        d[["time", "young", "time_x_young"]].reset_index(drop=True),
        month_dummies.reset_index(drop=True)
    ], axis=1)
    X = sm.add_constant(X)
    y = d["mean_rsv"].reset_index(drop=True)

    model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})

    return {
        "keyword": keyword_name,
        "beta1_time": model.params["time"],
        "beta3_interaction": model.params["time_x_young"],
        "beta3_se": model.bse["time_x_young"],
        "beta3_p": model.pvalues["time_x_young"],
        "beta3_ci_lower": model.conf_int().loc["time_x_young", 0],
        "beta3_ci_upper": model.conf_int().loc["time_x_young", 1],
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    df["period"] = pd.to_datetime(df["period"])
    keywords = sorted(df["keyword"].unique())

    print("=" * 70)
    print("SENSITIVITY ANALYSIS: Platform Migration Adjustment")
    print("=" * 70)
    print("\nAssumption: Young users leave Naver at r% per year,")
    print("so true Young RSV = observed × (1+r)^(year−2016)\n")

    all_results = []

    # Unadjusted baseline
    print("─── Unadjusted (baseline) ───")
    for kw in keywords:
        res = fit_model(df[df["keyword"] == kw], kw)
        res["attrition_rate"] = 0.0
        res["scenario"] = "Unadjusted"
        all_results.append(res)
        print(f"  {kw:12s}  β₃={res['beta3_interaction']:+.4f}  P={res['beta3_p']:.4f}")

    # Each attrition scenario
    for rate in ATTRITION_RATES:
        df_adj = adjust_for_migration(df, rate)
        label = f"{int(rate*100)}% annual attrition"
        print(f"\n─── {label} ───")
        print(f"  (Young RSV in 2025 inflated by ×{(1+rate)**9:.2f})")

        for kw in keywords:
            res = fit_model(df_adj[df_adj["keyword"] == kw], kw)
            res["attrition_rate"] = rate
            res["scenario"] = label
            all_results.append(res)
            print(f"  {kw:12s}  β₃={res['beta3_interaction']:+.4f}  P={res['beta3_p']:.4f}")

    results_df = pd.DataFrame(all_results)

    # BH-FDR within each scenario
    for scenario in results_df["scenario"].unique():
        mask = results_df["scenario"] == scenario
        reject, pvals_corr, _, _ = multipletests(
            results_df.loc[mask, "beta3_p"], alpha=0.05, method="fdr_bh"
        )
        results_df.loc[mask, "beta3_p_bh"] = pvals_corr
        results_df.loc[mask, "significant_bh"] = reject

    out_path = os.path.join(OUT_DIR, "sensitivity_platform_migration.csv")
    results_df.to_csv(out_path, index=False, encoding="utf-8-sig")

    # Summary
    print("\n" + "=" * 70)
    print("ROBUSTNESS SUMMARY")
    print("=" * 70)
    print(f"\n{'Keyword':12s}  {'Unadj':>8s}  {'3%/yr':>8s}  {'5%/yr':>8s}  {'7%/yr':>8s}")
    print("-" * 50)
    for kw in keywords:
        vals = []
        for rate in [0.0] + ATTRITION_RATES:
            row = results_df[(results_df["keyword"] == kw) &
                             (results_df["attrition_rate"] == rate)].iloc[0]
            sig = "*" if row["significant_bh"] else ""
            vals.append(f"{row['beta3_interaction']:+.3f}{sig}")
        print(f"{kw:12s}  {'  '.join(f'{v:>8s}' for v in vals)}")

    # Determine at what attrition rate the finding reverses
    print("\n── Reversal threshold ──")
    for kw in keywords:
        baseline = results_df[(results_df["keyword"] == kw) &
                              (results_df["attrition_rate"] == 0.0)].iloc[0]
        if baseline["beta3_interaction"] >= 0:
            print(f"  {kw}: baseline β₃ already ≥ 0, no maturation to reverse")
            continue

        reversed_at = None
        for rate in ATTRITION_RATES:
            row = results_df[(results_df["keyword"] == kw) &
                             (results_df["attrition_rate"] == rate)].iloc[0]
            if row["beta3_interaction"] >= 0 or not row["significant_bh"]:
                reversed_at = rate
                break

        if reversed_at:
            print(f"  {kw}: maturation becomes NS or reversed at {int(reversed_at*100)}%/yr attrition")
        else:
            print(f"  {kw}: maturation robust up to 7%/yr attrition")

    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
