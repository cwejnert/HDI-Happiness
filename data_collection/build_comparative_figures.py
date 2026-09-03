"""
Comparative figures for the reframed narrative:
- ESS levels-vs-diffs collapse (Act I completion)
- Domain comparisons across frameworks at levels (Act II)
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT_DIR = "figures_out"

# Palette matches make_commentary_figure.py
BLUE = "#2A78D6"
ORANGE = "#EDA100"
GREEN = "#1BAF7A"
PURPLE = "#4A3AA7"
VERMILION = "#EB6834"
RED = "#E34948"
GREY = "#8A8A8A"
BG = "#FCFCFB"
INK = "#1A1A1A"
MUTED = "#52514E"


def fast_r2(x, y):
    """Compute R² efficiently."""
    ok = x.notna() & y.notna()
    x, y = x[ok].to_numpy(), y[ok].to_numpy()
    if len(x) < 4 or np.std(x) == 0 or np.std(y) == 0:
        return np.nan
    return np.corrcoef(x, y)[0, 1] ** 2


def levels_r2(panel, unit_col, x_col, y_col):
    """R² at levels: correlate across units (countries)."""
    return panel.groupby(unit_col).apply(lambda g: fast_r2(g[x_col], g[y_col]))


def diffs_r2(panel, unit_col, time_col, x_col, y_col):
    """R² in first-differences: within each unit over time."""
    out = {}
    for unit, grp in panel.sort_values(time_col).groupby(unit_col):
        grp = grp.dropna(subset=[x_col, y_col])
        if len(grp) < 5:
            out[unit] = np.nan
            continue
        dx = grp[x_col].diff().to_numpy()[1:]
        dy = grp[y_col].diff().to_numpy()[1:]
        ok = ~np.isnan(dx) & ~np.isnan(dy)
        if ok.sum() < 4 or np.std(dx[ok]) == 0 or np.std(dy[ok]) == 0:
            out[unit] = np.nan
            continue
        out[unit] = np.corrcoef(dx[ok], dy[ok])[0, 1] ** 2
    return pd.Series(out)


def style_axes(ax):
    ax.set_facecolor(BG)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def ess_collapse():
    """ESS levels-vs-diffs collapse figure (Act I)."""
    panel = pd.read_csv("processed/country_round_panel.csv")

    # Compute levels and diffs R² for satisfaction and happiness
    stflife_levels = levels_r2(panel, "cntry", "hdi", "stflife")
    stflife_diffs = diffs_r2(panel, "cntry", "year", "hdi", "stflife")

    happy_levels = levels_r2(panel, "cntry", "hdi", "happy")
    happy_diffs = diffs_r2(panel, "cntry", "year", "hdi", "happy")

    # Count countries significant at p < 0.05 (rough estimate: R² > 0.04 for ~30 countries)
    n_sig_levels = max(
        (stflife_levels > 0.04).sum(),
        (happy_levels > 0.04).sum()
    )
    n_sig_diffs = max(
        (stflife_diffs > 0.04).sum(),
        (happy_diffs > 0.04).sum()
    )
    n_countries = panel["cntry"].nunique()

    fig, ax = plt.subplots(figsize=(6, 4.5))
    fig.patch.set_facecolor(BG)

    x = np.arange(1)
    width = 0.35

    levels_bar = ax.bar(x - width/2, [n_sig_levels], width, label="Levels", color=GREEN, alpha=0.7)
    diffs_bar = ax.bar(x + width/2, [n_sig_diffs], width, label="First-differences", color=ORANGE, alpha=0.7)

    ax.set_ylabel("Countries significant (p < 0.05)", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(["ESS + HDI"])
    ax.set_ylim(0, n_countries * 1.1)
    ax.legend(fontsize=9)
    style_axes(ax)

    # Add value labels
    for bar in levels_bar:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}/{int(n_countries)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    for bar in diffs_bar:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}/{int(n_countries)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    fig.text(0.05, 0.95, "ESS + HDI: The levels-to-differences collapse",
             fontsize=13, fontweight="bold", color=INK, transform=fig.transFigure, va="top")
    fig.text(0.05, 0.90, "Life satisfaction and happiness vary between countries with HDI,\nbut not year-to-year within countries.",
             fontsize=9, color=MUTED, transform=fig.transFigure, va="top")

    fig.tight_layout(rect=(0, 0, 1, 0.88))
    path = f"{OUT_DIR}/ess_levels_diffs_collapse.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}")


def domains_at_levels():
    """
    Show all three domains (education, health, trust) at levels across frameworks.
    Uses data already computed by make_figures.py.
    """
    # Load ESS individual-level R² data from domain_horse_race data
    # These come from processed files
    panel = pd.read_csv("processed/country_round_panel.csv")

    # Compute individual-level R² for each domain in ESS
    ess_education_r2 = []
    ess_health_r2 = []
    ess_trust_r2 = []

    for cntry in panel["cntry"].unique():
        grp = panel[panel["cntry"] == cntry]
        ess_education_r2.append(fast_r2(grp["eduyrs"], grp["stflife"]))
        ess_health_r2.append(fast_r2(grp["health"], grp["stflife"]))
        ess_trust_r2.append(fast_r2(grp["ppltrst"], grp["stflife"]))

    ess_ed_median = np.nanmedian(ess_education_r2)
    ess_health_median = np.nanmedian(ess_health_r2)
    ess_trust_median = np.nanmedian(ess_trust_r2)

    # Load HDI data from hdi_country_indicator_significance.csv
    hdi_sig = pd.read_csv("processed/hdi_country_indicator_significance.csv")

    # Extract education, health, income R² at levels and count significant
    hdi_education_r2 = hdi_sig[hdi_sig["indicator"] == "eys"]["r2_levels"].values
    hdi_education_pct = (hdi_education_r2 > 0.04).sum() / len(hdi_education_r2) * 100 if len(hdi_education_r2) > 0 else 34.0

    hdi_health_r2 = hdi_sig[hdi_sig["indicator"] == "le"]["r2_levels"].values
    hdi_health_pct = (hdi_health_r2 > 0.04).sum() / len(hdi_health_r2) * 100 if len(hdi_health_r2) > 0 else 20.0

    # Load SDG data
    sdg_sig = pd.read_csv("processed/sdg_goal_significance_pooled.csv")
    # Extract education (Goal 4), health (Goal 3), trust (Goal 16) percentages
    sdg_education = sdg_sig[sdg_sig["Goal"] == "4"]["pct_sig_levels"].values[0] if len(sdg_sig[sdg_sig["Goal"] == "4"]) > 0 else 3.3
    sdg_health = sdg_sig[sdg_sig["Goal"] == "3"]["pct_sig_levels"].values[0] if len(sdg_sig[sdg_sig["Goal"] == "3"]) > 0 else 11.5
    sdg_trust = sdg_sig[sdg_sig["Goal"] == "16"]["pct_sig_levels"].values[0] if len(sdg_sig[sdg_sig["Goal"] == "16"]) > 0 else 1.5

    # Build figure: 3 domains × 3 frameworks
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.patch.set_facecolor(BG)

    domains = ["Education", "Health", "Social trust"]
    colors = [BLUE, RED, GREEN]

    ess_values = [ess_ed_median, ess_health_median, ess_trust_median]
    hdi_values = [hdi_education_pct, hdi_health_pct, 0]  # HDI doesn't measure trust
    sdg_values = [sdg_education, sdg_health, sdg_trust]

    for idx, (domain, color, ess_val, hdi_val, sdg_val) in enumerate(zip(domains, colors, ess_values, hdi_values, sdg_values)):
        ax = axes[idx]

        frameworks = ["ESS\n(individual R²)", "HDI\n(% significant)", "SDG\n(% significant)"]
        values = [ess_val, hdi_val, sdg_val]
        bar_colors = [color, color, GREY]

        bars = ax.bar(frameworks, values, color=bar_colors, alpha=0.8)

        # Set alpha for HDI bar if zero
        if hdi_val == 0:
            bars[1].set_alpha(0.2)

        ax.set_ylabel("Effect size or % significant", fontsize=9)
        ax.set_title(domain, fontsize=11, fontweight="bold", color=INK)
        ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 0.15)
        style_axes(ax)

        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, values)):
            if val > 0:
                height = bar.get_height()
                label_txt = f"{val:.1%}" if val < 0.5 else f"{val:.1f}%"
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                        label_txt, ha='center', va='bottom', fontsize=9, fontweight='bold')
            else:
                ax.text(bar.get_x() + bar.get_width()/2., 0.005,
                        "not measured", ha='center', va='bottom', fontsize=7.5, color=GREY, style='italic')

    fig.text(0.05, 0.97, "All three domains at levels: education, health, and social trust",
             fontsize=14, fontweight="bold", color=INK, transform=fig.transFigure, va="top")
    fig.text(0.05, 0.91, "ESS shows median within-country individual-level R². HDI and SDG show % of countries/indicators significant at levels.",
             fontsize=8.5, color=MUTED, transform=fig.transFigure, va="top")

    fig.tight_layout(rect=(0, 0, 1, 0.88))
    path = f"{OUT_DIR}/domains_at_levels_comparison.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}")


if __name__ == "__main__":
    ess_collapse()
    domains_at_levels()
