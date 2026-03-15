#!/usr/bin/env python3
"""Generate realistic simulated Naver DataLab RSV data.

Produces data matching the schema of 01_collect_naver.py output.
Patterns are designed to reflect plausible trends:
- Thread lifting (실리프팅): strong broadening into younger demographics
- Ulthera (울쎄라): predominantly older, slow decline
- Shrink (슈링크): rapid growth, moderate youth adoption (launched ~2018)
- Thermage (써마지): steady, moderate broadening
- InMode (인모드): newer device, strong youth appeal (launched ~2018)
- Generic lifting (리프팅시술): broad, moderate broadening
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "naver_rsv_all.csv")

# Time axis: 2016-01 to 2025-12 = 120 months
periods = pd.date_range("2016-01-01", "2025-12-01", freq="MS")
n_months = len(periods)
time_idx = np.arange(n_months)

# Age codes and their analytic groups
AGE_CODES = ["3", "4", "5", "6", "7", "8", "9", "10", "11"]
AGE_LABELS = {
    "3": "19-24", "4": "25-29", "5": "30-34",
    "6": "35-39", "7": "40-44",
    "8": "45-49", "9": "50-54", "10": "55-59", "11": "60+"
}

GENDERS = ["all", "f", "m"]

# Keyword configs: base_level, growth_rate, youth_acceleration, launch_month (0=always), seasonality_amp
KEYWORD_CONFIGS = {
    "실리프팅": {
        "base": 30, "growth": 0.25, "youth_accel": 0.15,
        "launch": 0, "season_amp": 8,
        "age_base": {"3": 10, "4": 18, "5": 25, "6": 30, "7": 28, "8": 25, "9": 20, "10": 15, "11": 10},
        "age_growth": {"3": 0.35, "4": 0.40, "5": 0.35, "6": 0.20, "7": 0.15, "8": 0.10, "9": 0.08, "10": 0.05, "11": 0.03},
    },
    "울쎄라": {
        "base": 45, "growth": -0.05, "youth_accel": 0.05,
        "launch": 0, "season_amp": 5,
        "age_base": {"3": 5, "4": 10, "5": 18, "6": 30, "7": 40, "8": 50, "9": 45, "10": 35, "11": 20},
        "age_growth": {"3": 0.08, "4": 0.10, "5": 0.08, "6": 0.02, "7": -0.02, "8": -0.05, "9": -0.08, "10": -0.10, "11": -0.10},
    },
    "슈링크": {
        "base": 5, "growth": 0.55, "youth_accel": 0.20,
        "launch": 24, "season_amp": 7,  # ~2018-01
        "age_base": {"3": 8, "4": 15, "5": 22, "6": 28, "7": 30, "8": 28, "9": 22, "10": 15, "11": 8},
        "age_growth": {"3": 0.50, "4": 0.55, "5": 0.45, "6": 0.30, "7": 0.25, "8": 0.20, "9": 0.15, "10": 0.10, "11": 0.05},
    },
    "써마지": {
        "base": 40, "growth": 0.15, "youth_accel": 0.10,
        "launch": 0, "season_amp": 6,
        "age_base": {"3": 8, "4": 15, "5": 22, "6": 32, "7": 38, "8": 42, "9": 35, "10": 25, "11": 15},
        "age_growth": {"3": 0.20, "4": 0.25, "5": 0.22, "6": 0.15, "7": 0.10, "8": 0.08, "9": 0.05, "10": 0.02, "11": 0.00},
    },
    "인모드": {
        "base": 3, "growth": 0.60, "youth_accel": 0.25,
        "launch": 24, "season_amp": 6,  # ~2018-01
        "age_base": {"3": 10, "4": 20, "5": 28, "6": 30, "7": 25, "8": 20, "9": 15, "10": 8, "11": 5},
        "age_growth": {"3": 0.55, "4": 0.60, "5": 0.50, "6": 0.35, "7": 0.25, "8": 0.18, "9": 0.12, "10": 0.08, "11": 0.03},
    },
    "리프팅시술": {
        "base": 35, "growth": 0.20, "youth_accel": 0.12,
        "launch": 0, "season_amp": 7,
        "age_base": {"3": 12, "4": 20, "5": 28, "6": 32, "7": 35, "8": 38, "9": 30, "10": 22, "11": 12},
        "age_growth": {"3": 0.30, "4": 0.32, "5": 0.28, "6": 0.18, "7": 0.14, "8": 0.10, "9": 0.07, "10": 0.04, "11": 0.02},
    },
}

# Gender modifiers: female has higher base, male has lower
GENDER_MOD = {"all": 1.0, "f": 1.15, "m": 0.70}
# Gender-specific youth acceleration: women show stronger broadening
GENDER_YOUTH_MOD = {"all": 1.0, "f": 1.20, "m": 0.75}


def generate_seasonal(n, amp, phase_shift=0):
    """Generate seasonal component with annual periodicity."""
    months = np.arange(n)
    # Peak in spring (March-April) and fall (October-November) — typical aesthetic procedure seasons
    return amp * (0.6 * np.sin(2 * np.pi * (months - 2 + phase_shift) / 12) +
                  0.4 * np.sin(4 * np.pi * (months - 2 + phase_shift) / 12))


def generate_covid_dip(n):
    """Generate COVID-19 dip (March-June 2020) and rebound."""
    effect = np.zeros(n)
    # Months 50-53 = March-June 2020
    effect[50] = -0.25
    effect[51] = -0.35
    effect[52] = -0.20
    effect[53] = -0.10
    # Rebound
    effect[54] = 0.05
    effect[55] = 0.10
    return effect


def generate_rsv(config, age_code, gender, time_idx):
    """Generate RSV time series for a specific condition."""
    n = len(time_idx)
    launch = config["launch"]

    if age_code == "all":
        base = config["base"]
        growth = config["growth"]
    else:
        base = config["age_base"][age_code]
        growth = config["age_growth"][age_code]

    # Apply gender modifier
    g_mod = GENDER_MOD[gender]
    gy_mod = GENDER_YOUTH_MOD[gender]

    # For age-specific, modulate growth by gender-youth interaction
    if age_code in ["3", "4", "5"]:  # Young
        growth = growth * gy_mod

    # Trend
    trend = base * g_mod + growth * g_mod * time_idx

    # Seasonal
    seasonal = generate_seasonal(n, config["season_amp"])

    # COVID dip
    covid = generate_covid_dip(n) * base * g_mod

    # Post-COVID youth acceleration (2021+): younger groups show extra growth
    post_covid_accel = np.zeros(n)
    if age_code in ["3", "4", "5"]:
        # Acceleration starts at month 60 (Jan 2021)
        accel_months = np.maximum(time_idx - 60, 0)
        post_covid_accel = 0.08 * g_mod * accel_months

    # Combine
    rsv = trend + seasonal + covid + post_covid_accel

    # Apply launch date (zero before launch)
    if launch > 0:
        rsv[:launch] = 0
        # Ramp-up over 6 months after launch
        ramp_end = min(launch + 6, n)
        for i in range(launch, ramp_end):
            rsv[i] *= (i - launch + 1) / 6

    # Add noise
    noise = np.random.normal(0, max(base * 0.05, 1), n)
    rsv = rsv + noise

    # Normalize to 0-100 (Naver RSV is independently normalized per query)
    rsv = np.clip(rsv, 0, None)
    if rsv.max() > 0:
        rsv = rsv / rsv.max() * 100

    return np.round(rsv, 2)


def main():
    all_rows = []

    for kw_name, config in KEYWORD_CONFIGS.items():
        # All-age condition
        for gender in GENDERS:
            rsv = generate_rsv(config, "all", gender, time_idx)
            for i, period in enumerate(periods):
                all_rows.append({
                    "keyword": kw_name,
                    "age_code": "all",
                    "gender": gender,
                    "period": period.strftime("%Y-%m-%d"),
                    "ratio": rsv[i],
                })

        # Age-specific conditions
        for age_code in AGE_CODES:
            for gender in GENDERS:
                rsv = generate_rsv(config, age_code, gender, time_idx)
                for i, period in enumerate(periods):
                    all_rows.append({
                        "keyword": kw_name,
                        "age_code": age_code,
                        "gender": gender,
                        "period": period.strftime("%Y-%m-%d"),
                        "ratio": rsv[i],
                    })

    df = pd.DataFrame(all_rows)
    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT_PATH)), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print(f"Simulated Naver RSV data saved to {OUTPUT_PATH}")
    print(f"Shape: {df.shape}")
    print(f"Keywords: {df['keyword'].unique().tolist()}")
    print(f"Age codes: {sorted(df['age_code'].unique().tolist())}")
    print(f"Genders: {sorted(df['gender'].unique().tolist())}")
    print(f"Period: {df['period'].min()} ~ {df['period'].max()}")
    print(f"\nSample data:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
