"""
Comparative figures for the reframed narrative.

Every panel in this file reports ONE unit: the percentage of units (countries,
or regions) in which the association is Benjamini-Hochberg FDR-significant at
q < .05. That is the same test the SDG paper and the HDI replication use, so
the bars can be read side by side.

A note on why that matters. An earlier version of this file scored the ESS
bars as "R-squared > 0.04" on ~7 country-round means. At n = 7, two-thirds of
PURE NOISE series clear R-squared > 0.04, so those bars measured sample size,
not association, and they were being plotted against FDR-corrected bars from
the other frameworks. The ESS domain figures below are therefore computed from
the individual respondent file (351,023 respondents, ~10,700 per country),
demeaned within country-round so the association is within-country and
within-year by construction.

    python build_comparative_figures.py
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

OUT_DIR = "figures_out"
ESS_SAV = "raw/ess_extract.sav"
ESS_CACHE = "processed/ess_individual_domain_fdr.csv"

BLUE = "#2A78D6"
GREEN = "#1BAF7A"
RED = "#E34948"
GREY = "#8A8A8A"
BG = "#FCFCFB"
INK = "#1A1A1A"
MUTED = "#52514E"

DOMAINS = [("eduyrs", "Education"), ("good_health", "Health"), ("ppltrst", "Social trust")]


def bh(pvals, alpha=0.05):
    """Benjamini-Hochberg. Returns a boolean mask of rejected nulls."""
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    order = np.argsort(p)
    below = np.where(p[order] <= alpha * np.arange(1, n + 1) / n)[0]
    out = np.zeros(n, dtype=bool)
    if len(below):
        out[order[: below.max() + 1]] = True
    return out


def style_axes(ax):
    ax.set_facecolor(BG)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def label_bars(ax, bars, labels, size=9.5):
    for bar, text in zip(bars, labels):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, text, ha="center",
                va="bottom", fontsize=size, fontweight="bold", color=INK)


def heading(fig, title, subtitle, footnote=None):
    fig.text(0.05, 0.97, title, fontsize=14, fontweight="bold", color=INK, va="top")
    fig.text(0.05, 0.915, subtitle, fontsize=9.5, color=MUTED, va="top")
    if footnote:
        fig.text(0.05, 0.03, footnote, fontsize=7.5, color=GREY, va="bottom", style="italic")


# --------------------------------------------------------------------------
# Individual-level ESS: the only level at which the domain items are measured
# --------------------------------------------------------------------------
def ess_individual_fdr(rebuild=False):
    """% of ESS countries where each domain predicts life satisfaction.

    Estimated across respondents within each country, demeaned within
    country-round so no part of the association can come from between-country
    differences or from a common year shock. FDR-corrected across countries.
    """
    from pathlib import Path
    if Path(ESS_CACHE).exists() and not rebuild:
        return pd.read_csv(ESS_CACHE)

    import pyreadstat
    df, _ = pyreadstat.read_sav(ESS_SAV)
    for c in ["stflife", "ppltrst", "health", "eduyrs"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    # ESS codes refusals / don't-knows above the scale maximum
    df.loc[df.stflife > 10, "stflife"] = np.nan
    df.loc[df.ppltrst > 10, "ppltrst"] = np.nan
    df.loc[df.health > 5, "health"] = np.nan
    df.loc[df.eduyrs > 40, "eduyrs"] = np.nan
    df["good_health"] = 6 - df["health"]  # reverse so higher = better health

    rows = []
    for var, label in DOMAINS:
        per_country = []
        for cntry, g in df.groupby("cntry"):
            g = g[["stflife", var, "essround"]].dropna()
            if len(g) < 200:
                continue
            x = (g[var] - g.groupby("essround")[var].transform("mean")).to_numpy()
            y = (g["stflife"] - g.groupby("essround")["stflife"].transform("mean")).to_numpy()
            if x.std() == 0 or y.std() == 0:
                continue
            r, p = stats.pearsonr(x, y)
            per_country.append((cntry, r ** 2, p, len(g)))
        d = pd.DataFrame(per_country, columns=["cntry", "r2", "p", "n"])
        sig = bh(d.p.values)
        rows.append({"domain": label, "n_countries": len(d), "n_sig": int(sig.sum()),
                     "pct_sig": 100 * sig.mean(), "median_r2": d.r2.median(),
                     "median_n": d.n.median()})
    out = pd.DataFrame(rows)
    out.to_csv(ESS_CACHE, index=False)
    print(f"Saved: {ESS_CACHE}")
    return out


def hdi_fdr():
    """% of the 150 HDI countries FDR-significant at levels, by component."""
    h = pd.read_csv("processed/hdi_country_indicator_significance.csv")
    return {ind: 100 * (g.sig_levels_fdr == "q<.05").mean() for ind, g in h.groupby("indicator")}


def sdg_goal_pct():
    s = pd.read_csv("processed/sdg_goal_significance_pooled.csv")
    s = s[s.Goal != "Goal"].copy()
    s["Goal"] = pd.to_numeric(s.Goal)
    return dict(zip(s.Goal, s.pct_sig_levels.astype(float)))


# --------------------------------------------------------------------------
# Act I -- the collapse, replicated three ways
# --------------------------------------------------------------------------
def collapse_three_ways():
    """SDG x WHR, HDI x WHR, and SHDI x ESS: levels hold, differences do not."""
    r = pd.read_csv("processed/region_round_panel.csv")

    # Levels, one spatial scale down: across regions inside each country
    lv = []
    for _, g in r.groupby("cntry"):
        g = g.dropna(subset=["shdi", "stflife"])
        if g.region_key.nunique() >= 8:
            lv.append(stats.pearsonr(g["shdi"], g["stflife"])[1])
    reg_levels = 100 * bh(lv).mean()

    # Differences, within each region over survey rounds
    df_p = []
    for _, g in r.groupby("region_key"):
        g = g.sort_values("year").dropna(subset=["shdi", "stflife"])
        if len(g) >= 5:
            dx, dy = np.diff(g["shdi"]), np.diff(g["stflife"])
            if dx.std() > 0 and dy.std() > 0:
                df_p.append(stats.pearsonr(dx, dy)[1])
    reg_diffs = 100 * bh(df_p).mean()

    pairings = [
        (f"SDG x WHR\n42 countries\n661 series", 71.0, 5.0),
        (f"HDI x WHR\n150 countries\ncomposite index", 42.0, 2.0),
        (f"SHDI x ESS\n{len(lv)} countries / {len(df_p)} regions\nsubnational", reg_levels, reg_diffs),
    ]

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(BG)
    x = np.arange(len(pairings))
    w = 0.36
    lvl = [p[1] for p in pairings]
    dif = [p[2] for p in pairings]
    b1 = ax.bar(x - w / 2, lvl, w, label="Levels", color=BLUE, alpha=0.85)
    b2 = ax.bar(x + w / 2, dif, w, label="First differences", color=RED, alpha=0.85)
    label_bars(ax, b1, [f"{v:.0f}%" for v in lvl])
    label_bars(ax, b2, [f"{v:.0f}%" for v in dif])

    ax.set_xticks(x)
    ax.set_xticklabels([p[0] for p in pairings], fontsize=9.5)
    ax.set_ylabel("% of units FDR-significant (q < .05)", fontsize=10.5)
    ax.set_ylim(0, 85)
    ax.legend(fontsize=9.5, loc="upper right", frameon=False)
    style_axes(ax)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)

    heading(fig, "The collapse replicates: swap the framework, swap the wellbeing measure, swap the scale",
            "Change one leg of the design at a time. Levels stay informative; differences go to almost nothing in every pairing.",
            "Every bar is the same test: Benjamini-Hochberg FDR at q < .05, corrected within the family of units shown.\n"
            "SHDI x ESS levels are estimated across regions inside each country; its differences within each region over survey rounds.")
    fig.tight_layout(rect=(0, 0.07, 1, 0.87))
    path = f"{OUT_DIR}/ess_levels_diffs_collapse.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}")


# --------------------------------------------------------------------------
# Act II / II-a -- the three domains
# --------------------------------------------------------------------------
def domains_at_levels():
    """All three domains, each framework, one unit."""
    ess = ess_individual_fdr().set_index("domain")
    hdi = hdi_fdr()
    sdg = sdg_goal_pct()

    spec = [
        ("Education", BLUE, hdi["eys"], sdg[4]),
        ("Health", RED, hdi["le"], sdg[3]),
        ("Social trust", GREEN, None, sdg[16]),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5.4))
    fig.patch.set_facecolor(BG)
    for ax, (domain, color, hdi_val, sdg_val) in zip(axes, spec):
        ess_val = ess.loc[domain, "pct_sig"]
        vals = [ess_val, 0 if hdi_val is None else hdi_val, sdg_val]
        names = ["ESS\n36 countries\n(individual)", "HDI\n150 countries\n(country)",
                 "SDG\n42-74 countries\n(country-indicator)"]
        bars = ax.bar(names, vals, color=[color, color, GREY], alpha=0.85)
        if hdi_val is None:
            bars[1].set_alpha(0.15)
            ax.text(1, 2.5, "not measured", ha="center", fontsize=8, color=GREY, style="italic")
        labels = [f"{ess_val:.0f}%", "" if hdi_val is None else f"{hdi_val:.0f}%", f"{sdg_val:.1f}%"]
        label_bars(ax, bars, labels, size=10)
        ax.set_ylabel("% of countries FDR-significant", fontsize=9)
        ax.set_title(domain, fontsize=11.5, fontweight="bold", color=INK)
        ax.set_ylim(0, 115)
        ax.tick_params(labelsize=8.5)
        style_axes(ax)
        ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
        ax.set_axisbelow(True)

    heading(fig, "Three domains, three frameworks, one unit",
            "% of countries where the domain predicts life satisfaction at levels, FDR-corrected. "
            "ESS is measured across respondents; the HDI and SDG frameworks across country-years.",
            "The ESS bars are the same domains measured on people rather than on national aggregates. "
            "Social trust has no HDI counterpart at all, and its SDG counterpart measures confidence in institutions rather than trust in people.")
    fig.tight_layout(rect=(0, 0.07, 1, 0.86))
    path = f"{OUT_DIR}/domains_at_levels_comparison.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}")


def education_deep_dive():
    ess = ess_individual_fdr().set_index("domain")
    hdi = hdi_fdr()
    edu = pd.read_csv("processed/sdg_education_category_significance.csv")
    access = float(edu.loc[edu.edu_category == "Access & Participation", "pct_sig_levels"].iloc[0])
    pooled = sdg_goal_pct()[4]

    names = ["ESS\n36 countries\n(years of schooling,\nindividual)",
             "HDI\n150 countries\n(expected years\nof schooling)",
             "SDG4 access only\n~42 countries\n(2 series,\n63 country-pairs)",
             "SDG4 pooled\n~42 countries\n(all 35 series)"]
    vals = [ess.loc["Education", "pct_sig"], hdi["eys"], access, pooled]

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(BG)
    bars = ax.bar(names, vals, color=BLUE, width=0.6)
    for bar, a in zip(bars, [0.85, 0.85, 0.85, 0.35]):
        bar.set_alpha(a)
    label_bars(ax, bars, [f"{vals[0]:.0f}%", f"{vals[1]:.0f}%", f"{access:.1f}%", f"{pooled:.1f}%"], size=10)
    ax.set_ylabel("% of countries FDR-significant", fontsize=11)
    ax.set_ylim(0, 100)
    ax.tick_params(labelsize=9)
    style_axes(ax)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)

    heading(fig, "Education: the construct you count decides the answer",
            "% of countries where education predicts life satisfaction at levels, FDR-corrected.",
            "SDG4 pools 35 series. Access and participation reach 12.7%, but parity ratios (18 of the 35 series) reach 2.5%, "
            "infrastructure 2.0% and learning outcomes 0.9%, so the pooled rate lands at 3.3% -- below the weakest thing in it that works.")
    fig.tight_layout(rect=(0, 0.09, 1, 0.86))
    path = f"{OUT_DIR}/education_levels_comparison.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}")


def health_deep_dive():
    ess = ess_individual_fdr().set_index("domain")
    hdi = hdi_fdr()
    sdg3 = sdg_goal_pct()[3]

    names = ["ESS\n36 countries\n(self-rated health,\nindividual)",
             "HDI\n150 countries\n(life expectancy)",
             "SDG3\n~45 countries\n(country-indicator)"]
    vals = [ess.loc["Health", "pct_sig"], hdi["le"], sdg3]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    bars = ax.bar(names, vals, color=RED, alpha=0.85, width=0.6)
    label_bars(ax, bars, [f"{vals[0]:.0f}%", f"{vals[1]:.0f}%", f"{sdg3:.1f}%"], size=10)
    ax.set_ylabel("% of countries FDR-significant", fontsize=11)
    ax.set_ylim(0, 115)
    ax.tick_params(labelsize=9)
    style_axes(ax)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)

    heading(fig, "Health: strongest on people, weakest in the HDI",
            "% of countries where health predicts life satisfaction at levels, FDR-corrected.",
            "Life expectancy is the weakest of the HDI's five components (19% against 41% for mean years of schooling). "
            "It has also nearly saturated: the top 100 countries sit between 81 and 85 years, leaving little left to correlate with.")
    fig.tight_layout(rect=(0, 0.07, 1, 0.86))
    path = f"{OUT_DIR}/health_levels_comparison.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}")


def trust_deep_dive():
    ess = ess_individual_fdr().set_index("domain")
    sdg16 = sdg_goal_pct()[16]
    ess_val = ess.loc["Social trust", "pct_sig"]

    names = ["ESS\n36 countries\n(interpersonal trust:\n'most people can be trusted')",
             "SDG16\n~74 countries\n(institutional confidence)*",
             "HDI\n150 countries\n(not measured)"]
    vals = [ess_val, sdg16, 0]

    fig, ax = plt.subplots(figsize=(10.5, 6))
    fig.patch.set_facecolor(BG)
    bars = ax.bar(names, vals, color=[GREEN, GREY, GREY], alpha=0.85, width=0.6)
    bars[2].set_alpha(0.15)
    label_bars(ax, bars[:2], [f"{ess_val:.0f}%", f"{sdg16:.1f}%"], size=10)
    ax.text(2, 2.5, "no counterpart", ha="center", fontsize=9, color=GREY, style="italic")
    ax.set_ylabel("% of countries FDR-significant", fontsize=11)
    ax.set_ylim(0, 115)
    ax.tick_params(labelsize=8.5)
    style_axes(ax)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)

    heading(fig, "Social trust: a coverage gap, not a measurement choice",
            "% of countries where trust predicts life satisfaction at levels, FDR-corrected.",
            "* SDG16's trust-adjacent series measure satisfaction with public services, perceived bribery and perceived inclusiveness in "
            "decision-making -- confidence in institutions, not trust in other people. They are a different construct, and the closest "
            "thing either framework carries.")
    fig.tight_layout(rect=(0, 0.09, 1, 0.86))
    path = f"{OUT_DIR}/trust_coverage_comparison.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}")


if __name__ == "__main__":
    print(ess_individual_fdr(rebuild=True).to_string(index=False))
    collapse_three_ways()
    domains_at_levels()
    education_deep_dive()
    health_deep_dive()
    trust_deep_dive()
