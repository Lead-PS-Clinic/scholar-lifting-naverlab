#!/usr/bin/env python3
"""Phase 3: Process raw Naver RSV data into analytic datasets.

1. Map age codes to 3 analytic groups (Young 20-34, Middle 35-44, Traditional 45+)
2. Compute group-level mean RSV per keyword/period/gender
3. Compute annual age-group proportional shares (Approach B)
4. Compute Young-to-Traditional Ratio (YTR)

Outputs:
- data/processed/rsv_by_keyword_agegroup_month.csv
- data/processed/annual_age_proportions.csv
- data/processed/ytr_timeseries.csv
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "naver_rsv_all.csv")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")

AGE_GROUP_MAP = {
    "3": "Young",    # 19-24
    "4": "Young",    # 25-29
    "5": "Young",    # 30-34
    "6": "Middle",   # 35-39
    "7": "Middle",   # 40-44
    "8": "Traditional",  # 45-49
    "9": "Traditional",  # 50-54
    "10": "Traditional", # 55-59
    "11": "Traditional", # 60+
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Load raw data
    df = pd.read_csv(RAW_PATH)
    df["period"] = pd.to_datetime(df["period"])
    print(f"Loaded {len(df)} rows from {RAW_PATH}")

    # ── Step 1: Age-specific rows only (exclude 'all') ──
    df_age = df[df["age_code"] != "all"].copy()
    df_age["age_code"] = df_age["age_code"].astype(str)
    df_age["age_group"] = df_age["age_code"].map(AGE_GROUP_MAP)

    # ── Step 2: Group-level mean RSV ──
    # Average RSV across age codes within each group
    rsv_grouped = (
        df_age.groupby(["keyword", "age_group", "gender", "period"])["ratio"]
        .mean()
        .reset_index()
    )
    rsv_grouped = rsv_grouped.rename(columns={"ratio": "mean_rsv"})
    rsv_grouped = rsv_grouped.sort_values(["keyword", "gender", "age_group", "period"])

    out1 = os.path.join(OUT_DIR, "rsv_by_keyword_agegroup_month.csv")
    rsv_grouped.to_csv(out1, index=False, encoding="utf-8-sig")
    print(f"\nSaved rsv_by_keyword_agegroup_month.csv: {rsv_grouped.shape}")

    # ── Step 3: Annual age-group proportional share ──
    rsv_grouped["year"] = rsv_grouped["period"].dt.year

    # Annual mean RSV per keyword × age_group × gender
    annual = (
        rsv_grouped.groupby(["keyword", "age_group", "gender", "year"])["mean_rsv"]
        .mean()
        .reset_index()
    )

    # Total RSV per keyword × gender × year (sum across age groups)
    annual_total = (
        annual.groupby(["keyword", "gender", "year"])["mean_rsv"]
        .sum()
        .reset_index()
        .rename(columns={"mean_rsv": "total_rsv"})
    )

    # Merge and compute proportion
    annual = annual.merge(annual_total, on=["keyword", "gender", "year"])
    annual["proportion"] = annual["mean_rsv"] / annual["total_rsv"]

    out2 = os.path.join(OUT_DIR, "annual_age_proportions.csv")
    annual.to_csv(out2, index=False, encoding="utf-8-sig")
    print(f"Saved annual_age_proportions.csv: {annual.shape}")

    # ── Step 4: Young-to-Traditional Ratio (YTR) ──
    # Pivot to get Young and Traditional proportions side by side
    ytr_data = annual[annual["age_group"].isin(["Young", "Traditional"])].copy()
    ytr_pivot = ytr_data.pivot_table(
        index=["keyword", "gender", "year"],
        columns="age_group",
        values="proportion",
    ).reset_index()

    ytr_pivot["YTR"] = ytr_pivot["Young"] / ytr_pivot["Traditional"]

    out3 = os.path.join(OUT_DIR, "ytr_timeseries.csv")
    ytr_pivot.to_csv(out3, index=False, encoding="utf-8-sig")
    print(f"Saved ytr_timeseries.csv: {ytr_pivot.shape}")

    # Summary
    print("\n── Summary ──")
    print(f"Keywords: {sorted(rsv_grouped['keyword'].unique())}")
    print(f"Age groups: {sorted(rsv_grouped['age_group'].unique())}")
    print(f"Genders: {sorted(rsv_grouped['gender'].unique())}")
    print(f"Years: {sorted(annual['year'].unique())}")

    # Show YTR trend for all keywords combined, gender=all
    ytr_all = ytr_pivot[ytr_pivot["gender"] == "all"]
    ytr_mean = ytr_all.groupby("year")["YTR"].mean()
    print(f"\nMean YTR across keywords (gender=all):")
    for year, val in ytr_mean.items():
        print(f"  {year}: {val:.3f}")


if __name__ == "__main__":
    main()
