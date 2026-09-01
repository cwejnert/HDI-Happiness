"""
HDI versus the SDG framework, on the same countries and the same design.

Two comparisons, because they point in opposite directions and the paper
needs both to be honest:

  (a) COVERAGE AT A MATCHED BAR -- "what share of the countries each dataset
      covers clears a given bar in levels?" At the loosest bar -- at least ONE
      indicator significant -- the SDG framework wins, 71% to 51%, because one
      of ~456 series is far easier than one of 5. But that bar is not
      comparable across frameworks with 456 and 5 indicators. Requiring
      instead a SHARE of each country's own indicators makes it comparable,
      and the ordering reverses hard: at 1-in-5 of a country's own indicators
      the HDI reaches 51% of its countries and the SDG framework only 17%.
      Above ~35% no SDG country qualifies at all, while 44% of HDI countries
      still clear a 3-of-5 bar.

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
    """Both frameworks on their own full country sets, across thresholds."""
    sdg = pd.read_csv("raw/robust_all_for_figures.csv", low_memory=False)
    sdg["sig"] = sdg.sig_levels_fdr.eq("q<.05")
    per_country = sdg.groupby("GeoAreaName").agg(n=("sig", "size"), k=("sig", "sum"))
    sdg_share = (100 * per_country.k / per_country.n).to_numpy()
    n_series = sdg.groupby("GeoAreaName").SeriesCode.nunique().median()

    hdr = pd.read_csv("raw/HDI_with_happiness.csv")
    wide = hdr.pivot_table(index=["country", "year"], columns="indicatorCode",
                           values="value").reset_index()
    happy = hdr.groupby(["country", "year"])["happiness"].mean().reset_index()
    panel = wide.merge(happy, on=["country", "year"]).sort_values(["country", "year"])
    counts = []
    for cty, g in panel.groupby("country"):
        g = g.sort_values("year")
        q = bh([pval(g[i].to_numpy(float), g["happiness"].to_numpy(float)) for i in HDI_INDS])
        if np.isnan(q).all():
            continue
        counts.append(int(np.nansum(q < .05)))
    hdi_counts = np.array(counts)
    hdi_share = 100 * hdi_counts / len(HDI_INDS)

    rank = pd.read_csv("processed/sdg_series_significance_ranking.csv")
    rank = rank[rank.n_countries >= 8]
    return sdg_share, hdi_share, n_series, rank.pct_sig_levels.to_numpy()


def main():
    sdg_share, hdi_share, n_series, sdg_dist = compute()
    n_sdg, n_hdi = len(sdg_share), len(hdi_share)
    # where each HDI component falls in the SDG series distribution (panel b)
    hdi_pts = {"hdi": 42.4, "mys": 40.7, "gnipc": 40.4, "eys": 34.0, "le": 19.9}

    fig, axes = plt.subplots(1, 2, figsize=(14.5, 6.0))
    fig.patch.set_facecolor(BG)

    # ---------- (a) coverage across matched thresholds ----------
    ax = axes[0]
    grid = np.arange(0.01, 101, 0.5)
    ax.plot(grid, [100 * (sdg_share >= t).mean() for t in grid], color=ORANGE,
            linewidth=2.6, label=f"SDG framework  ({n_sdg} countries, ~{n_series:.0f} series each)")
    ax.plot(grid, [100 * (hdi_share >= t).mean() for t in grid], color=BLUE,
            linewidth=2.6, label=f"HDI  ({n_hdi} countries, 5 indicators each)")

    ax.axvline(20, color=GREY, linestyle=(0, (4, 3)), linewidth=1.1)
    ax.annotate("a matched bar:\n1 in 5 of a country's\nown indicators",
                xy=(20, 88), xytext=(27, 84), fontsize=8.3, color=INK,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
    for val, col, lab in [(100 * (hdi_share >= 20).mean(), BLUE, "51%"),
                          (100 * (sdg_share >= 20).mean(), ORANGE, "17%")]:
        ax.plot(20, val, "o", color=col, markersize=7, markeredgecolor="white", zorder=5)
        ax.text(21.5, val, lab, fontsize=10, fontweight="bold", color=col, va="center")

    ax.text(1.5, 100 * (sdg_share > 0).mean() + 3.5, "71%", fontsize=9, color=ORANGE)
    ax.text(1.5, 100 * (hdi_share > 0).mean() - 6.5, "51%", fontsize=9, color=BLUE)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Bar: % of a country's own indicators required to be significant", fontsize=9.5)
    ax.set_ylabel("% of that dataset's countries clearing the bar", fontsize=9.5)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax.set_facecolor(BG)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("a  At a comparable bar, the ordering reverses",
                 fontsize=11.5, fontweight="bold", color=INK, loc="left", pad=44)
    ax.text(0, 1.015,
            "At the loosest bar — any ONE indicator — the SDG framework leads 71% to 51%, but one\n"
            "of ~456 series is not the same test as one of 5. Requiring a share of each country's own\n"
            "indicators makes it comparable. Above ~35% no SDG country qualifies at all.",
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
    ax.set_title("b  Why: the median SDG series carries no signal at all",
                 fontsize=11.5, fontweight="bold", color=INK, loc="left", pad=30)
    ax.text(0, 1.015,
            "Every one of the 609 SDG series with usable coverage, and where the five HDI\n"
            "components fall among them. The median SDG series sits at zero.",
            transform=ax.transAxes, fontsize=8.5, color="#5A5A5A", va="bottom")

    fig.text(0.006, 0.972,
             "The SDG framework wins on the loosest bar only; per indicator the HDI dominates",
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

    print(f"  SDG {n_sdg} countries | HDI {n_hdi} countries")
    for t in (0.01, 5, 10, 20, 40, 60, 80, 100):
        lab = "any" if t < 1 else f">={t:.0f}%"
        print(f"  bar {lab:>6s} of own indicators : SDG {100*(sdg_share>=t).mean():3.0f}%   "
              f"HDI {100*(hdi_share>=t).mean():3.0f}%")
    print(f"  median share of own series significant: SDG {np.median(sdg_share):.1f}%, "
          f"max {sdg_share.max():.1f}%")
    print(f"  SDG series distribution: median {np.median(sdg_dist):.1f}%, "
          f"{zero_share:.0f}% at zero, max {sdg_dist.max():.1f}%")
    for k, v in hdi_pts.items():
        print(f"  {HDI_LABELS[k]:24s} {v:5.1f}%  beats {(sdg_dist < v).mean()*100:.0f}% of SDG series")


if __name__ == "__main__":
    main()
