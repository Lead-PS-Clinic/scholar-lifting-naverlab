#!/usr/bin/env python3
"""Phase 5: Approach A — Interaction Model (Primary Analysis).

For each keyword:
  RSV_it = β0 + β1·Time + β2·Young + β3·(Time×Young) + Σγ_m·Month_m + ε

β3 > 0 with β1 > 0 → broadening (both grow, young faster)
β3 > 0 with β1 ≤ 0 → displacement (only young grows)
β3 < 0 with β1 > 0 → maturation (both grow, traditional faster)
β3 < 0 with β1 ≤ 0 → contraction (traditional declines, young declines faster)

Uses Newey-West HAC SE (maxlags=12).
Benjamini-Hochberg FDR correction across 6 keywords.
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "rsv_by_keyword_agegroup_month.csv")
OUT_DIR = os.path.join(BASE_DIR, "output", "tables")


def fit_interaction_model(df_kw, keyword_name):
    """Fit interaction model for one keyword, gender=all, Young vs Traditional."""
    # Filter to Young and Traditional, gender=all
    d = df_kw[(df_kw["age_group"].isin(["Young", "Traditional"])) &
              (df_kw["gender"] == "all")].copy()

    d["period"] = pd.to_datetime(d["period"])
    d = d.sort_values(["age_group", "period"])

    # Create variables
    min_date = d["period"].min()
    d["time"] = ((d["period"] - min_date).dt.days / 30.44).round().astype(int)  # months 0-119
    d["young"] = (d["age_group"] == "Young").astype(int)
    d["time_x_young"] = d["time"] * d["young"]

    # Monthly dummies (11 dummies, Jan=reference)
    d["month"] = d["period"].dt.month
    month_dummies = pd.get_dummies(d["month"], prefix="m", drop_first=True, dtype=float)

    # Design matrix
    X = pd.concat([
        d[["time", "young", "time_x_young"]].reset_index(drop=True),
        month_dummies.reset_index(drop=True)
    ], axis=1)
    X = sm.add_constant(X)
    y = d["mean_rsv"].reset_index(drop=True)

    # OLS with Newey-West HAC SE
    model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})

    # Extract key coefficients
    results = {
        "keyword": keyword_name,
        "beta1_time": model.params["time"],
        "beta1_se": model.bse["time"],
        "beta1_p": model.pvalues["time"],
        "beta2_young": model.params["young"],
        "beta2_se": model.bse["young"],
        "beta2_p": model.pvalues["young"],
        "beta3_interaction": model.params["time_x_young"],
        "beta3_se": model.bse["time_x_young"],
        "beta3_p": model.pvalues["time_x_young"],
        "beta3_ci_lower": model.conf_int().loc["time_x_young", 0],
        "beta3_ci_upper": model.conf_int().loc["time_x_young", 1],
        "r_squared": model.rsquared,
        "n_obs": model.nobs,
    }

    # Interpretation
    if results["beta1_time"] > 0 and results["beta3_interaction"] > 0:
        results["pattern"] = "Broadening"
    elif results["beta1_time"] <= 0 and results["beta3_interaction"] > 0:
        results["pattern"] = "Displacement"
    elif results["beta1_time"] > 0 and results["beta3_interaction"] < 0:
        results["pattern"] = "Maturation"
    elif results["beta1_time"] <= 0 and results["beta3_interaction"] < 0:
        results["pattern"] = "Contraction"
    else:
        results["pattern"] = "No differential"

    return results, model


def fit_gender_model(df_kw, keyword_name, gender):
    """Fit interaction model for one keyword, specific gender."""
    d = df_kw[(df_kw["age_group"].isin(["Young", "Traditional"])) &
              (df_kw["gender"] == gender)].copy()

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
        "gender": gender,
        "beta3_interaction": model.params["time_x_young"],
        "beta3_se": model.bse["time_x_young"],
        "beta3_p": model.pvalues["time_x_young"],
        "beta3_ci_lower": model.conf_int().loc["time_x_young", 0],
        "beta3_ci_upper": model.conf_int().loc["time_x_young", 1],
        "beta1_time": model.params["time"],
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    df["period"] = pd.to_datetime(df["period"])
    keywords = sorted(df["keyword"].unique())

    print("=" * 60)
    print("APPROACH A: Interaction Model (Primary Analysis)")
    print("=" * 60)

    # ── Table 2: Main results ──
    results_list = []
    for kw in keywords:
        df_kw = df[df["keyword"] == kw]
        res, model = fit_interaction_model(df_kw, kw)
        results_list.append(res)

    results_df = pd.DataFrame(results_list)

    # Benjamini-Hochberg FDR correction
    reject, pvals_corrected, _, _ = multipletests(
        results_df["beta3_p"], alpha=0.05, method="fdr_bh"
    )
    results_df["beta3_p_bh"] = pvals_corrected
    results_df["significant_bh"] = reject

    # Save Table 2
    table2_path = os.path.join(OUT_DIR, "table2_interaction_coefficients.csv")
    results_df.to_csv(table2_path, index=False, encoding="utf-8-sig")

    # Print results
    print("\nTable 2: Interaction Coefficients (β₃) by Keyword")
    print("-" * 60)
    for _, row in results_df.iterrows():
        sig = "*" if row["significant_bh"] else ""
        print(f"{row['keyword']:10s}  β₁={row['beta1_time']:+.4f}  "
              f"β₃={row['beta3_interaction']:+.4f} ({row['beta3_se']:.4f})  "
              f"95%CI [{row['beta3_ci_lower']:+.4f}, {row['beta3_ci_upper']:+.4f}]  "
              f"P={row['beta3_p']:.4f}  BH-P={row['beta3_p_bh']:.4f}{sig}  "
              f"→ {row['pattern']}")

    print(f"\nSaved: {table2_path}")

    # ── Table 3: Gender stratification ──
    print("\n" + "=" * 60)
    print("GENDER STRATIFICATION")
    print("=" * 60)

    gender_results = []
    for kw in keywords:
        df_kw = df[df["keyword"] == kw]
        for gender in ["f", "m"]:
            res = fit_gender_model(df_kw, kw, gender)
            gender_results.append(res)

    gender_df = pd.DataFrame(gender_results)

    # FDR correction within each gender
    for g in ["f", "m"]:
        mask = gender_df["gender"] == g
        reject, pvals_corrected, _, _ = multipletests(
            gender_df.loc[mask, "beta3_p"], alpha=0.05, method="fdr_bh"
        )
        gender_df.loc[mask, "beta3_p_bh"] = pvals_corrected
        gender_df.loc[mask, "significant_bh"] = reject

    table3_path = os.path.join(OUT_DIR, "table3_gender_stratification.csv")
    gender_df.to_csv(table3_path, index=False, encoding="utf-8-sig")

    print("\nTable 3: β₃ by Gender")
    print("-" * 60)
    for _, row in gender_df.iterrows():
        sig = "*" if row["significant_bh"] else ""
        print(f"{row['keyword']:10s}  {row['gender']}  "
              f"β₃={row['beta3_interaction']:+.4f} ({row['beta3_se']:.4f})  "
              f"P={row['beta3_p']:.4f}  BH-P={row['beta3_p_bh']:.4f}{sig}")

    print(f"\nSaved: {table3_path}")


if __name__ == "__main__":
    main()
