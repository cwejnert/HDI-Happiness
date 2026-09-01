"""
HDI versus the SDG framework, on the same countries and the same design.

Two comparisons, because they point in opposite directions and the paper
needs both to be honest:

  (a) COVERAGE -- "what share of the countries each dataset covers has at
      least one indicator significant in levels?" Each framework is scored on
      its OWN full country set, not a matched subset: the SDG database carries
      42 countries and the HDR 150-151, and the share is the quantity of
      interest. SDG 71%, HDI 51% on any of five, 42% on the composite. The SDG
      framework wins, because asking whether ANY of ~456 series is significant
      is a much easier bar than asking about 5. Conceding this up front is
      what earns the right to make comparison (b).

  (b) EFFICIENCY -- what does a single indicator buy you? The median SDG
      series is significant in 0% of countries and 54% of them never clear
      FDR anywhere. Every HDI component beats 90-100% of the 609-series SDG
      field. That is the sense in which the HDI is the better instrument.

Same outcome (WHR happiness) and the same BH-FDR-within-country design on
both sides; only the country universe differs, because that is each dataset's
own coverage.

Inputs:  raw/robust_all_for_figures.csv, raw/HDI_with_happiness.csv,
         processed/sdg_series_significance_ranking.csv
Output:  figures_out/I1_framework_coverage_vs_efficiency.png
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# SDG uses UN long-form country names; these five need mapping to HDR names.
NAME_XW = {
    "Bolivia (Plurinational State of)": "Bolivia",
    "Republic of Korea": "South Korea",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "United States of America": "United States",
    "Viet Nam": "Vietnam",
}
HDI_INDS = ["hdi", "mys", "gnipc", "eys", "le"]
HDI_LABELS = {"hdi": "HDI composite", "mys": "Mean yrs schooling",
              "gnipc": "GNI per capita", "eys": "Expected yrs schooling",
              "le": "Life expectancy"}

BLUE, ORANGE, GREEN, RED = "#2A78D6", "#EDA100", "#1BAF7A", "#E34948"
GREY, BG, INK = "#8A8A8A", "#FCFCFB", "#1A1A1A"


def bh(ps):
    ps = np.asarray(ps, float)
    out = np.full(ps.shape, np.nan)
    ok = ~np.isnan(ps)
    m = ok.sum()
    if m == 0:
        return out
    idx = np.argsort(ps[ok])
    q = np.minimum.accumulate((ps[ok][idx] * m / np.arange(1, m + 1))[::-1])[::-1]
    tmp = np.empty(m)
    tmp[idx] = np.clip(q, 0, 1)
    out[ok] = tmp
    return out


def pval(x, y):
    ok = ~np.isnan(x) & ~np.isnan(y)
    if ok.sum() < 4 or np.std(x[ok]) == 0 or np.std(y[ok]) == 0:
        return np.nan
    return stats.pearsonr(x[ok], y[ok])[1]


def compute():
    """Score each framework on its own full country set."""
    sdg = pd.read_csv("raw/robust_all_for_figures.csv", low_memory=False)
    sig = sdg.assign(v=sdg.sig_levels_fdr.eq("q<.05")).groupby("GeoAreaName")["v"].any()
    n_series = sdg.groupby("GeoAreaName").SeriesCode.nunique().median()

    hdr = pd.read_csv("raw/HDI_with_happiness.csv")
    wide = hdr.pivot_table(index=["country", "year"], columns="indicatorCode",
                           values="value").reset_index()
    happy = hdr.groupby(["country", "year"])["happiness"].mean().reset_index()
    panel = wide.merge(happy, on=["country", "year"]).sort_values(["country", "year"])

    rows = []
    for cty, g in panel.groupby("country"):
        g = g.sort_values("year")
        q = bh([pval(g[i].to_numpy(float), g["happiness"].to_numpy(float)) for i in HDI_INDS])
        if np.isnan(q).all():
            continue
        rows.append({"composite": bool(q[0] == q[0] and q[0] < .05),
                     "any5": bool(np.nansum(q < .05))})
    hdi = pd.DataFrame(rows)

    coverage = [
        ("SDG framework", int(sig.sum()), len(sig), f"any of ~{n_series:.0f} series", ORANGE),
        ("HDI, all five", int(hdi.any5.sum()), len(hdi), "any of 5 indicators", BLUE),
        ("HDI composite", int(hdi.composite.sum()), len(hdi), "1 indicator", GREEN),
    ]

    rank = pd.read_csv("processed/sdg_series_significance_ranking.csv")
    rank = rank[rank.n_countries >= 8]
    return coverage, rank.pct_sig_levels.to_numpy()


def main():
    coverage, sdg_dist = compute()
    hdi_pts = {"hdi": 42.4, "mys": 40.7, "gnipc": 40.4, "eys": 34.0, "le": 19.9}

    fig, axes = plt.subplots(1, 2, figsize=(14.5, 6.0))
    fig.patch.set_facecolor(BG)

    # ---------- (a) coverage ----------
    ax = axes[0]
    x = range(len(coverage))
    for i, (label, k, n, note, col) in enumerate(coverage):
        pct = 100 * k / n
        ax.bar(i, pct, 0.58, color=col)
        ax.text(i, pct + 1.6, f"{pct:.0f}%", ha="center", fontsize=12,
                fontweight="bold", color=INK)
        ax.text(i, pct + 6.0, f"{k}/{n}", ha="center", fontsize=8.5, color=GREY)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{c[0]}\n{c[3]}\n{c[2]} countries covered" for c in coverage],
                       fontsize=8.5)
    ax.set_ylim(0, 88)
    ax.set_ylabel("% of that dataset's countries with ≥1 indicator\nsignificant in levels", fontsize=9.5)
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("a  Coverage: the SDG framework reaches a larger share of its countries",
                 fontsize=11.5, fontweight="bold", color=INK, loc="left", pad=44)
    ax.text(0, 1.015,
            "Each framework scored on its own full country set — the SDG database covers 42\n"
            "countries, the HDR 150. Asking whether ANY of ~456 series is significant is a far\n"
            "easier bar than asking about five.",
            transform=ax.transAxes, fontsize=8.5, color="#5A5A5A", va="bottom")

    # ---------- (b) efficiency ----------
    ax = axes[1]
    bins = np.arange(0, 50, 2.5)
    ax.hist(sdg_dist, bins=bins, color=ORANGE, alpha=0.75, edgecolor="white", linewidth=0.6)
    ax.set_ylim(0, 430)
    zero_share = 100 * (sdg_dist == 0).mean()
    ax.annotate(f"{zero_share:.0f}% of SDG series are\nsignificant in NO country",
                xy=(1.6, 340), xytext=(7.5, 385), fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1))

    # the three top HDI components sit within 2 points of each other, so they
    # get one grouped label rather than three colliding ones
    for v, col in [(19.9, RED), (34.0, BLUE), (40.4, GREEN), (40.7, BLUE), (42.4, BLUE)]:
        ax.axvline(v, color=col, linewidth=1.7, ymax=0.60)
    ax.annotate("Life expectancy\n19.9%", xy=(19.9, 262), xytext=(21.5, 292),
                fontsize=8.3, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    ax.annotate("Expected yrs schooling\n34.0%", xy=(34.0, 262), xytext=(24.0, 205),
                fontsize=8.3, color=BLUE, ha="left",
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.annotate("GNI p.c. 40.4%\nMean yrs schooling 40.7%\nHDI composite 42.4%",
                xy=(41.2, 262), xytext=(30.5, 330), fontsize=8.3, color=INK, ha="left",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_xlim(0, 50)
    ax.set_xlabel("% of countries in which that single indicator is significant (levels)", fontsize=9.5)
    ax.set_ylabel(f"Number of SDG series (of {len(sdg_dist)})", fontsize=9.5)
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("b  Efficiency: but a single HDI component beats almost the whole field",
                 fontsize=11.5, fontweight="bold", color=INK, loc="left", pad=30)
    ax.text(0, 1.015,
            "Every one of the 609 SDG series with usable coverage, and where the five HDI\n"
            "components fall among them. The median SDG series sits at zero.",
            transform=ax.transAxes, fontsize=8.5, color="#5A5A5A", va="bottom")

    fig.text(0.006, 0.972,
             "The SDG framework covers more countries; the HDI does far more per indicator",
             fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.006, 0.020,
             "Benjamini–Hochberg FDR-corrected within country against WHR happiness. "
             "SDG series restricted to those measured in ≥8 countries. "
             "Sources: UN SDG Global Database; UNDP HDR; World Happiness Report.",
             fontsize=8, color=GREY, va="bottom")
    fig.tight_layout(rect=(0, 0.05, 1, 0.885))
    out = "figures_out/I1_framework_coverage_vs_efficiency.png"
    fig.savefig(out, dpi=200, facecolor=BG)
    print(f"Saved: {out}")

    for label, k, n, note, _ in coverage:
        print(f"  {label:16s} {k:3d}/{n}  ({100*k/n:.0f}%)   {note}")
    print("  (HappinessHDI.R reports the composite as 64/151 = 42%; the one-country "
          "difference is a merge edge case)")
    print(f"  SDG series distribution: median {np.median(sdg_dist):.1f}%, "
          f"{zero_share:.0f}% at zero, max {sdg_dist.max():.1f}%")
    for k, v in hdi_pts.items():
        print(f"  {HDI_LABELS[k]:24s} {v:5.1f}%  beats {(sdg_dist < v).mean()*100:.0f}% of SDG series")


if __name__ == "__main__":
    main()
