#!/usr/bin/env python3
"""Phase 7a: Joinpoint regression on YTR time series.

Segmented linear regression to detect breakpoints in the YTR trend.
Tests for 0, 1, and 2 joinpoints; selects best by BIC.
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from itertools import combinations

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
YTR_PATH = os.path.join(BASE_DIR, "data", "processed", "ytr_timeseries.csv")
OUT_DIR = os.path.join(BASE_DIR, "output", "tables")


def fit_segmented(years, ytr, joinpoints):
    """Fit segmented linear regression with given joinpoints."""
    X_parts = [np.ones(len(years)), years.astype(float)]

    for jp in joinpoints:
        seg = np.maximum(years.astype(float) - jp, 0)
        X_parts.append(seg)

    X = np.column_stack(X_parts)
    model = sm.OLS(ytr, X).fit()
    return model


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    ytr = pd.read_csv(YTR_PATH)
    # Use mean YTR across keywords, gender=all
    ytr_all = ytr[ytr["gender"] == "all"].groupby("year")["YTR"].mean().reset_index()

    years = ytr_all["year"].values
    ytr_vals = ytr_all["YTR"].values

    print("=" * 60)
    print("JOINPOINT REGRESSION ON YTR")
    print("=" * 60)

    # Candidate joinpoints: 2017-2024 (interior years)
    candidates = list(range(2017, 2025))

    results = []

    # 0 joinpoints (simple linear)
    m0 = fit_segmented(years, ytr_vals, [])
    results.append({"n_joinpoints": 0, "joinpoints": [], "bic": m0.bic, "aic": m0.aic, "model": m0})
    print(f"\n0 joinpoints: BIC={m0.bic:.3f}  AIC={m0.aic:.3f}")

    # 1 joinpoint
    best_1jp = None
    for jp in candidates:
        m = fit_segmented(years, ytr_vals, [jp])
        if best_1jp is None or m.bic < best_1jp["bic"]:
            best_1jp = {"n_joinpoints": 1, "joinpoints": [jp], "bic": m.bic, "aic": m.aic, "model": m}
    if best_1jp:
        results.append(best_1jp)
        print(f"1 joinpoint ({best_1jp['joinpoints']}): BIC={best_1jp['bic']:.3f}  AIC={best_1jp['aic']:.3f}")

    # 2 joinpoints
    best_2jp = None
    for jp1, jp2 in combinations(candidates, 2):
        if jp2 - jp1 < 2:
            continue
        m = fit_segmented(years, ytr_vals, [jp1, jp2])
        if best_2jp is None or m.bic < best_2jp["bic"]:
            best_2jp = {"n_joinpoints": 2, "joinpoints": [jp1, jp2], "bic": m.bic, "aic": m.aic, "model": m}
    if best_2jp:
        results.append(best_2jp)
        print(f"2 joinpoints ({best_2jp['joinpoints']}): BIC={best_2jp['bic']:.3f}  AIC={best_2jp['aic']:.3f}")

    # Select best model
    best = min(results, key=lambda x: x["bic"])
    print(f"\nBest model: {best['n_joinpoints']} joinpoint(s) at {best['joinpoints']}")
    print(f"Model summary:")
    print(best["model"].summary())

    # Save joinpoint info
    jp_info = pd.DataFrame([{
        "n_joinpoints": r["n_joinpoints"],
        "joinpoints": str(r["joinpoints"]),
        "bic": r["bic"],
        "aic": r["aic"],
    } for r in results])

    jp_path = os.path.join(OUT_DIR, "joinpoint_results.csv")
    jp_info.to_csv(jp_path, index=False, encoding="utf-8-sig")

    # Save predicted values for plotting
    best_model = best["model"]
    ytr_all["ytr_predicted"] = best_model.fittedvalues
    ytr_all["joinpoints"] = str(best["joinpoints"])

    pred_path = os.path.join(OUT_DIR, "joinpoint_predicted.csv")
    ytr_all.to_csv(pred_path, index=False, encoding="utf-8-sig")

    print(f"\nSaved: {jp_path}")
    print(f"Saved: {pred_path}")


if __name__ == "__main__":
    main()
