"""
The within-country domain test with every predictor externally measured.

The ranking flip (health and trust over development, inside countries) was
originally shown with self-rated health and trust — reported by the same ESS
respondents as the outcome, so open to a shared-method objection. GDL's
regional sub-indices (healthindex, edindex, incindex, from the per-year
Subnational HDI exports) are external, which lets the domains compete within
countries with no method overlap with the outcome at all.

Inputs:
    raw/shdi_subindices.csv          (combined per-year GDL exports, long)
    processed/ess_with_shdi.csv      (respondents with crosswalked regions)

Outputs:
    processed/within_country_subindex_correlations.csv
    figures_out/H1_within_country_external_domains.png

Result (2010-2023 pooled, countries with >=6 matched regions):
    GDL health index   median r=+0.344, 6/15  (Albania excluded: its regional
                                               healthindex is constant)
    GDL income index   median r=+0.120, 2/16
    GDL education idx  median r=+0.057, 2/16
So the flip is specifically a health flip, and it does not depend on
self-report. Self-rated health still runs higher (+0.50), consistent with
part of its lead being shared method variance -- exactly as caveated.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from config import ESS_ISO2_TO_ISO3

MIN_REGIONS = 6

EXTERNAL = [("healthindex", "Health index"), ("incindex", "Income index"),
            ("edindex", "Education index")]
SELFREPORT = [("good_health", "Self-rated health"), ("ppltrst", "Social trust")]


def build_panel() -> pd.DataFrame:
    ess = pd.read_csv("processed/ess_with_shdi.csv", low_memory=False)
    ess["good_health"] = 6 - ess["health"]
    ess["iso3"] = ess["cntry"].map(ESS_ISO2_TO_ISO3)
    reg = (ess.dropna(subset=["gdl_region_name"])
              .groupby(["cntry", "iso3", "gdl_region_name"])
              .agg(stflife=("stflife", "mean"), good_health=("good_health", "mean"),
                   ppltrst=("ppltrst", "mean"), n=("stflife", "size"))
              .reset_index())

    si = pd.read_csv("raw/shdi_subindices.csv")
    si = si[si.level == "Subnat"]
    wide = (si.pivot_table(index=["iso3", "region_name"], columns="indicator",
                           values="value", aggfunc="mean").reset_index())
    m = reg.merge(wide, left_on=["iso3", "gdl_region_name"],
                  right_on=["iso3", "region_name"], how="inner")
    keep = m.groupby("cntry").size()
    return m[m.cntry.isin(keep[keep >= MIN_REGIONS].index)]


def correlate(m: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for var, label in EXTERNAL + SELFREPORT:
        for cntry, g in m.groupby("cntry"):
            g = g.dropna(subset=[var, "stflife"])
            # a constant predictor (GDL fills some countries' regions with the
            # national value) has no within-country information: skip, don't zero
            if len(g) < MIN_REGIONS or g[var].std() < 1e-9:
                continue
            r, p = stats.pearsonr(g[var], g["stflife"])
            rows.append({"predictor": var, "label": label, "cntry": cntry,
                         "r": r, "p": p, "n_regions": len(g)})
    return pd.DataFrame(rows)


def main():
    m = build_panel()
    res = correlate(m)
    res.to_csv("processed/within_country_subindex_correlations.csv", index=False)

    summ = (res.groupby(["predictor", "label"])
               .agg(median_r=("r", "median"), sig=("p", lambda s: (s < .05).sum()),
                    n=("r", "size")).reset_index())
    print(summ.sort_values("median_r", ascending=False).to_string(index=False))

    # ---- figure ----
    BLUE, ORANGE, RED, GREEN = "#2A78D6", "#EDA100", "#E34948", "#1BAF7A"
    GREY, BG, INK = "#8A8A8A", "#FCFCFB", "#1A1A1A"
    order = [("healthindex", RED, 0.95), ("incindex", ORANGE, 0.95),
             ("edindex", BLUE, 0.95), ("good_health", RED, 0.40),
             ("ppltrst", GREEN, 0.40)]
    fig, ax = plt.subplots(figsize=(11, 5.6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    y = np.arange(len(order))[::-1]
    for yi, (var, col, alpha) in zip(y, order):
        row = summ[summ.predictor == var].iloc[0]
        ax.barh(yi, row.median_r, 0.58, color=col, alpha=alpha)
        ax.text(row.median_r + 0.012, yi,
                f"{row.median_r:+.3f}   ({int(row.sig)}/{int(row.n)} countries sig.)",
                va="center", fontsize=9.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([
        "GDL health index\n(external)", "GDL income index\n(external)",
        "GDL education index\n(external)", "Self-rated health\n(same-survey)",
        "Social trust\n(same-survey)"], fontsize=9)
    ax.set_xlim(0, 0.75)
    ax.set_xlabel("Median within-country regional correlation with life satisfaction", fontsize=9.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="x", color="#E6E6E6", linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.set_axisbelow(True)
    ax.set_title("The within-country flip survives external measurement — and it is a health flip",
                 fontsize=12.5, fontweight="bold", color=INK, loc="left", pad=30)
    ax.text(0, 1.02,
            "GDL regional sub-indices share no method with the ESS outcome. Health leads "
            "income and education among the external\nmeasures; self-rated health runs higher "
            "still, consistent with part of its lead being shared method variance.",
            transform=ax.transAxes, fontsize=8.7, color="#5A5A5A", va="bottom")
    fig.text(0.008, 0.02,
             "16 ESS countries with ≥6 crosswalked regions, sub-indices pooled 2010–2023. Albania excluded "
             "from the health row\n(constant regional healthindex). Sources: Global Data Lab; European "
             "Social Survey rounds 5–11.",
             fontsize=7.5, color=GREY, linespacing=1.5)
    fig.tight_layout(rect=(0, 0.07, 1, 0.98))
    fig.savefig("figures_out/H1_within_country_external_domains.png", dpi=200, facecolor=BG)
    print("Saved: figures_out/H1_within_country_external_domains.png")


if __name__ == "__main__":
    main()
