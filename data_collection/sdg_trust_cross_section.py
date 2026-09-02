"""
Can the SDG framework see social trust cross-sectionally, if not over time?

The deck's Act II result is a coverage statement: 147 of 163 trust/satisfaction
country-series carry too few years for the levels-and-differences design, so
they are never computed. That says the SDG framework cannot test trust *in this
design*. It does not say the framework carries no information about trust --
several of the series have real breadth ACROSS countries at one year apiece.

This runs the test the coverage allows: a pure cross-section of countries,
each series against the WHR Cantril ladder in the matching year.

Three things make the result harder to interpret than it looks, and all three
are reported:

  1. In a cross-section of countries almost everything correlates with the
     ladder, because almost everything correlates with income. So every series
     is also reported as a partial correlation net of log GNI per capita, and
     against HDI components computed on the SAME country set.
  2. SP_PSR_OSATIS_HLTH -- the broadest series by far -- is Gallup World Poll,
     the same survey that produces the WHR ladder. It is a same-instrument
     comparison, not independent corroboration, exactly the objection the deck
     raises against the ESS self-report measures.
  3. None of the 13 series measures interpersonal trust. They measure
     satisfaction with public services and experience of bribery. They are
     institutional-confidence proxies, and the commentary must not silently
     promote them to "trust".

Inputs:  raw/sdg_trust_series_values.csv  (pull_sdg_trust_series.py)
         raw/HDI_with_happiness.csv       (WHR ladder + HDI components)
Outputs: processed/sdg_trust_cross_section.csv
         figures_out/K1_sdg_trust_cross_section.png
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pycountry
from scipy import stats

MIN_COUNTRIES = 12          # below this a cross-section is not worth reporting
COMPARATORS = [("hdi", "HDI"), ("le", "Life expectancy"),
               ("mys", "Mean schooling"), ("eys", "Expected schooling"),
               ("gnipc", "GNI per capita (log)")]


def m49_to_iso3(code) -> str | None:
    try:
        return pycountry.countries.get(numeric=str(int(code)).zfill(3)).alpha_3
    except Exception:
        return None


def load_outcome() -> pd.DataFrame:
    """Country-year ladder plus the HDI components, wide."""
    h = pd.read_csv("raw/HDI_with_happiness.csv")
    wide = h.pivot_table(index=["iso3", "year"], columns="indicatorCode",
                         values="value").reset_index()
    lad = h[["iso3", "year", "happiness"]].drop_duplicates()
    out = wide.merge(lad, on=["iso3", "year"], how="left")
    out["gnipc"] = np.log(out["gnipc"])
    return out


def load_series() -> pd.DataFrame:
    s = pd.read_csv("raw/sdg_trust_series_values.csv")
    s["iso3"] = s.geoAreaCode.map(m49_to_iso3)
    # the unmatched codes are regional and global aggregates, not countries
    return s.dropna(subset=["iso3"])


def partial_r(x, y, z):
    """r(x,y) with z partialled out of both."""
    rx = x - np.polyval(np.polyfit(z, x, 1), z)
    ry = y - np.polyval(np.polyfit(z, y, 1), z)
    return stats.pearsonr(rx, ry)


def cross_section(s: pd.DataFrame, out: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for code, g in s.groupby("SeriesCode"):
        m = g.merge(out, on=["iso3", "year"], how="inner").dropna(
            subset=["value", "happiness", "gnipc"])
        # one country, one observation: keep the most recent matched year
        m = m.sort_values("year").groupby("iso3", as_index=False).last()
        if len(m) < MIN_COUNTRIES:
            rows.append({"SeriesCode": code, "n": len(m), "skipped": True})
            continue

        r, p = stats.pearsonr(m["value"], m["happiness"])
        pr, pp = partial_r(m["value"].to_numpy(), m["happiness"].to_numpy(),
                           m["gnipc"].to_numpy())
        rec = {"SeriesCode": code,
               "SeriesDescription": g.SeriesDescription.iloc[0],
               "n": len(m), "skipped": False, "r": r, "p": p,
               "partial_r": pr, "partial_p": pp,
               "median_year": int(m.year.median()),
               "gallup": g.source.fillna("").str.contains("Gallup").mean()}
        # comparators on this series' own country set, so n and country mix
        # cannot be what separates them. Both specifications, because the
        # income-controlled one is only interpretable against them: net of log
        # GNI nothing survives cross-sectionally, the HDI included.
        for var, label in COMPARATORS:
            c = m.dropna(subset=[var])
            if len(c) >= MIN_COUNTRIES:
                rec[f"r_{var}"] = stats.pearsonr(c[var], c["happiness"])[0]
                if var != "gnipc":
                    rec[f"pr_{var}"] = partial_r(c[var].to_numpy(),
                                                 c["happiness"].to_numpy(),
                                                 c["gnipc"].to_numpy())[0]
        rows.append(rec)

    res = pd.DataFrame(rows)
    ok = res[~res.skipped].copy()
    # 13 series tested together, so correct within the family as elsewhere
    for col in ("p", "partial_p"):
        pv = ok[col].to_numpy()
        order = np.argsort(pv)
        q = np.empty_like(pv)
        q[order] = np.minimum.accumulate(
            (pv[order] * len(pv) / np.arange(1, len(pv) + 1))[::-1])[::-1]
        ok[col.replace("p", "q") if col == "p" else "partial_q"] = np.minimum(q, 1)
    return res.merge(ok[["SeriesCode", "q", "partial_q"]], on="SeriesCode", how="left")


SHORT = {
    "SP_PSR_OSATIS_HLTH": "Satisfied with healthcare",
    "SP_PSR_OSATIS_GOV": "Satisfied with government services",
    "SP_PSR_OSATIS_SEC": "Satisfied with secondary education",
    "SP_PSR_OSATIS_PRM": "Satisfied with primary education",
    "SP_PSR_SATIS_GOV": "Satisfied with government (users)",
    "SP_PSR_SATIS_HLTH": "Satisfied with healthcare (users)",
    "SP_PSR_SATIS_PRM": "Satisfied with primary education (users)",
    "SP_PSR_SATIS_SEC": "Satisfied with secondary education (users)",
    "IU_COR_BRIB": "Paid a bribe (individuals)",
    "IC_FRM_BRIB": "Paid a bribe (firms)",
    "IU_DMK_INCL": "Decision-making is inclusive",
    "IU_DMK_ICRS": "Decision-making is responsive",
    "VC_VOV_GDSD": "Experienced discrimination",
}

# panel (b) has no room for the full labels
TIGHT = {
    "SP_PSR_OSATIS_HLTH": "Satisfied\nhealthcare",
    "IU_COR_BRIB": "Bribe\n(individuals)",
    "IC_FRM_BRIB": "Bribe\n(firms)",
    "IU_DMK_INCL": "Inclusive\ndecisions",
    "VC_VOV_GDSD": "Experienced\ndiscrimination",
}


def figure(res: pd.DataFrame):
    BG, INK, GREY = "#FCFCFB", "#1A1A1A", "#8A8A8A"
    GREEN, ORANGE, RED, BLUE = "#1BAF7A", "#EDA100", "#E34948", "#2A78D6"

    d = res[~res.skipped].copy()
    d["absr"] = d.r.abs()
    d = d.sort_values("absr").reset_index(drop=True)
    # the widest series carries the comparator band; its country set is the
    # one the HDI components are strongest on, so it is the toughest benchmark
    ref = d.loc[d.n.idxmax()]

    fig, axes = plt.subplots(1, 2, figsize=(15.2, 7.0),
                             gridspec_kw={"width_ratios": [1.4, 1]})
    fig.patch.set_facecolor(BG)
    for ax in axes:
        ax.set_facecolor(BG)

    # ---- (a) each series against the ladder, with the HDI band behind it ----
    ax = axes[0]
    lo = min(abs(ref.get(f"r_{v}", np.nan)) for v, _ in COMPARATORS)
    hi = max(abs(ref.get(f"r_{v}", np.nan)) for v, _ in COMPARATORS)
    ax.axvspan(lo, hi, color=GREY, alpha=.16, zorder=0)
    ax.text((lo + hi) / 2, -0.92,
            f"HDI and its\ncomponents, same\n{int(ref.n)} countries\n|r| {lo:.2f}–{hi:.2f}",
            fontsize=7.8, color="#5A5A5A", ha="center", va="bottom", linespacing=1.45)

    y = np.arange(len(d))
    cols = [GREEN if q < .05 else GREY for q in d.q]
    ax.barh(y, d.absr, 0.55, color=cols, alpha=.85, zorder=2)
    for yi, row in d.iterrows():
        ax.text(row.absr + .012, yi, f"{row.r:+.2f}" + ("*" if row.q < .05 else ""),
                va="center", fontsize=8, color=INK, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{SHORT.get(c, c)}  (n={int(n)})"
                        for c, n in zip(d.SeriesCode, d.n)], fontsize=8.6)
    ax.set_ylim(-1.15, len(d) - 0.35)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("|correlation| with the Cantril ladder across countries", fontsize=9)
    ax.set_title("(a) Nine of the thirteen series can be tested across countries.\n"
                 "     Four are significant — and every one is weaker than the\n"
                 "     development indicators the frameworks already carry",
                 fontsize=10.5, fontweight="bold", color=INK, loc="left", pad=10)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="x", color="#E9E9E9", linewidth=0.8)
    ax.set_axisbelow(True)

    # ---- (b) net of income everything collapses, HDI included ----
    ax = axes[1]
    broad = d[d.n >= 70].sort_values("n", ascending=False)
    names = [TIGHT.get(c, c) for c in broad.SeriesCode]
    x = np.arange(len(names) + 1)
    raw = list(broad.absr) + [abs(ref.get("r_hdi", np.nan))]
    net = list(broad.partial_r.abs()) + [abs(ref.get("pr_hdi", np.nan))]
    labels = names + ["HDI\n(comparator)"]
    w = 0.36
    ax.bar(x - w / 2, raw, w, color=BLUE, alpha=.85, label="raw |r|")
    ax.bar(x + w / 2, net, w, color=ORANGE, alpha=.9, label="net of log GNI per capita")
    for xi, (a, b) in enumerate(zip(raw, net)):
        ax.text(xi - w / 2, a + .015, f"{a:.2f}", ha="center", fontsize=7.8, color=INK)
        ax.text(xi + w / 2, b + .015, f"{b:.2f}", ha="center", fontsize=7.8, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("|r| with the ladder", fontsize=9)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_title("(b) Income control separates nothing here — net of\n"
                 "     GNI per capita even the HDI collapses",
                 fontsize=10.5, fontweight="bold", color=INK, loc="left", pad=10)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="#E9E9E9", linewidth=0.8)
    ax.set_axisbelow(True)

    fig.suptitle("Testing the SDG framework's trust series the only way their coverage allows",
                 fontsize=14.5, fontweight="bold", color=INK, x=0.006, ha="left", y=0.985)
    fig.text(0.006, 0.940,
             "One observation per country, most recent year matched to the WHR ladder. "
             "* marks q<.05 after Benjamini–Hochberg across the nine testable series.",
             fontsize=8.8, color="#5A5A5A")
    fig.text(0.006, 0.014,
             "None of these series measures interpersonal trust; they measure satisfaction with "
             "public services and experience of bribery, and belong to institutional confidence. "
             "The broadest of them, satisfaction with healthcare, is\nGallup World Poll — the same "
             "survey that produces the ladder — so it is a same-instrument comparison, not "
             "independent corroboration. \"Decision-making is inclusive\" correlates negatively, a "
             "known artefact of\nsubjective institutional scales across very unequal income levels. "
             "Sources: UN SDG Global Database; World Happiness Report; UNDP Human Development Report.",
             fontsize=7.6, color=GREY, linespacing=1.5)
    fig.tight_layout(rect=(0, 0.072, 1, 0.925))
    out = "figures_out/K1_sdg_trust_cross_section.png"
    fig.savefig(out, dpi=200, facecolor=BG)
    print(f"Saved: {out}")


def main():
    res = cross_section(load_series(), load_outcome())
    res.to_csv("processed/sdg_trust_cross_section.csv", index=False)

    ok = res[~res.skipped].sort_values("r", ascending=False)
    print(f"{len(ok)} of 13 series have >= {MIN_COUNTRIES} countries with a "
          f"matched ladder value\n")
    cols = ["SeriesCode", "n", "median_year", "r", "q", "partial_r", "partial_q", "gallup"]
    print(ok[cols].to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print(f"\nsignificant raw (q<.05):     {(ok.q < .05).sum()} of {len(ok)}")
    print(f"significant net of income:   {(ok.partial_q < .05).sum()} of {len(ok)}")
    figure(res)


if __name__ == "__main__":
    main()
