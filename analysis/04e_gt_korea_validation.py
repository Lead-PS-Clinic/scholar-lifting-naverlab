#!/usr/bin/env python3
"""Cross-validate Naver RSV trends with Google Trends Korea data.

Computes Spearman correlation between monthly all-age Naver RSV and GT Korea RSV
for each keyword. High correlation supports the interpretation that Naver trends
reflect genuine search behavior rather than platform-specific artifacts.
"""

import os
import pandas as pd
import numpy as np
from scipy import stats

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
NAVER_PATH = os.path.join(BASE_DIR, "data", "raw", "naver_rsv_all.csv")
GT_PATH = os.path.join(BASE_DIR, "data", "raw", "gt_korea_lifting.csv")
OUT_DIR = os.path.join(BASE_DIR, "output", "tables")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    naver = pd.read_csv(NAVER_PATH)
    naver["period"] = pd.to_datetime(naver["period"])
    gt = pd.read_csv(GT_PATH)
    gt["date"] = pd.to_datetime(gt["date"])

    # Naver: all-age, all-gender
    naver_all = naver[(naver["age_code"] == "all") & (naver["gender"] == "all")].copy()
    naver_all = naver_all.rename(columns={"period": "date", "ratio": "naver_rsv"})

    print("=" * 60)
    print("NAVER-GT KOREA CROSS-VALIDATION")
    print("=" * 60)

    results = []
    keywords = sorted(gt["keyword"].unique())

    for kw in keywords:
        n = naver_all[naver_all["keyword"] == kw][["date", "naver_rsv"]].copy()
        g = gt[gt["keyword"] == kw][["date", "rsv"]].rename(columns={"rsv": "gt_rsv"}).copy()

        merged = pd.merge(n, g, on="date", how="inner")

        if len(merged) < 10:
            print(f"  {kw}: insufficient overlapping data ({len(merged)} points)")
            continue

        rho, p = stats.spearmanr(merged["naver_rsv"], merged["gt_rsv"])
        r_pearson, p_pearson = stats.pearsonr(merged["naver_rsv"], merged["gt_rsv"])

        results.append({
            "keyword": kw,
            "n_months": len(merged),
            "spearman_rho": rho,
            "spearman_p": p,
            "pearson_r": r_pearson,
            "pearson_p": p_pearson,
        })

        sig = "*" if p < 0.05 else ""
        print(f"  {kw:12s}  ρ={rho:+.3f}  P={p:.4f}{sig}  r={r_pearson:+.3f}  n={len(merged)}")

    if results:
        results_df = pd.DataFrame(results)
        out_path = os.path.join(OUT_DIR, "gt_korea_cross_validation.csv")
        results_df.to_csv(out_path, index=False, encoding="utf-8-sig")

        mean_rho = results_df["spearman_rho"].mean()
        print(f"\n  Mean Spearman ρ = {mean_rho:.3f}")
        print(f"  Interpretation: {'Strong' if mean_rho > 0.7 else 'Moderate' if mean_rho > 0.4 else 'Weak'} "
              f"cross-platform concordance")
        print(f"\nSaved: {out_path}")
    else:
        print("No results to save.")


if __name__ == "__main__":
    main()
