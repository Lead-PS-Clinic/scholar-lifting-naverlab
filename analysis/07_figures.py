#!/usr/bin/env python3
"""Phase 8: Publication-quality figures and exploratory visualizations.

Figures:
1. Naver all-age RSV by keyword + GT global prejuvenation overlay (dual axis)
2. Annual age-group proportional share stacked area (KEY FIGURE)
3. β₃ forest plot by keyword
4. Joinpoint regression on YTR
+ Exploratory: Young vs Traditional RSV panels, GT global trends
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Try Korean font
KOREAN_FONTS = ["NanumGothic", "NanumBarunGothic", "Malgun Gothic", "AppleGothic"]
font_set = False
for fname in KOREAN_FONTS:
    try:
        fm.findfont(fname, fallback_to_default=False)
        plt.rcParams["font.family"] = fname
        font_set = True
        break
    except Exception:
        continue

if not font_set:
    plt.rcParams["font.family"] = "DejaVu Sans"
    print("Warning: Korean font not found, using DejaVu Sans")

plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["savefig.bbox"] = "tight"

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
FIG_DIR = os.path.join(BASE_DIR, "output", "figures")

# Color palette
COLORS = {
    "Young": "#E74C3C",
    "Middle": "#F39C12",
    "Traditional": "#3498DB",
}
KW_COLORS = {
    "실리프팅": "#E74C3C",
    "울쎄라": "#9B59B6",
    "슈링크": "#3498DB",
    "써마지": "#2ECC71",
    "인모드": "#F39C12",
    "리프팅시술": "#1ABC9C",
}


def load_data():
    raw = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "naver_rsv_all.csv"))
    raw["period"] = pd.to_datetime(raw["period"])
    gt = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "gt_global_prejuvenation.csv"))
    gt["date"] = pd.to_datetime(gt["date"])
    grouped = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "rsv_by_keyword_agegroup_month.csv"))
    grouped["period"] = pd.to_datetime(grouped["period"])
    props = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "annual_age_proportions.csv"))
    ytr = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "ytr_timeseries.csv"))
    table2 = pd.read_csv(os.path.join(BASE_DIR, "output", "tables", "table2_interaction_coefficients.csv"))
    jp_pred = pd.read_csv(os.path.join(BASE_DIR, "output", "tables", "joinpoint_predicted.csv"))
    return raw, gt, grouped, props, ytr, table2, jp_pred


def figure1(raw, gt):
    """Naver all-age RSV by keyword + GT prejuvenation overlay."""
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Naver data: all-age, all-gender
    naver_all = raw[(raw["age_code"] == "all") & (raw["gender"] == "all")]

    for kw in KW_COLORS:
        d = naver_all[naver_all["keyword"] == kw].sort_values("period")
        ax1.plot(d["period"], d["ratio"], color=KW_COLORS[kw], label=kw, alpha=0.8, linewidth=1.2)

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Naver RSV (0-100)", color="black")
    ax1.legend(loc="upper left", fontsize=8, framealpha=0.9)
    ax1.set_ylim(0, 105)

    # GT overlay on secondary axis
    ax2 = ax1.twinx()
    # Use "baby botox" as it has the strongest signal
    ax2.plot(gt["date"], gt["baby botox"], color="gray", linestyle="--",
             linewidth=1.5, alpha=0.7, label='GT: "baby botox" (global)')
    if "prejuvenation" in gt.columns:
        ax2.plot(gt["date"], gt["prejuvenation"], color="darkgray", linestyle=":",
                 linewidth=1.5, alpha=0.7, label='GT: "prejuvenation" (global)')
    ax2.set_ylabel("Google Trends RSV (global)", color="gray")
    ax2.legend(loc="upper right", fontsize=8, framealpha=0.9)

    ax1.set_title("Figure 1. Monthly Search Interest in Non-Surgical Lifting Procedures (Naver, 2016–2025)\n"
                   "with Global Prejuvenation Trends (Google Trends)", fontsize=11)

    # COVID annotation
    ax1.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-01"),
                alpha=0.1, color="red", label="COVID-19 initial impact")

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "figure1_naver_rsv_gt_overlay.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


def figure2(props):
    """Annual age-group proportional share — stacked area (KEY FIGURE)."""
    # All keywords combined, gender=all
    d = props[props["gender"] == "all"].copy()
    d_agg = d.groupby(["age_group", "year"])["proportion"].mean().reset_index()

    # Pivot for stacked area
    pivot = d_agg.pivot(index="year", columns="age_group", values="proportion")
    # Order: Traditional, Middle, Young (bottom to top)
    pivot = pivot[["Traditional", "Middle", "Young"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.stackplot(pivot.index, pivot.T.values,
                 labels=["Traditional (45+)", "Middle (35-44)", "Young (20-34)"],
                 colors=[COLORS["Traditional"], COLORS["Middle"], COLORS["Young"]],
                 alpha=0.85)

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Proportional Share of Search Interest", fontsize=12)
    ax.set_title("Figure 2. Age-Group Proportional Share of Non-Surgical Lifting Search Interest\n"
                 "(All Procedures Combined, Naver 2016–2025)", fontsize=11)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
    ax.set_xlim(2016, 2025)
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))

    # Annotate YTR values
    for year in [2016, 2020, 2025]:
        y_val = pivot.loc[year, "Young"]
        t_val = pivot.loc[year, "Traditional"]
        ytr = y_val / t_val if t_val > 0 else 0
        ax.annotate(f"YTR={ytr:.2f}", xy=(year, 0.02),
                    fontsize=8, ha="center", color="white", weight="bold")

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "figure2_age_proportions_stacked.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


def figure3(table2):
    """Forest plot of β₃ interaction coefficients by keyword."""
    fig, ax = plt.subplots(figsize=(8, 5))

    table2_sorted = table2.sort_values("beta3_interaction", ascending=True)
    y_pos = range(len(table2_sorted))

    for i, (_, row) in enumerate(table2_sorted.iterrows()):
        color = "#E74C3C" if row["significant_bh"] else "#95A5A6"
        ax.errorbar(row["beta3_interaction"], i,
                    xerr=[[row["beta3_interaction"] - row["beta3_ci_lower"]],
                           [row["beta3_ci_upper"] - row["beta3_interaction"]]],
                    fmt="o", color=color, capsize=4, markersize=8, linewidth=2)

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(table2_sorted["keyword"].values, fontsize=10)
    ax.axvline(x=0, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("β₃ (Time × Young Interaction Coefficient)", fontsize=11)
    ax.set_title("Figure 3. Age-Differential Growth Rate in Search Interest by Procedure\n"
                 "(β₃ < 0 indicates faster growth in Traditional 45+ vs Young 20–34)", fontsize=10)

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#E74C3C', markersize=8, label='Significant (BH-FDR < 0.05)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#95A5A6', markersize=8, label='Not significant'),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "figure3_beta3_forest_plot.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


def figure4(jp_pred, ytr):
    """Joinpoint regression on YTR."""
    fig, ax = plt.subplots(figsize=(10, 5))

    # Mean YTR across keywords
    ytr_all = ytr[ytr["gender"] == "all"].groupby("year")["YTR"].mean().reset_index()

    ax.scatter(ytr_all["year"], ytr_all["YTR"], color="#3498DB", s=60, zorder=5, label="Observed YTR")
    ax.plot(jp_pred["year"], jp_pred["ytr_predicted"], color="#E74C3C", linewidth=2,
            linestyle="-", label="Joinpoint model", zorder=4)

    # Parse joinpoints
    import ast
    try:
        jps = ast.literal_eval(jp_pred["joinpoints"].iloc[0])
    except (ValueError, SyntaxError):
        jps = []
    for jp in jps:
        ax.axvline(x=jp, color="#F39C12", linestyle="--", linewidth=1.5, alpha=0.7)
        ax.annotate(f"Joinpoint: {jp}", xy=(jp, ax.get_ylim()[1] * 0.95),
                    fontsize=9, ha="center", color="#F39C12")

    ax.axhline(y=1.0, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.annotate("YTR = 1.0 (parity)", xy=(2016.5, 1.02), fontsize=8, color="gray")

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Young-to-Traditional Ratio (YTR)", fontsize=12)
    ax.set_title("Figure 4. Joinpoint Regression of Young-to-Traditional Ratio (YTR)\n"
                 "(All Procedures Combined, Naver 2016–2025)", fontsize=11)
    ax.legend(fontsize=10)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "figure4_joinpoint_ytr.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


def figure_exploratory_panels(grouped):
    """Young vs Traditional RSV — 6 keyword small multiples."""
    keywords = sorted(grouped["keyword"].unique())
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharex=True)
    axes = axes.flatten()

    for i, kw in enumerate(keywords):
        ax = axes[i]
        d = grouped[(grouped["keyword"] == kw) & (grouped["gender"] == "all")]

        for ag in ["Young", "Traditional"]:
            dd = d[d["age_group"] == ag].sort_values("period")
            ax.plot(dd["period"], dd["mean_rsv"], color=COLORS[ag], label=ag, linewidth=1.2)

        ax.set_title(kw, fontsize=11, fontweight="bold")
        ax.set_ylim(0, None)
        if i == 0:
            ax.legend(fontsize=8)

    fig.suptitle("Young (20-34) vs Traditional (45+) Search Interest by Procedure (Naver, 2016-2025)",
                 fontsize=12, y=1.02)
    fig.supxlabel("Date")
    fig.supylabel("Mean RSV")
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "exploratory_young_vs_traditional_panels.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


def figure_gt_global(gt):
    """GT global: prejuvenation, preventive botox, baby botox."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for col in ["prejuvenation", "preventive botox", "baby botox"]:
        if col in gt.columns:
            ax.plot(gt["date"], gt[col], label=col, linewidth=1.5)

    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Google Trends RSV (Worldwide)", fontsize=12)
    ax.set_title("Global Search Interest in Prejuvenation-Related Terms (Google Trends, 2016-2025)",
                 fontsize=11)
    ax.legend(fontsize=10)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "exploratory_gt_global_trends.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved: {path}")


def main():
    os.makedirs(FIG_DIR, exist_ok=True)

    print("Loading data...")
    raw, gt, grouped, props, ytr, table2, jp_pred = load_data()

    print("\nGenerating figures...")
    figure1(raw, gt)
    figure2(props)
    figure3(table2)
    figure4(jp_pred, ytr)
    figure_exploratory_panels(grouped)
    figure_gt_global(gt)

    print(f"\nAll figures saved to {FIG_DIR}")


if __name__ == "__main__":
    main()
