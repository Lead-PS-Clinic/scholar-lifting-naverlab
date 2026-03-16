#!/usr/bin/env python3
"""Phase 7a: Joinpoint regression on YTR time series.

Segmented linear regression to detect breakpoints in the YTR trend.
Tests for 0, 1, and 2 joinpoints; selects best by BIC.

Includes both annual-level (primary) and monthly-level (sensitivity) analyses.
Monthly analysis addresses the concern of overfitting with only 10 annual points.
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from itertools import combinations

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
YTR_PATH = os.path.join(BASE_DIR, "data", "processed", "ytr_timeseries.csv")
GROUPED_PATH = os.path.join(BASE_DIR, "data", "processed", "rsv_by_keyword_agegroup_month.csv")
OUT_DIR = os.path.join(BASE_DIR, "output", "tables")


def fit_segmented(x_vals, y_vals, joinpoints):
    """Fit segmented linear regression with given joinpoints."""
    X_parts = [np.ones(len(x_vals)), x_vals.astype(float)]

    for jp in joinpoints:
        seg = np.maximum(x_vals.astype(float) - jp, 0)
        X_parts.append(seg)

    X = np.column_stack(X_parts)
    model = sm.OLS(y_vals, X).fit()
    return model


def run_annual_joinpoint(ytr_all):
    """Run joinpoint analysis on annual YTR data (primary)."""
    years = ytr_all["year"].values
    ytr_vals = ytr_all["YTR"].values

    candidates = list(range(2017, 2025))
    results = []

    # 0 joinpoints
    m0 = fit_segmented(years, ytr_vals, [])
    results.append({"n_joinpoints": 0, "joinpoints": [], "bic": m0.bic, "aic": m0.aic,
                     "r_squared": m0.rsquared, "model": m0})

    # 1 joinpoint
    best_1jp = None
    for jp in candidates:
        m = fit_segmented(years, ytr_vals, [jp])
        if best_1jp is None or m.bic < best_1jp["bic"]:
            best_1jp = {"n_joinpoints": 1, "joinpoints": [jp], "bic": m.bic, "aic": m.aic,
                        "r_squared": m.rsquared, "model": m}
    if best_1jp:
        results.append(best_1jp)

    # 2 joinpoints
    best_2jp = None
    for jp1, jp2 in combinations(candidates, 2):
        if jp2 - jp1 < 2:
            continue
        m = fit_segmented(years, ytr_vals, [jp1, jp2])
        if best_2jp is None or m.bic < best_2jp["bic"]:
            best_2jp = {"n_joinpoints": 2, "joinpoints": [jp1, jp2], "bic": m.bic, "aic": m.aic,
                        "r_squared": m.rsquared, "model": m}
    if best_2jp:
        results.append(best_2jp)

    return results, ytr_all


def compute_monthly_ytr(grouped_path):
    """Compute monthly YTR from grouped RSV data."""
    df = pd.read_csv(grouped_path)
    df["period"] = pd.to_datetime(df["period"])

    # Filter to gender=all, Young and Traditional only
    d = df[(df["gender"] == "all") &
           (df["age_group"].isin(["Young", "Traditional"]))].copy()

    # Mean across keywords per month × age_group
    monthly = d.groupby(["period", "age_group"])["mean_rsv"].mean().reset_index()
    pivot = monthly.pivot(index="period", columns="age_group", values="mean_rsv").reset_index()
    pivot["YTR"] = pivot["Young"] / pivot["Traditional"]
    pivot["time_numeric"] = (pivot["period"] - pivot["period"].min()).dt.days / 365.25 + 2016

    return pivot


def run_monthly_joinpoint(monthly_ytr):
    """Run joinpoint analysis on monthly YTR data (sensitivity)."""
    x_vals = monthly_ytr["time_numeric"].values
    y_vals = monthly_ytr["YTR"].values

    # Candidate joinpoints: 2017.0 to 2024.5, step 0.5
    candidates = [2016.5 + 0.5 * i for i in range(1, 18)]  # 2017.0 to 2024.5
    results = []

    # 0 joinpoints
    m0 = fit_segmented(x_vals, y_vals, [])
    results.append({"n_joinpoints": 0, "joinpoints": [], "bic": m0.bic, "aic": m0.aic,
                     "r_squared": m0.rsquared, "model": m0})

    # 1 joinpoint
    best_1jp = None
    for jp in candidates:
        m = fit_segmented(x_vals, y_vals, [jp])
        if best_1jp is None or m.bic < best_1jp["bic"]:
            best_1jp = {"n_joinpoints": 1, "joinpoints": [jp], "bic": m.bic, "aic": m.aic,
                        "r_squared": m.rsquared, "model": m}
    if best_1jp:
        results.append(best_1jp)

    # 2 joinpoints
    best_2jp = None
    for jp1, jp2 in combinations(candidates, 2):
        if jp2 - jp1 < 1.0:
            continue
        m = fit_segmented(x_vals, y_vals, [jp1, jp2])
        if best_2jp is None or m.bic < best_2jp["bic"]:
            best_2jp = {"n_joinpoints": 2, "joinpoints": [jp1, jp2], "bic": m.bic, "aic": m.aic,
                        "r_squared": m.rsquared, "model": m}
    if best_2jp:
        results.append(best_2jp)

    return results, monthly_ytr


def bootstrap_joinpoint_ci(ytr_all, n_bootstrap=2000, seed=42):
    """Bootstrap confidence intervals for joinpoint locations."""
    rng = np.random.default_rng(seed)
    years = ytr_all["year"].values
    ytr_vals = ytr_all["YTR"].values
    n = len(years)

    boot_jp1 = []
    boot_jp2 = []
    boot_n_jp = []

    for _ in range(n_bootstrap):
        # Resample residuals (parametric bootstrap)
        best_model = min(
            [{"jp": [], "m": fit_segmented(years, ytr_vals, [])}] +
            [{"jp": [jp], "m": fit_segmented(years, ytr_vals, [jp])}
             for jp in range(2017, 2025)] +
            [{"jp": [jp1, jp2], "m": fit_segmented(years, ytr_vals, [jp1, jp2])}
             for jp1, jp2 in combinations(range(2017, 2025), 2) if jp2 - jp1 >= 2],
            key=lambda x: x["m"].bic
        )
        residuals = ytr_vals - best_model["m"].fittedvalues
        boot_resid = rng.choice(residuals, size=n, replace=True)
        boot_y = best_model["m"].fittedvalues + boot_resid

        # Fit best model on bootstrap sample
        candidates = list(range(2017, 2025))
        best_boot = {"bic": np.inf, "jp": [], "n_jp": 0}

        m0 = fit_segmented(years, boot_y, [])
        if m0.bic < best_boot["bic"]:
            best_boot = {"bic": m0.bic, "jp": [], "n_jp": 0}

        for jp in candidates:
            m = fit_segmented(years, boot_y, [jp])
            if m.bic < best_boot["bic"]:
                best_boot = {"bic": m.bic, "jp": [jp], "n_jp": 1}

        for jp1, jp2 in combinations(candidates, 2):
            if jp2 - jp1 < 2:
                continue
            m = fit_segmented(years, boot_y, [jp1, jp2])
            if m.bic < best_boot["bic"]:
                best_boot = {"bic": m.bic, "jp": [jp1, jp2], "n_jp": 2}

        boot_n_jp.append(best_boot["n_jp"])
        if best_boot["n_jp"] >= 1:
            boot_jp1.append(best_boot["jp"][0])
        if best_boot["n_jp"] >= 2:
            boot_jp2.append(best_boot["jp"][1])

    results = {
        "n_bootstrap": n_bootstrap,
        "pct_0jp": sum(1 for x in boot_n_jp if x == 0) / n_bootstrap * 100,
        "pct_1jp": sum(1 for x in boot_n_jp if x == 1) / n_bootstrap * 100,
        "pct_2jp": sum(1 for x in boot_n_jp if x == 2) / n_bootstrap * 100,
    }
    if boot_jp1:
        results["jp1_median"] = np.median(boot_jp1)
        results["jp1_ci_lower"] = np.percentile(boot_jp1, 2.5)
        results["jp1_ci_upper"] = np.percentile(boot_jp1, 97.5)
    if boot_jp2:
        results["jp2_median"] = np.median(boot_jp2)
        results["jp2_ci_lower"] = np.percentile(boot_jp2, 2.5)
        results["jp2_ci_upper"] = np.percentile(boot_jp2, 97.5)

    return results


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    ytr = pd.read_csv(YTR_PATH)
    ytr_all = ytr[ytr["gender"] == "all"].groupby("year")["YTR"].mean().reset_index()

    # ── Annual joinpoint (primary) ──
    print("=" * 60)
    print("JOINPOINT REGRESSION ON YTR (ANNUAL — PRIMARY)")
    print("=" * 60)

    annual_results, _ = run_annual_joinpoint(ytr_all)

    for r in annual_results:
        print(f"\n{r['n_joinpoints']} joinpoint(s) at {r['joinpoints']}: "
              f"BIC={r['bic']:.3f}  AIC={r['aic']:.3f}  R²={r['r_squared']:.4f}")

    best_annual = min(annual_results, key=lambda x: x["bic"])
    print(f"\nBest model: {best_annual['n_joinpoints']} joinpoint(s) at {best_annual['joinpoints']}")
    print(best_annual["model"].summary())

    # Save annual results
    jp_info = pd.DataFrame([{
        "level": "annual",
        "n_joinpoints": r["n_joinpoints"],
        "joinpoints": str(r["joinpoints"]),
        "bic": r["bic"],
        "aic": r["aic"],
        "r_squared": r["r_squared"],
    } for r in annual_results])

    # Save predicted
    ytr_all["ytr_predicted"] = best_annual["model"].fittedvalues
    ytr_all["joinpoints"] = str(best_annual["joinpoints"])

    pred_path = os.path.join(OUT_DIR, "joinpoint_predicted.csv")
    ytr_all.to_csv(pred_path, index=False, encoding="utf-8-sig")

    # ── Monthly joinpoint (sensitivity) ──
    print("\n" + "=" * 60)
    print("JOINPOINT REGRESSION ON YTR (MONTHLY — SENSITIVITY)")
    print("=" * 60)
    print("(120 data points — addresses concern of overfitting with 10 annual points)")

    monthly_ytr = compute_monthly_ytr(GROUPED_PATH)
    monthly_results, _ = run_monthly_joinpoint(monthly_ytr)

    for r in monthly_results:
        print(f"\n{r['n_joinpoints']} joinpoint(s) at {[f'{jp:.1f}' for jp in r['joinpoints']]}: "
              f"BIC={r['bic']:.3f}  AIC={r['aic']:.3f}  R²={r['r_squared']:.4f}")

    best_monthly = min(monthly_results, key=lambda x: x["bic"])
    print(f"\nBest monthly model: {best_monthly['n_joinpoints']} joinpoint(s) "
          f"at {[f'{jp:.1f}' for jp in best_monthly['joinpoints']]}")

    # Save monthly results
    monthly_jp_info = pd.DataFrame([{
        "level": "monthly",
        "n_joinpoints": r["n_joinpoints"],
        "joinpoints": str([round(jp, 1) for jp in r["joinpoints"]]),
        "bic": r["bic"],
        "aic": r["aic"],
        "r_squared": r["r_squared"],
    } for r in monthly_results])

    # Combine and save
    all_jp = pd.concat([jp_info, monthly_jp_info], ignore_index=True)
    jp_path = os.path.join(OUT_DIR, "joinpoint_results.csv")
    all_jp.to_csv(jp_path, index=False, encoding="utf-8-sig")

    # Save monthly predicted for supplementary figure
    monthly_ytr["ytr_predicted"] = best_monthly["model"].fittedvalues
    monthly_pred_path = os.path.join(OUT_DIR, "joinpoint_monthly_predicted.csv")
    monthly_ytr.to_csv(monthly_pred_path, index=False, encoding="utf-8-sig")

    # ── Bootstrap CI for joinpoints ──
    print("\n" + "=" * 60)
    print("BOOTSTRAP CONFIDENCE INTERVALS FOR JOINPOINTS (n=2000)")
    print("=" * 60)

    boot_results = bootstrap_joinpoint_ci(ytr_all, n_bootstrap=2000)
    print(f"  Model selection frequency:")
    print(f"    0 joinpoints: {boot_results['pct_0jp']:.1f}%")
    print(f"    1 joinpoint:  {boot_results['pct_1jp']:.1f}%")
    print(f"    2 joinpoints: {boot_results['pct_2jp']:.1f}%")
    if "jp1_median" in boot_results:
        print(f"  Joinpoint 1: median={boot_results['jp1_median']:.0f}, "
              f"95% CI [{boot_results['jp1_ci_lower']:.0f}, {boot_results['jp1_ci_upper']:.0f}]")
    if "jp2_median" in boot_results:
        print(f"  Joinpoint 2: median={boot_results['jp2_median']:.0f}, "
              f"95% CI [{boot_results['jp2_ci_lower']:.0f}, {boot_results['jp2_ci_upper']:.0f}]")

    boot_df = pd.DataFrame([boot_results])
    boot_path = os.path.join(OUT_DIR, "joinpoint_bootstrap_ci.csv")
    boot_df.to_csv(boot_path, index=False, encoding="utf-8-sig")
    print(f"\nSaved: {boot_path}")

    # ── Concordance check ──
    print("\n" + "=" * 60)
    print("CONCORDANCE: Annual vs Monthly")
    print("=" * 60)
    print(f"  Annual:  {best_annual['n_joinpoints']} joinpoints at {best_annual['joinpoints']}")
    print(f"  Monthly: {best_monthly['n_joinpoints']} joinpoints at "
          f"{[round(jp, 1) for jp in best_monthly['joinpoints']]}")

    if best_annual["n_joinpoints"] == best_monthly["n_joinpoints"]:
        print("  → Same number of joinpoints selected — supports annual finding")
    else:
        print("  → Different structure detected — see discussion")

    print(f"\nSaved: {jp_path}")
    print(f"Saved: {pred_path}")
    print(f"Saved: {monthly_pred_path}")


if __name__ == "__main__":
    main()
