#!/usr/bin/env python3
"""Phase 6: Approach B — Age-group proportional share analysis (Secondary).

- Table 1: YTR by year × keyword
- YTR linear trend test (OLS on year)
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
PROPS_PATH = os.path.join(BASE_DIR, "data", "processed", "annual_age_proportions.csv")
YTR_PATH = os.path.join(BASE_DIR, "data", "processed", "ytr_timeseries.csv")
OUT_DIR = os.path.join(BASE_DIR, "output", "tables")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    ytr = pd.read_csv(YTR_PATH)
    props = pd.read_csv(PROPS_PATH)

    # Filter to gender=all for main tables
    ytr_all = ytr[ytr["gender"] == "all"].copy()

    print("=" * 60)
    print("APPROACH B: Age-Group Proportional Share (Secondary)")
    print("=" * 60)

    # ── Table 1: YTR by year × keyword ──
    table1 = ytr_all.pivot_table(index="year", columns="keyword", values="YTR")
    # Add mean across keywords
    table1["Mean"] = table1.mean(axis=1)

    table1_path = os.path.join(OUT_DIR, "table1_ytr_by_year_keyword.csv")
    table1.to_csv(table1_path, encoding="utf-8-sig")

    print("\nTable 1: Young-to-Traditional Ratio by Year × Keyword")
    print("-" * 80)
    print(table1.round(3).to_string())

    # ── YTR trend test ──
    print("\n\nYTR Linear Trend Tests:")
    print("-" * 60)

    keywords = sorted(ytr_all["keyword"].unique())
    trend_results = []

    for kw in keywords + ["_combined_"]:
        if kw == "_combined_":
            # Average YTR across keywords per year
            d = ytr_all.groupby("year")["YTR"].mean().reset_index()
            label = "All combined"
        else:
            d = ytr_all[ytr_all["keyword"] == kw][["year", "YTR"]].copy()
            label = kw

        X = sm.add_constant(d["year"])
        y = d["YTR"]
        model = sm.OLS(y, X).fit()

        slope = model.params["year"]
        p = model.pvalues["year"]
        r2 = model.rsquared

        trend_results.append({
            "keyword": label,
            "slope_per_year": slope,
            "p_value": p,
            "r_squared": r2,
            "ytr_2016": d[d["year"] == 2016]["YTR"].values[0] if len(d[d["year"] == 2016]) > 0 else np.nan,
            "ytr_2025": d[d["year"] == 2025]["YTR"].values[0] if len(d[d["year"] == 2025]) > 0 else np.nan,
        })

        sig = "*" if p < 0.05 else ""
        print(f"  {label:12s}: slope={slope:+.4f}/yr  P={p:.4f}{sig}  R²={r2:.3f}")

    trend_df = pd.DataFrame(trend_results)
    trend_path = os.path.join(OUT_DIR, "ytr_trend_tests.csv")
    trend_df.to_csv(trend_path, index=False, encoding="utf-8-sig")

    print(f"\nSaved: {table1_path}")
    print(f"Saved: {trend_path}")


if __name__ == "__main__":
    main()
