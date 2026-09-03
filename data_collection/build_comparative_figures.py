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
def detection_rate(rho, n_obs, n_units, draws=400, seed=1):
    """Share of units a per-unit time-series test recovers when the association is REAL.

    The collapse design tests each unit's own time series, so its power is set
    by the length of that series, not by how many units there are. This is what
    decides whether a null result means "no association" or "too few years".
    """
    rng = np.random.default_rng(seed)
    cov = [[1, rho], [rho, 1]]
    out = []
    for _ in range(draws):
        ps = [stats.pearsonr(*rng.multivariate_normal([0, 0], cov, size=n_obs).T)[1]
              for _ in range(n_units)]
        out.append(bh(ps).mean())
    return 100 * float(np.mean(out))


def ts_levels_diffs(panel, unit, xcol, ycol, tcol="year", minn=5):
    """Per unit: time-series levels vs first differences, one unit for both halves.

    This is the design the SDG paper uses. Both halves are FDR-corrected across
    the same family of units, so the two bars for a pairing are comparable to
    each other and to the other pairings.
    """
    lp, dp, ns = [], [], []
    for _, g in panel.groupby(unit):
        g = g.sort_values(tcol).dropna(subset=[xcol, ycol])
        if len(g) < minn:
            continue
        if g[xcol].std() > 0 and g[ycol].std() > 0:
            lp.append(stats.pearsonr(g[xcol], g[ycol])[1])
            ns.append(len(g))
        dx, dy = np.diff(g[xcol]), np.diff(g[ycol])
        if len(dx) >= 4 and dx.std() > 0 and dy.std() > 0:
            dp.append(stats.pearsonr(dx, dy)[1])
    return 100 * bh(lp).mean(), 100 * bh(dp).mean(), len(lp), float(np.median(ns))


def collapse_and_its_limits():
    """The collapse across three pairings, same unit within each.

    An earlier version took the third pairing's levels from a cross-section
    across regions and its differences from a time series within regions,
    which made the two halves incomparable; that is fixed here. A later
    version added a second panel simulating detection power by series length,
    to explain why the third pairing looks weak -- dropped in favour of a
    single panel, with the power caveat carried in the footnote and the beat
    text instead. The detection-rate simulation (detection_rate()) still
    backs the "7 rounds is underpowered" claim in the text; it is just not
    drawn.

    The third pairing swaps only the wellbeing instrument: same HDI, same
    countries, Cantril ladder replaced by ESS life satisfaction. It runs on
    seven survey rounds instead of thirteen years and comes back weak in
    levels AND inverted (differences above levels), which is not a pattern a
    real association produces -- the hatching and the footnote flag that
    without a second panel to prove it.
    """
    nat = pd.read_csv("processed/country_round_panel.csv")
    ess_lv, ess_df, ess_n, ess_yrs = ts_levels_diffs(nat, "cntry", "hdi", "stflife")

    # separate corroboration: across regions inside each country, a cross-section
    r = pd.read_csv("processed/region_round_panel.csv")
    lv = []
    for _, g in r.groupby("cntry"):
        g = g.dropna(subset=["shdi", "stflife"])
        if g.region_key.nunique() >= 8:
            lv.append(stats.pearsonr(g["shdi"], g["stflife"])[1])
    reg_levels, n_ctry = 100 * bh(lv).mean(), len(lv)

    fig, ax = plt.subplots(figsize=(11, 6.2))
    fig.patch.set_facecolor(BG)

    pairings = [("SDG x WHR\n42 countries\n~13 years each", 71.0, 5.0, True),
                ("HDI x WHR\n150 countries\n~13 years each", 42.0, 2.0, True),
                (f"HDI x ESS\n{ess_n} countries\n{ess_yrs:.0f} rounds each", ess_lv, ess_df, False)]
    x, w = np.arange(len(pairings)), 0.32
    b1 = ax.bar(x - w / 2, [p[1] for p in pairings], w, label="Levels", color=BLUE, alpha=0.85)
    b2 = ax.bar(x + w / 2, [p[2] for p in pairings], w, label="First differences", color=RED, alpha=0.85)
    for bar, p in zip(list(b1) + list(b2), [q for q in pairings] * 2):
        if not p[3]:
            bar.set_alpha(0.32)
            bar.set_hatch("///")
    label_bars(ax, b1, [f"{p[1]:.0f}%" for p in pairings])
    label_bars(ax, b2, [f"{p[2]:.0f}%" for p in pairings])
    ax.set_xticks(x)
    ax.set_xticklabels([p[0] for p in pairings], fontsize=10)
    ax.set_ylabel("% of countries FDR-significant (q < .05)", fontsize=10.5)
    ax.set_ylim(0, 85)
    ax.legend(fontsize=10, loc="upper right", frameon=False)
    ax.annotate("hatched: 7 rounds, underpowered.\ndifferences above levels is\nthe signature of a test that\nis not working, not a result",
                xy=(2.16, max(ess_lv, ess_df)), xytext=(1.32, 48), fontsize=8.5,
                color=MUTED, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
    style_axes(ax)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)

    heading(fig, "The collapse holds under both well-powered pairings",
            "Levels and first differences, per country, on the same unit for both halves of each pairing.",
            f"All bars are Benjamini-Hochberg FDR at q < .05, corrected across the units shown, with levels and differences on the same units.\n"
            f"The ESS does contribute a well-powered levels result, just not a time-series one: across regions inside each country, subnational HDI predicts\n"
            f"ESS life satisfaction in {reg_levels:.0f}% of {n_ctry} countries -- close to the 42% the HDI reaches nationally, and with an independent wellbeing instrument.")
    fig.tight_layout(rect=(0, 0.11, 1, 0.86))
    path = f"{OUT_DIR}/ess_levels_diffs_collapse.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}  [ESS cross-sectional levels: {reg_levels:.1f}% of {n_ctry}]")


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
    collapse_and_its_limits()
    domains_at_levels()
    education_deep_dive()
    health_deep_dive()
    trust_deep_dive()


# --------------------------------------------------------------------------
# Act II-a -- which domains survive the differences test, pooled for power
# --------------------------------------------------------------------------
def pooled_within(panel, unit, x, y, t="year"):
    """Within-country levels and first differences, pooled across all countries.

    The per-country design the SDG paper uses spends its power on 25-150
    separate tests of ~7 points each. Pooling asks the same within-country
    question of every country at once, which is the difference between no
    verdict and a clear one.
    """
    d = panel.dropna(subset=[x, y]).copy()
    keep = d.groupby(unit)[x].transform("count") >= 3
    d = d[keep]
    xd = d[x] - d.groupby(unit)[x].transform("mean")
    yd = d[y] - d.groupby(unit)[y].transform("mean")
    lr, lp = stats.pearsonr(xd, yd)

    dx, dy = [], []
    for _, g in panel.groupby(unit):
        g = g.sort_values(t).dropna(subset=[x, y])
        if len(g) >= 3:
            dx += list(np.diff(g[x]))
            dy += list(np.diff(g[y]))
    dr, dp = stats.pearsonr(np.array(dx), np.array(dy))
    return {"levels_r": lr, "levels_p": lp, "levels_n": len(d),
            "diffs_r": dr, "diffs_p": dp, "diffs_n": len(dx)}


def cluster_ols_fd(panel, unit, x, y, t="essround"):
    """Delta y on Delta x with round fixed effects; SEs clustered by unit.

    A correlation says two things move together; this says by how much, in the
    outcome's own units, which is what a reader needs to judge whether the
    differences result is a curiosity or something worth building policy on.
    """
    dx_rows = []
    for u, g in panel.groupby(unit):
        g = g.sort_values(t).dropna(subset=[x, y])
        if len(g) < 3:
            continue
        rd = g[t].to_numpy()
        for i, (ddx, ddy) in enumerate(zip(np.diff(g[x]), np.diff(g[y]))):
            dx_rows.append((u, rd[i + 1], ddx, ddy))
    d = pd.DataFrame(dx_rows, columns=[unit, "round", "dx", "dy"])
    X = pd.get_dummies(d["round"], prefix="r", drop_first=True).astype(float)
    X.insert(0, "dx", d.dx.values)
    X.insert(0, "const", 1.0)
    Xv, yv = X.values, d.dy.values
    XtXi = np.linalg.pinv(Xv.T @ Xv)
    beta = XtXi @ Xv.T @ yv
    resid = yv - Xv @ beta
    meat = np.zeros((Xv.shape[1],) * 2)
    for u in d[unit].unique():
        m = (d[unit] == u).values
        score = Xv[m].T @ resid[m]
        meat += np.outer(score, score)
    G, n, k = d[unit].nunique(), *Xv.shape
    V = XtXi @ meat @ XtXi * (G / (G - 1)) * ((n - 1) / (n - k))
    se = np.sqrt(np.diag(V))
    b, b_se = beta[1], se[1]
    t_stat = b / b_se
    sd_x, sd_y = d.dx.std(), d.dy.std()
    return {"b": b, "se": b_se, "t": t_stat, "sd_x": sd_x, "sd_y": sd_y,
            "effect_1sd": b * sd_x, "pct_of_typical_move": 100 * b * sd_x / sd_y, "n": n, "G": G}


def which_domains_survive_differences():
    """Does within-country CHANGE in each domain track change in wellbeing -- and by how much?

    This is the test the deck previously tried to answer with HDI x ESS, which
    only ever asked whether the development composite tracks ESS wellbeing. The
    substantive question is about the domain measures themselves, and the
    substantive answer needs a magnitude, not just a correlation: panel a
    converts the differences result into life-satisfaction points so a 1 SD
    change in a country's trust or health reading between ESS rounds has a
    concrete size, benchmarked against how much life satisfaction typically
    moves round to round.
    """
    p = pd.read_csv("processed/country_round_panel.csv")
    p["good_health"] = 6 - p["health"]
    nat = pd.read_csv("processed/national_hdi_shdi_whr_panel.csv")

    same = [("Education", "eduyrs"), ("Health", "good_health"), ("Social trust", "ppltrst"),
            ("HDI composite", "hdi")]
    rows = []
    for lab, v in same:
        r = pooled_within(p, "cntry", v, "stflife")
        rows.append({"predictor": lab, "outcome": "ESS life satisfaction", "source": "same survey", **r})
    for lab, v in same[:3]:
        r = pooled_within(p, "cntry", v, "whr_happiness")
        rows.append({"predictor": lab, "outcome": "WHR ladder", "source": "cross-source", **r})
    r = pooled_within(nat, "iso3", "hdi", "whr_happiness")
    rows.append({"predictor": "HDI composite", "outcome": "WHR ladder", "source": "cross-source", **r})
    res = pd.DataFrame(rows)
    res.to_csv("processed/pooled_within_country_domains.csv", index=False)
    print("Saved: processed/pooled_within_country_domains.csv")

    eff = pd.DataFrame([{"predictor": lab, **cluster_ols_fd(p, "cntry", v, "stflife")}
                        for lab, v in same]).set_index("predictor")
    eff.to_csv("processed/differences_effect_sizes.csv")
    print("Saved: processed/differences_effect_sizes.csv")

    def star(pv):
        return "***" if pv < .001 else "**" if pv < .01 else "*" if pv < .05 else "n.s."

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.5, 5.9), gridspec_kw={"width_ratios": [1, 1.05]})
    fig.patch.set_facecolor(BG)
    palette = {"Education": BLUE, "Health": RED, "Social trust": GREEN, "HDI composite": "#7A6BC4"}
    order = ["Social trust", "Health", "HDI composite", "Education"]

    # -- panel a: the headline -- effect size in ESS life-satisfaction points --
    typical_move = eff.loc["Social trust", "sd_y"]
    xs = np.arange(len(order))
    vals = [eff.loc[k, "effect_1sd"] for k in order]
    cols = [palette[k] for k in order]
    sig = [eff.loc[k, "t"] for k in order]
    bars = axA.bar(xs, vals, color=cols, width=0.6)
    for bar, tt in zip(bars, sig):
        bar.set_alpha(0.9 if abs(tt) >= 1.96 else 0.35)
    for i, k in enumerate(order):
        row = eff.loc[k]
        pct = row.pct_of_typical_move
        lab = f"+{row.effect_1sd:.2f} pts" if row.t >= 1.96 else f"+{row.effect_1sd:.2f} pts (n.s.)"
        sub = f"{pct:.0f}% of a typical\nround-to-round move" if row.t >= 1.96 else ""
        axA.text(i, row.effect_1sd + 0.008, lab, ha="center", va="bottom", fontsize=9.5,
                 fontweight="bold", color=INK if row.t >= 1.96 else GREY)
        if sub:
            axA.text(i, row.effect_1sd + 0.038, sub, ha="center", va="bottom", fontsize=7.8, color=MUTED)
    axA.axhline(0, color=INK, lw=0.9)
    axA.set_xticks(xs)
    axA.set_xticklabels(order, fontsize=9.5)
    axA.set_ylabel("ESS life-satisfaction points, per 1 SD change\nin the predictor between survey rounds", fontsize=9.5)
    axA.set_ylim(0, 0.26)
    axA.set_title("a  What the differences result is worth, in points", fontsize=11.5,
                  fontweight="bold", color=INK, loc="left")
    style_axes(axA)
    axA.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    axA.set_axisbelow(True)

    # -- panel b: the evidence behind it -- correlations, levels vs diffs, split-half --
    d = res[res.source == "same survey"].set_index("predictor").loc[order].reset_index()
    x, w = np.arange(len(d)), 0.34
    cols2 = [palette[k] for k in d.predictor]
    b1 = axB.bar(x - w / 2, d.levels_r, w, color=cols2, alpha=0.9, label="Levels (within country)")
    b2 = axB.bar(x + w / 2, d.diffs_r, w, color=cols2, alpha=0.38, hatch="///",
                edgecolor="white", label="First differences")
    for bar, rv, pv in list(zip(b1, d.levels_r, d.levels_p)) + list(zip(b2, d.diffs_r, d.diffs_p)):
        axB.text(bar.get_x() + bar.get_width() / 2, max(rv, 0) + 0.018,
                 f"{rv:+.2f}\n{star(pv)}", ha="center", va="bottom", fontsize=8.5,
                 fontweight="bold", color=INK if pv < .05 else GREY)
    axB.axhline(0, color=INK, lw=0.9)
    axB.set_xticks(x)
    axB.set_xticklabels(d.predictor, fontsize=9.5)
    axB.set_ylabel("pooled within-country correlation", fontsize=10)
    axB.set_ylim(-0.09, 0.78)
    axB.set_title("b  The correlation evidence behind it", fontsize=11.5,
                  fontweight="bold", color=INK, loc="left")
    style_axes(axB)
    axB.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    axB.set_axisbelow(True)

    sh = split_half_differences().set_index("domain")
    first = True
    for i, name in enumerate(d.predictor):
        if name not in sh.index:
            continue
        row = sh.loc[name]
        axB.errorbar(i + w / 2, row.split_half_r,
                     yerr=[[row.split_half_r - row.lo], [row.hi - row.split_half_r]],
                     fmt="D", ms=6, color=INK, ecolor=INK, elinewidth=1.4, capsize=4, zorder=6,
                     label="Split-half: no shared respondents" if first else None)
        first = False
    axB.legend(fontsize=8.5, loc="upper right", frameon=False)

    heading(fig, "The trust and health differences are not just significant -- they move life satisfaction",
            f"Pooled across countries, round fixed effects, SEs clustered by country. A typical round-to-round swing in life satisfaction is {typical_move:.2f} points.",
            "Panel a: OLS of the change in life satisfaction on the change in the predictor, converted to points per 1 SD change (grey = not significant at .05).\n"
            "Panel b: the correlations behind panel a, with split-half diamonds -- predictor and outcome from disjoint respondents, so trust's +0.59 is not two\n"
            "questions answered by the same person in the same sitting. It retains 93% of its estimate; health retains 88%.")
    fig.tight_layout(rect=(0, 0.11, 1, 0.85))
    path = f"{OUT_DIR}/domains_survive_differences.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close()
    print(f"Saved: {path}")
    print(eff.round(4).to_string())
    print(res[["predictor", "outcome", "levels_r", "levels_p", "diffs_r", "diffs_p", "diffs_n"]].to_string(index=False))


SPLIT_CACHE = "processed/ess_split_half_differences.csv"


def split_half_differences(n_splits=120, rebuild=False):
    """Does the within-ESS differences result survive removing shared respondents?

    The cross-source check against the WHR ladder is ambiguous: it fails for
    trust, but it also pairs two different samples with different fieldwork
    timing, and differencing amplifies that mismatch. This test isolates the
    common-method question instead. Within each country-round, respondents are
    split at random: the predictor mean comes from one half, the outcome mean
    from the other. No person contributes to both sides, but sample, fieldwork
    and timing are held identical. If the association were an artefact of the
    same people answering both questions, it would vanish here.
    """
    from pathlib import Path
    if Path(SPLIT_CACHE).exists() and not rebuild:
        return pd.read_csv(SPLIT_CACHE)

    import pyreadstat
    df, _ = pyreadstat.read_sav(ESS_SAV)
    for c in ["stflife", "ppltrst", "health", "eduyrs"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df.loc[df.stflife > 10, "stflife"] = np.nan
    df.loc[df.ppltrst > 10, "ppltrst"] = np.nan
    df.loc[df.health > 5, "health"] = np.nan
    df.loc[df.eduyrs > 40, "eduyrs"] = np.nan
    df["good_health"] = 6 - df["health"]

    def fd(panel, x, y):
        dx, dy = [], []
        for _, g in panel.groupby("cntry"):
            g = g.sort_values("essround").dropna(subset=[x, y])
            if len(g) >= 3:
                dx += list(np.diff(g[x]))
                dy += list(np.diff(g[y]))
        return stats.pearsonr(np.array(dx), np.array(dy))[0]

    rng = np.random.default_rng(7)
    rows = []
    for var, lab in [("good_health", "Health"), ("ppltrst", "Social trust"), ("eduyrs", "Education")]:
        d = df[["cntry", "essround", var, "stflife"]].dropna()
        rs = []
        for _ in range(n_splits):
            h = rng.random(len(d)) < 0.5
            A = d[h].groupby(["cntry", "essround"])[var].mean().rename("x")
            B = d[~h].groupby(["cntry", "essround"])["stflife"].mean().rename("y")
            rs.append(fd(pd.concat([A, B], axis=1).dropna().reset_index(), "x", "y"))
        same = d.groupby(["cntry", "essround"]).agg(x=(var, "mean"), y=("stflife", "mean")).reset_index()
        rows.append({"domain": lab, "same_sample_r": fd(same, "x", "y"),
                     "split_half_r": float(np.mean(rs)),
                     "lo": float(np.percentile(rs, 2.5)), "hi": float(np.percentile(rs, 97.5)),
                     "n_splits": n_splits})
    out = pd.DataFrame(rows)
    out.to_csv(SPLIT_CACHE, index=False)
    print(f"Saved: {SPLIT_CACHE}")
    return out


def differences_robustness(save=True):
    """Both ESS outcomes, with and without common time shocks removed.

    Two robustness questions at once. First, the brief always said "life
    satisfaction and happiness", so both ESS outcome items are run. Second,
    the ESS panel is 25 European countries over 7 rounds, where a shared shock
    (2008-09, 2020) moves everyone together and can manufacture a pooled
    first-difference correlation. Demeaning each difference by survey round
    removes anything common to a round and leaves only idiosyncratic
    country-level movement.

    The HDI's differences result against ESS happiness halves under that
    control (+0.31 -> +0.17), so most of the gap between the two ESS outcomes
    was shared shocks. Health and social trust are unaffected.
    """
    p = pd.read_csv("processed/country_round_panel.csv")
    p["good_health"] = 6 - p["health"]
    rows = []
    for var, lab in [("hdi", "HDI composite"), ("good_health", "Health"),
                     ("ppltrst", "Social trust"), ("eduyrs", "Education")]:
        for out in ["stflife", "happy"]:
            recs = []
            for c, g in p.groupby("cntry"):
                g = g.sort_values("essround").dropna(subset=[var, out])
                if len(g) < 3:
                    continue
                rd = g.essround.to_numpy()
                recs += [(rd[i + 1], dx, dy) for i, (dx, dy)
                         in enumerate(zip(np.diff(g[var]), np.diff(g[out])))]
            d = pd.DataFrame(recs, columns=["round", "dx", "dy"])
            r0, p0 = stats.pearsonr(d.dx, d.dy)
            xa = d.dx - d.groupby("round").dx.transform("mean")
            ya = d.dy - d.groupby("round").dy.transform("mean")
            r1, p1 = stats.pearsonr(xa, ya)
            rows.append({"predictor": lab, "outcome": out, "n_diffs": len(d),
                         "diffs_r": r0, "diffs_p": p0,
                         "diffs_r_round_fe": r1, "diffs_p_round_fe": p1})
    out = pd.DataFrame(rows)
    if save:
        out.to_csv("processed/differences_robustness.csv", index=False)
        print("Saved: processed/differences_robustness.csv")
    return out
