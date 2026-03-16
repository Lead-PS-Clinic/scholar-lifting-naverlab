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

Model diagnostics: Durbin-Watson, Ljung-Box Q(12).
Sensitivity analyses: Prais-Winsten GLS, Fourier terms (2 sine-cosine pairs).
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.multitest import multipletests

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "rsv_by_keyword_agegroup_month.csv")
OUT_DIR = os.path.join(BASE_DIR, "output", "tables")


def _prepare_data(df_kw, gender="all"):
    """Prepare data for Young vs Traditional interaction model."""
    d = df_kw[(df_kw["age_group"].isin(["Young", "Traditional"])) &
              (df_kw["gender"] == gender)].copy()

    d["period"] = pd.to_datetime(d["period"])
    d = d.sort_values(["age_group", "period"])

    min_date = d["period"].min()
    d["time"] = ((d["period"] - min_date).dt.days / 30.44).round().astype(int)
    d["young"] = (d["age_group"] == "Young").astype(int)
    d["time_x_young"] = d["time"] * d["young"]
    d["month"] = d["period"].dt.month

    return d


def _build_design_monthly_dummies(d):
    """Build design matrix with 11 monthly dummies (Jan=reference)."""
    month_dummies = pd.get_dummies(d["month"], prefix="m", drop_first=True, dtype=float)
    X = pd.concat([
        d[["time", "young", "time_x_young"]].reset_index(drop=True),
        month_dummies.reset_index(drop=True)
    ], axis=1)
    X = sm.add_constant(X)
    y = d["mean_rsv"].reset_index(drop=True)
    return X, y


def _build_design_fourier(d, n_pairs=2):
    """Build design matrix with Fourier terms instead of monthly dummies."""
    fourier_cols = {}
    for k in range(1, n_pairs + 1):
        fourier_cols[f"sin_{k}"] = np.sin(2 * np.pi * k * d["month"].values / 12)
        fourier_cols[f"cos_{k}"] = np.cos(2 * np.pi * k * d["month"].values / 12)
    fourier_df = pd.DataFrame(fourier_cols)

    X = pd.concat([
        d[["time", "young", "time_x_young"]].reset_index(drop=True),
        fourier_df.reset_index(drop=True)
    ], axis=1)
    X = sm.add_constant(X)
    y = d["mean_rsv"].reset_index(drop=True)
    return X, y


def _classify_pattern(beta1, beta3):
    if beta1 > 0 and beta3 > 0:
        return "Broadening"
    elif beta1 <= 0 and beta3 > 0:
        return "Displacement"
    elif beta1 > 0 and beta3 < 0:
        return "Maturation"
    elif beta1 <= 0 and beta3 < 0:
        return "Contraction"
    return "No differential"


def _extract_results(model, keyword_name, method_label="OLS_HAC"):
    """Extract key coefficients and diagnostics from a fitted model."""
    resid = model.resid.values
    dw = durbin_watson(resid)

    try:
        lb = acorr_ljungbox(resid, lags=[12], return_df=True)
        lb_q = lb["lb_stat"].values[0]
        lb_p = lb["lb_pvalue"].values[0]
    except Exception:
        lb_q, lb_p = np.nan, np.nan

    results = {
        "keyword": keyword_name,
        "method": method_label,
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
        "n_obs": int(model.nobs),
        "durbin_watson": dw,
        "ljung_box_q12": lb_q,
        "ljung_box_p12": lb_p,
    }
    results["pattern"] = _classify_pattern(results["beta1_time"], results["beta3_interaction"])
    return results


def fit_interaction_model(df_kw, keyword_name):
    """Fit primary OLS + Newey-West HAC model."""
    d = _prepare_data(df_kw, "all")
    X, y = _build_design_monthly_dummies(d)
    model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
    return _extract_results(model, keyword_name, "OLS_HAC"), model


def fit_prais_winsten(df_kw, keyword_name):
    """Prais-Winsten GLS sensitivity analysis for AR(1) autocorrelation."""
    d = _prepare_data(df_kw, "all")
    X, y = _build_design_monthly_dummies(d)

    model = sm.GLSAR(y, X, rho=1).iterative_fit(maxiter=50)
    results = {
        "keyword": keyword_name,
        "method": "Prais-Winsten",
        "beta3_interaction": model.params["time_x_young"],
        "beta3_se": model.bse["time_x_young"],
        "beta3_p": model.pvalues["time_x_young"],
        "beta3_ci_lower": model.conf_int().loc["time_x_young", 0],
        "beta3_ci_upper": model.conf_int().loc["time_x_young", 1],
        "r_squared": model.rsquared,
        "rho": model.rho if hasattr(model, "rho") else np.nan,
        "beta1_time": model.params["time"],
    }
    results["pattern"] = _classify_pattern(results["beta1_time"], results["beta3_interaction"])
    return results


def fit_fourier_model(df_kw, keyword_name):
    """Fourier terms sensitivity analysis (2 sine-cosine pairs)."""
    d = _prepare_data(df_kw, "all")
    X, y = _build_design_fourier(d, n_pairs=2)
    model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
    results = {
        "keyword": keyword_name,
        "method": "Fourier",
        "beta3_interaction": model.params["time_x_young"],
        "beta3_se": model.bse["time_x_young"],
        "beta3_p": model.pvalues["time_x_young"],
        "beta3_ci_lower": model.conf_int().loc["time_x_young", 0],
        "beta3_ci_upper": model.conf_int().loc["time_x_young", 1],
        "r_squared": model.rsquared,
        "beta1_time": model.params["time"],
    }
    results["pattern"] = _classify_pattern(results["beta1_time"], results["beta3_interaction"])
    return results


def fit_gender_model(df_kw, keyword_name, gender):
    """Fit interaction model for one keyword, specific gender."""
    d = _prepare_data(df_kw, gender)
    X, y = _build_design_monthly_dummies(d)
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

    print("=" * 70)
    print("APPROACH A: Interaction Model (Primary Analysis)")
    print("=" * 70)

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

    print("\nTable 2: Interaction Coefficients (β₃) by Keyword")
    print("-" * 70)
    for _, row in results_df.iterrows():
        sig = "*" if row["significant_bh"] else ""
        print(f"{row['keyword']:10s}  β₁={row['beta1_time']:+.4f}  "
              f"β₃={row['beta3_interaction']:+.4f} ({row['beta3_se']:.4f})  "
              f"95%CI [{row['beta3_ci_lower']:+.4f}, {row['beta3_ci_upper']:+.4f}]  "
              f"P={row['beta3_p']:.4f}  BH-P={row['beta3_p_bh']:.4f}{sig}  "
              f"→ {row['pattern']}")

    # Diagnostics summary
    print("\nModel Diagnostics:")
    print("-" * 70)
    for _, row in results_df.iterrows():
        dw_flag = " ⚠" if row["durbin_watson"] < 1.5 else ""
        lb_flag = " ⚠" if row["ljung_box_p12"] < 0.05 else ""
        print(f"{row['keyword']:10s}  DW={row['durbin_watson']:.3f}{dw_flag}  "
              f"LB-Q(12)={row['ljung_box_q12']:.2f}  LB-P={row['ljung_box_p12']:.4f}{lb_flag}")

    print(f"\nSaved: {table2_path}")

    # ── Sensitivity: Prais-Winsten GLS ──
    print("\n" + "=" * 70)
    print("SENSITIVITY ANALYSIS: Prais-Winsten GLS")
    print("=" * 70)

    pw_results = []
    for kw in keywords:
        df_kw = df[df["keyword"] == kw]
        res = fit_prais_winsten(df_kw, kw)
        pw_results.append(res)

    pw_df = pd.DataFrame(pw_results)
    reject_pw, pvals_pw, _, _ = multipletests(pw_df["beta3_p"], alpha=0.05, method="fdr_bh")
    pw_df["beta3_p_bh"] = pvals_pw
    pw_df["significant_bh"] = reject_pw

    pw_path = os.path.join(OUT_DIR, "sensitivity_prais_winsten.csv")
    pw_df.to_csv(pw_path, index=False, encoding="utf-8-sig")

    for _, row in pw_df.iterrows():
        sig = "*" if row["significant_bh"] else ""
        print(f"{row['keyword']:10s}  β₃={row['beta3_interaction']:+.4f} ({row['beta3_se']:.4f})  "
              f"P={row['beta3_p']:.4f}  BH-P={row['beta3_p_bh']:.4f}{sig}  → {row['pattern']}")

    print(f"\nSaved: {pw_path}")

    # ── Sensitivity: Fourier terms ──
    print("\n" + "=" * 70)
    print("SENSITIVITY ANALYSIS: Fourier Terms (2 sine-cosine pairs)")
    print("=" * 70)

    fourier_results = []
    for kw in keywords:
        df_kw = df[df["keyword"] == kw]
        res = fit_fourier_model(df_kw, kw)
        fourier_results.append(res)

    fourier_df = pd.DataFrame(fourier_results)
    reject_f, pvals_f, _, _ = multipletests(fourier_df["beta3_p"], alpha=0.05, method="fdr_bh")
    fourier_df["beta3_p_bh"] = pvals_f
    fourier_df["significant_bh"] = reject_f

    fourier_path = os.path.join(OUT_DIR, "sensitivity_fourier.csv")
    fourier_df.to_csv(fourier_path, index=False, encoding="utf-8-sig")

    for _, row in fourier_df.iterrows():
        sig = "*" if row["significant_bh"] else ""
        print(f"{row['keyword']:10s}  β₃={row['beta3_interaction']:+.4f} ({row['beta3_se']:.4f})  "
              f"P={row['beta3_p']:.4f}  BH-P={row['beta3_p_bh']:.4f}{sig}  → {row['pattern']}")

    print(f"\nSaved: {fourier_path}")

    # ── Concordance summary ──
    print("\n" + "=" * 70)
    print("SENSITIVITY CONCORDANCE SUMMARY")
    print("=" * 70)
    print(f"{'Keyword':12s}  {'OLS-HAC':12s}  {'Prais-Winsten':14s}  {'Fourier':12s}")
    print("-" * 55)
    for i, kw in enumerate(keywords):
        main_sig = "Sig*" if results_df.iloc[i]["significant_bh"] else "NS"
        pw_sig = "Sig*" if pw_df.iloc[i]["significant_bh"] else "NS"
        f_sig = "Sig*" if fourier_df.iloc[i]["significant_bh"] else "NS"
        main_b3 = results_df.iloc[i]["beta3_interaction"]
        pw_b3 = pw_df.iloc[i]["beta3_interaction"]
        f_b3 = fourier_df.iloc[i]["beta3_interaction"]
        print(f"{kw:12s}  {main_b3:+.3f} {main_sig:4s}  {pw_b3:+.3f} {pw_sig:4s}      {f_b3:+.3f} {f_sig:4s}")

    # ── Table 3: Gender stratification ──
    print("\n" + "=" * 70)
    print("GENDER STRATIFICATION")
    print("=" * 70)

    gender_results = []
    for kw in keywords:
        df_kw = df[df["keyword"] == kw]
        for gender in ["f", "m"]:
            res = fit_gender_model(df_kw, kw, gender)
            gender_results.append(res)

    gender_df = pd.DataFrame(gender_results)

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
    print("-" * 70)
    for _, row in gender_df.iterrows():
        sig = "*" if row["significant_bh"] else ""
        print(f"{row['keyword']:10s}  {row['gender']}  "
              f"β₃={row['beta3_interaction']:+.4f} ({row['beta3_se']:.4f})  "
              f"P={row['beta3_p']:.4f}  BH-P={row['beta3_p_bh']:.4f}{sig}")

    print(f"\nSaved: {table3_path}")


if __name__ == "__main__":
    main()
