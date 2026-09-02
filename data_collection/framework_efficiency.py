"""
HDI versus the SDG framework: three comparisons, reported together.

No single statistic settles "which framework tracks wellbeing better", so all
three are reported and none is nominated as the headline:

  (a) DETECTION -- "does ANY indicator show a significant levels association
      in this country?" SDG 71% of its 42 countries, HDI 51% of its 150. The
      SDG framework wins, and this is a fair comparison: Benjamini-Hochberg
      under the complete null controls FWER at the same alpha regardless of
      family size, so both sides are size-matched. The SDG advantage is
      genuine statistical POWER bought with breadth, not an artifact.

  (b) BUDGET-MATCHED -- give the SDG framework the same five indicators the
      HDI gets, drawn at random, 4000 times. SDG-random-5 reaches 30% of
      countries (95% range 19-40); the HDI's chosen five reach 40% on the same
      42 countries. The HDI's selection is better than a random five, but it
      lands at the top EDGE of the random range, not outside it. Most of the
      SDG framework's lead in (a) is explained by indicator count, and the
      HDI's edge at matched budget is real but modest.

  (c) PER-INDICATOR -- the median SDG series is significant in NO country and
      54% never clear FDR anywhere, while HDI components beat 90-100% of the
      609-series field. This is the strongest claim because it requires no
      cross-framework normalisation at all -- though note it compares the
      HDI's best against the SDG median, which (b) shows is generous.

An earlier version normalised by the SHARE of a country's own indicators.
That was dropped: it penalises breadth for its own sake (bolt 100 irrelevant
series onto the HDI and its score collapses while it loses no information),
and the FWER argument above shows the "any" bar did not need rescuing.

Same outcome (WHR happiness), same BH-FDR-within-country design throughout;
country universes differ because that is each dataset's own coverage.

Inputs:  raw/robust_all_for_figures.csv, raw/HDI_with_happiness.csv,
         processed/sdg_series_significance_ranking.csv
Output:  figures_out/I1_framework_three_comparisons.png
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


def compute(n_boot=4000, seed=0):
    rng = np.random.default_rng(seed)
    sdg = pd.read_csv("raw/robust_all_for_figures.csv", low_memory=False)
    sdg["cname"] = sdg.GeoAreaName.replace(NAME_XW)
    sdg["sig"] = sdg.sig_levels_fdr.eq("q<.05")

    detect_sdg = sdg.groupby("GeoAreaName")["sig"].any()
    n_series = sdg.groupby("GeoAreaName").SeriesCode.nunique().median()

    hdr = pd.read_csv("raw/HDI_with_happiness.csv")
    wide = hdr.pivot_table(index=["country", "year"], columns="indicatorCode",
                           values="value").reset_index()
    happy = hdr.groupby(["country", "year"])["happiness"].mean().reset_index()
    panel = wide.merge(happy, on=["country", "year"]).sort_values(["country", "year"])
    hdi_any = {}
    for cty, g in panel.groupby("country"):
        g = g.sort_values("year")
        q = bh([pval(g[i].to_numpy(float), g["happiness"].to_numpy(float)) for i in HDI_INDS])
        if np.isnan(q).all():
            continue
        hdi_any[cty] = bool(np.nansum(q < .05))
    hdi_any = pd.Series(hdi_any)

    # (b) budget-matched: 5 random SDG series per country, on the SDG country set
    by_country = {c: g.sig.to_numpy() for c, g in sdg.groupby("GeoAreaName")}
    boot = []
    for _ in range(n_boot):
        hits = sum(rng.choice(a, size=min(5, len(a)), replace=False).any()
                   for a in by_country.values())
        boot.append(100 * hits / len(by_country))
    boot = np.array(boot)

    # the HDI's own five, restricted to the same countries, for a like-for-like
    matched = set(sdg.cname) & set(hdi_any.index)
    hdi_matched = 100 * hdi_any[hdi_any.index.isin(matched)].mean()

    rank = pd.read_csv("processed/sdg_series_significance_ranking.csv")
    rank = rank[rank.n_countries >= 8]
    return dict(
        detect=[("SDG framework", int(detect_sdg.sum()), len(detect_sdg),
                 f"any of ~{n_series:.0f} series", ORANGE),
                ("HDI", int(hdi_any.sum()), len(hdi_any), "any of 5 indicators", BLUE)],
        boot=boot, hdi_matched=hdi_matched, n_matched=len(matched),
        sdg_dist=rank.pct_sig_levels.to_numpy())


def main():
    d = compute()
    hdi_pts = {"hdi": 42.4, "mys": 40.7, "gnipc": 40.4, "eys": 34.0, "le": 19.9}
    sdg_dist, boot = d["sdg_dist"], d["boot"]

    fig, axes = plt.subplots(1, 3, figsize=(17.5, 5.9))
    fig.patch.set_facecolor(BG)

    # ---------- (a) detection ----------
    ax = axes[0]
    for i, (label, k, n, note, col) in enumerate(d["detect"]):
        pct = 100 * k / n
        ax.bar(i, pct, 0.52, color=col)
        ax.text(i, pct + 1.8, f"{pct:.0f}%", ha="center", fontsize=13,
                fontweight="bold", color=INK)
        ax.text(i, pct + 6.5, f"{k}/{n} countries", ha="center", fontsize=8.5, color=GREY)
    ax.set_xticks(range(len(d["detect"])))
    ax.set_xticklabels([f"{c[0]}\n{c[3]}" for c in d["detect"]], fontsize=9)
    ax.set_ylim(0, 92)
    ax.set_ylabel("% of that dataset's countries with ≥1 indicator significant", fontsize=9)
    ax.set_title("a  Detection: the SDG framework wins", fontsize=11,
                 fontweight="bold", color=INK, loc="left", pad=40)
    ax.text(0, 1.015,
            "A fair comparison, not an artifact: BH under the null controls the\n"
            "error rate at the same α whatever the family size. The SDG lead is\n"
            "genuine power bought with breadth.",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")

    # ---------- (b) budget-matched ----------
    ax = axes[1]
    counts, _, _ = ax.hist(boot, bins=30, color=ORANGE, alpha=0.75,
                           edgecolor="white", linewidth=0.5)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    ax.axvspan(lo, hi, color=ORANGE, alpha=0.10, zorder=0)
    ax.set_ylim(0, counts.max() * 1.62)
    top = ax.get_ylim()[1]
    ax.axvline(boot.mean(), color=ORANGE, linewidth=2.2, ymax=0.72)
    ax.axvline(d["hdi_matched"], color=BLUE, linewidth=2.6, ymax=0.86)
    ax.annotate(f"SDG, 5 random series\n{boot.mean():.0f}%",
                xy=(boot.mean(), top * 0.72), xytext=(boot.mean() - 10.5, top * 0.86),
                fontsize=8.6, color=ORANGE, fontweight="bold", ha="left",
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.9))
    ax.annotate(f"HDI, its own 5\n{d['hdi_matched']:.0f}%",
                xy=(d["hdi_matched"], top * 0.86), xytext=(d["hdi_matched"] + 0.4, top * 0.93),
                fontsize=8.6, color=BLUE, fontweight="bold", ha="left",
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.9))
    ax.annotate(f"95% of random draws fall in {lo:.0f}–{hi:.0f}%",
                xy=(lo, top * 0.10), xytext=(lo + 0.6, top * 0.20),
                fontsize=8, color=GREY,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
    ax.set_xlabel("% of the 42 SDG countries with ≥1 of 5 significant", fontsize=9)
    ax.set_ylabel("Bootstrap draws (of 4,000)", fontsize=9)
    ax.set_title("b  Budget-matched: the HDI's edge is real but modest", fontsize=11,
                 fontweight="bold", color=INK, loc="left", pad=40)
    ax.text(0, 1.015,
            "Give the SDG framework the same five-indicator budget, drawn at\n"
            "random. The HDI's chosen five beat a random five — but land at the\n"
            "top edge of the range, not outside it.",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")

    # ---------- (c) per-indicator ----------
    ax = axes[2]
    ax.hist(sdg_dist, bins=np.arange(0, 50, 2.5), color=ORANGE, alpha=0.75,
            edgecolor="white", linewidth=0.6)
    ax.set_ylim(0, 430)
    zero = 100 * (sdg_dist == 0).mean()
    ax.annotate(f"{zero:.0f}% of SDG series are\nsignificant in NO country",
                xy=(1.6, 340), xytext=(8, 388), fontsize=8.3, color=INK,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
    for v, col in [(19.9, RED), (34.0, BLUE), (40.4, GREEN), (40.7, BLUE), (42.4, BLUE)]:
        ax.axvline(v, color=col, linewidth=1.7, ymax=0.58)
    ax.annotate("Life expectancy 19.9%", xy=(19.9, 250), xytext=(21, 285),
                fontsize=8, color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    ax.annotate("Exp. yrs schooling 34.0%", xy=(34.0, 250), xytext=(19, 190),
                fontsize=8, color=BLUE, arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    ax.annotate("GNI p.c. 40.4%\nMean yrs schooling 40.7%\nHDI composite 42.4%",
                xy=(41.2, 250), xytext=(27.5, 330), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_xlim(0, 50)
    ax.set_xlabel("% of countries in which that single indicator is significant", fontsize=9)
    ax.set_ylabel(f"Number of SDG series (of {len(sdg_dist)})", fontsize=9)
    ax.set_title("c  Per indicator: the HDI dominates", fontsize=11,
                 fontweight="bold", color=INK, loc="left", pad=40)
    ax.text(0, 1.015,
            "No cross-framework normalisation at all. Note this sets the HDI's\n"
            "best against the SDG median — panel b shows that is generous.",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")

    for ax in axes:
        ax.set_facecolor(BG)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
        ax.set_axisbelow(True)

    fig.text(0.005, 0.975,
             "HDI versus the SDG framework: three comparisons, no single verdict",
             fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.005, 0.020,
             "Benjamini–Hochberg FDR-corrected within country against WHR happiness. "
             "SDG series in panel c restricted to those measured in ≥8 countries. "
             "Sources: UN SDG Global Database; UNDP HDR; World Happiness Report.",
             fontsize=8, color=GREY, va="bottom")
    fig.tight_layout(rect=(0, 0.05, 1, 0.905))
    out = "figures_out/I1_framework_three_comparisons.png"
    fig.savefig(out, dpi=200, facecolor=BG)
    print(f"Saved: {out}\n")

    for label, k, n, note, _ in d["detect"]:
        print(f"  (a) {label:16s} {k:3d}/{n}  ({100*k/n:.0f}%)   {note}")
    print(f"  (b) SDG 5 random series : {boot.mean():.0f}%  (95% range {lo:.0f}-{hi:.0f}%)")
    print(f"  (b) HDI its own 5, same {d['n_matched']} countries : {d['hdi_matched']:.0f}%")
    print(f"  (c) SDG series: median {np.median(sdg_dist):.1f}%, {zero:.0f}% at zero, "
          f"max {sdg_dist.max():.1f}%")
    for k, v in hdi_pts.items():
        print(f"      {HDI_LABELS[k]:24s} {v:5.1f}%  beats {(sdg_dist < v).mean()*100:.0f}%")


if __name__ == "__main__":
    main()
