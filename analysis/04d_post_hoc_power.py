#!/usr/bin/env python3
"""Post-hoc power analysis for non-significant keywords.

Computes the minimum detectable effect size (MDES) for each keyword
at 80% power and α=0.05, and compares with observed β₃ to determine
whether non-significance reflects true null or insufficient power.
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "rsv_by_keyword_agegroup_month.csv")
TABLE2_PATH = os.path.join(BASE_DIR, "output", "tables", "table2_interaction_coefficients.csv")
OUT_DIR = os.path.join(BASE_DIR, "output", "tables")


def compute_mdes(n_obs, se_beta3, alpha=0.05, power=0.80):
    """Compute minimum detectable effect size at given power.

    MDES = (z_{1-alpha/2} + z_{power}) * SE
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    return (z_alpha + z_power) * se_beta3


def compute_observed_power(beta3, se_beta3, alpha=0.05):
    """Compute observed (post-hoc) power for the given effect size."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_stat = abs(beta3) / se_beta3
    power = stats.norm.cdf(z_stat - z_alpha) + stats.norm.cdf(-z_stat - z_alpha)
    return power


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    table2 = pd.read_csv(TABLE2_PATH)

    print("=" * 70)
    print("POST-HOC POWER ANALYSIS")
    print("=" * 70)

    results = []
    for _, row in table2.iterrows():
        mdes = compute_mdes(row["n_obs"], row["beta3_se"])
        obs_power = compute_observed_power(row["beta3_interaction"], row["beta3_se"])

        res = {
            "keyword": row["keyword"],
            "beta3_observed": row["beta3_interaction"],
            "beta3_se": row["beta3_se"],
            "n_obs": int(row["n_obs"]),
            "mdes_80pct": mdes,
            "observed_power": obs_power,
            "significant_bh": row["significant_bh"],
        }
        results.append(res)

        sig_label = "SIG" if row["significant_bh"] else "NS"
        print(f"  {row['keyword']:12s}  β₃={row['beta3_interaction']:+.4f}  "
              f"SE={row['beta3_se']:.4f}  MDES(80%)={mdes:.4f}  "
              f"Power={obs_power:.3f}  [{sig_label}]")

    results_df = pd.DataFrame(results)
    out_path = os.path.join(OUT_DIR, "post_hoc_power.csv")
    results_df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"\nInterpretation:")
    ns_keywords = results_df[~results_df["significant_bh"]]
    for _, row in ns_keywords.iterrows():
        if abs(row["beta3_observed"]) < row["mdes_80pct"]:
            print(f"  {row['keyword']}: |β₃|={abs(row['beta3_observed']):.4f} < MDES={row['mdes_80pct']:.4f} "
                  f"→ effect too small to detect at 80% power")
        else:
            print(f"  {row['keyword']}: |β₃|={abs(row['beta3_observed']):.4f} ≥ MDES={row['mdes_80pct']:.4f} "
                  f"→ adequate power, likely true null")

    # Compute: what sample size would be needed to detect the average NS effect?
    avg_ns_effect = ns_keywords["beta3_observed"].abs().mean()
    avg_ns_se = ns_keywords["beta3_se"].mean()
    z_alpha = stats.norm.ppf(0.975)
    z_power = stats.norm.ppf(0.80)
    # Required n proportional to (SE_required)^2, where SE_required = |effect| / (z_a + z_p)
    se_required = avg_ns_effect / (z_alpha + z_power)
    # SE scales with 1/sqrt(n), so n_required = n_current * (current_se / required_se)^2
    avg_n = ns_keywords["n_obs"].mean()
    n_required = avg_n * (avg_ns_se / se_required) ** 2

    print(f"\n  Average NS |β₃| = {avg_ns_effect:.4f}, average SE = {avg_ns_se:.4f}")
    print(f"  To detect this effect at 80% power: ~{int(n_required)} observations per keyword needed")
    print(f"  (Current: ~{int(avg_n)} per keyword)")

    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
