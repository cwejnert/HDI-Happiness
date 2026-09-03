"""
Three specifications, one set of domains -- and the ranking changes twice.

The deck reports three different tests and has been letting the reader join
them up unaided:

    (a) BETWEEN COUNTRIES, IN LEVELS      is a country with more of X happier?
    (b) BETWEEN COUNTRIES, IN CHANGES     when a country gains X, does it get
                                          happier? -- the collapse
    (c) WITHIN ONE COUNTRY, ACROSS ITS    are the regions with more of X the
        REGIONS                           happier regions?

They are not three attempts at the same question. (a) is dominated by the
development gradient, where schooling and income proxy the whole bundle at
once. (b) removes every fixed national difference and almost nothing survives.
(c) holds the country -- its institutions, its history, its national policy --
fixed, and asks what still separates a good place to live from a worse one
inside it.

The ranking is different in each, and in a consistent direction: what predicts
*where* wellbeing is high is structural (schooling, income); what predicts
where it is high *inside a country* is experiential (health, trust). Education
leads (a) and is near-zero in (c); health and trust are near-zero or unmeasured
in (a) and lead (c).

Panels (a) and (b) use the same instrument on the same countries, so the
collapse between them is exact. Panel (c) is a different instrument at a
different scale and is marked as such; within it, externally measured
predictors are drawn solid and same-survey self-reports hatched, because the
shared-method objection applies only to the latter.

Inputs:  raw/HDI_indicator_summary.csv
         processed/ess_with_shdi.csv
         processed/within_country_mechanism_correlations.csv
         processed/within_country_subindex_correlations.csv
Outputs: processed/specification_synthesis.csv
         figures_out/L1_three_specifications.png
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from scipy import stats

MIN_REGIONS = 6

BG, INK, GREY = "#FCFCFB", "#1A1A1A", "#8A8A8A"
C_EDU = "#2A78D6"
C_HEALTH = "#E34948"
C_TRUST = "#1BAF7A"
C_DEV = "#8A8A8A"

DOMAINS = [("Education", C_EDU), ("Health", C_HEALTH),
           ("Social trust", C_TRUST), ("Development", C_DEV)]


def pooled_regional_education() -> tuple[float, int, int]:
    """Education across regions, pooling respondents rather than round means.

    G3 in make_figures.py builds region values as the unweighted mean of that
    region's per-round means; this pools respondents directly, so regions are
    weighted by sample size. For health, trust and development the choice moves
    the median a little. For education it moves it across zero -- +0.13 pooled
    against -0.08 from round means -- because education is the one domain whose
    within-country correlations are not consistently signed to begin with:
    eight of sixteen countries positive, and the significant ones point both
    ways. main() prints both so the instability is on the record rather than
    hidden behind whichever number a figure happens to use.
    """
    ess = pd.read_csv("processed/ess_with_shdi.csv", low_memory=False)
    reg = (ess.dropna(subset=["gdl_region_name"])
              .groupby(["cntry", "gdl_region_name"])
              .agg(stflife=("stflife", "mean"), eduyrs=("eduyrs", "mean"))
              .reset_index().dropna())
    rs = []
    for cntry, g in reg.groupby("cntry"):
        if len(g) < MIN_REGIONS:
            continue
        r, p = stats.pearsonr(g["eduyrs"], g["stflife"])
        rs.append((r, p))
    r = np.array([x[0] for x in rs])
    p = np.array([x[1] for x in rs])
    return float(np.median(r)), int((p < .05).sum()), len(r)


def collect() -> pd.DataFrame:
    hdi = pd.read_csv("raw/HDI_indicator_summary.csv").set_index("indicatorCode")
    mech = pd.read_csv("processed/within_country_mechanism_correlations.csv")
    sub = pd.read_csv("processed/within_country_subindex_correlations.csv")

    def hdi_row(code):
        r = hdi.loc[code]
        return (100 * r.n_sig_levels_fdr / r.n_countries,
                100 * r.n_sig_diffs_fdr / r.n_countries,
                int(r.n_sig_levels_fdr), int(r.n_sig_diffs_fdr), int(r.n_countries))

    def med(df, pred):
        """Median, count significant, and count positive -- the last because
        for education the median is not a fair summary on its own."""
        g = df[df.predictor == pred]
        return (float(g.r.median()), int((g.p < .05).sum()), len(g),
                int((g.r > 0).sum()))

    rows = []
    for domain, hdi_code, self_pred, ext_pred in [
            ("Education", "mys", "eduyrs", "edindex"),
            ("Health", "le", "good_health", "healthindex"),
            ("Social trust", None, "ppltrst", None),
            ("Development", "hdi", "shdi", "incindex")]:
        rec = {"domain": domain}
        if hdi_code:
            (rec["levels_pct"], rec["diffs_pct"], rec["levels_n"],
             rec["diffs_n"], rec["n_countries"]) = hdi_row(hdi_code)
            rec["hdi_indicator"] = hdi_code
        # every self-report cell now comes from G3's mechanism file, so panel
        # (c) is one aggregation throughout rather than a mix of two
        if self_pred:
            (rec["self_r"], rec["self_sig"], rec["self_n"],
             rec["self_pos"]) = med(mech, self_pred)
            rec["self_pred"] = self_pred
        if ext_pred:
            (rec["ext_r"], rec["ext_sig"], rec["ext_n"],
             rec["ext_pos"]) = med(sub, ext_pred)
            rec["ext_pred"] = ext_pred
        rows.append(rec)
    return pd.DataFrame(rows).set_index("domain").loc[[d for d, _ in DOMAINS]].reset_index()


def figure(d: pd.DataFrame):
    fig, axes = plt.subplots(1, 3, figsize=(15.6, 6.6))
    fig.patch.set_facecolor(BG)
    for ax in axes:
        ax.set_facecolor(BG)

    y = np.arange(len(DOMAINS))[::-1]
    colors = [c for _, c in DOMAINS]
    labels = [n for n, _ in DOMAINS]

    def frame(ax, title, sub, xlabel, xmax):
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=10)
        ax.set_xlim(0, xmax)
        ax.set_xlabel(xlabel, fontsize=8.8)
        ax.set_title(title, fontsize=11, fontweight="bold", color=INK, loc="left", pad=34)
        ax.text(0, 1.012, sub, transform=ax.transAxes, fontsize=8.2,
                color="#5A5A5A", va="bottom", linespacing=1.4)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.grid(axis="x", color="#EAEAEA", linewidth=0.8)
        ax.set_axisbelow(True)

    def unmeasured(ax, yi, xmax):
        ax.text(xmax * 0.035, yi, "not measured by the HDI", fontsize=8.4,
                color=GREY, style="italic", va="center")

    # ---- (a) between countries, levels ----
    ax = axes[0]
    for yi, (_, row), col in zip(y, d.iterrows(), colors):
        if pd.isna(row.get("levels_pct")):
            unmeasured(ax, yi, 55)
            continue
        ax.barh(yi, row.levels_pct, 0.6, color=col, alpha=.88)
        ax.text(row.levels_pct + 0.8, yi,
                f"{row.levels_pct:.1f}%  ({int(row.levels_n)}/{int(row.n_countries)})",
                va="center", fontsize=8.6, color=INK)
    frame(ax, "(a) Between countries, in levels",
          "Is a country with more of this happier?\nHDI components, "
          "% of countries FDR-significant", "% of countries significant", 55)

    # ---- (b) between countries, differences ----
    ax = axes[1]
    for yi, (_, row), col in zip(y, d.iterrows(), colors):
        if pd.isna(row.get("diffs_pct")):
            unmeasured(ax, yi, 55)
            continue
        ax.barh(yi, row.diffs_pct, 0.6, color=col, alpha=.88)
        ax.text(row.diffs_pct + 0.8, yi,
                f"{row.diffs_pct:.1f}%  ({int(row.diffs_n)}/{int(row.n_countries)})",
                va="center", fontsize=8.6, color=INK)
    frame(ax, "(b) The same countries, in year-to-year changes",
          "When a country gains it, does it get happier?\nSame instrument, "
          "same countries — this is the collapse", "% of countries significant", 55)

    # ---- (c) within countries, across regions ----
    # education's median is negative here, so this panel needs a signed axis
    # and a zero line; the "n positive of 16" is printed with each bar because
    # a median near zero can mean consistently tiny or wildly inconsistent, and
    # for education it is the second
    ax = axes[2]
    for yi, (_, row), col in zip(y, d.iterrows(), colors):
        for off, rk, sk, nk, pk, alpha, hatch in (
                (0.17, "ext_r", "ext_sig", "ext_n", "ext_pos", .9, None),
                (-0.17, "self_r", "self_sig", "self_n", "self_pos", .45, "///")):
            if pd.isna(row.get(rk)):
                continue
            v = row[rk]
            ax.barh(yi + off, v, 0.32, color=col, alpha=alpha, hatch=hatch,
                    edgecolor=col, linewidth=0)
            ax.text(v + (.012 if v >= 0 else -.012), yi + off,
                    f"{v:+.2f}  {int(row[sk])} sig., {int(row[pk])}+ of {int(row[nk])}",
                    va="center", ha="left" if v >= 0 else "right",
                    fontsize=7.6, color=INK)
    frame(ax, "(c) Inside one country, across its regions",
          "Are the regions with more of it the happier regions?\nESS regions, "
          "median within-country correlation", "median regional r", 0.92)
    ax.set_xlim(-0.30, 0.92)
    ax.axvline(0, color=INK, linewidth=0.9)
    ax.legend(handles=[Patch(facecolor=GREY, alpha=.9, label="externally measured"),
                       Patch(facecolor=GREY, alpha=.45, hatch="///", label="self-reported")],
              loc="upper center", bbox_to_anchor=(0.5, -0.135), ncol=2,
              frameon=False, fontsize=8.4)

    fig.suptitle("The same domains, three specifications — and the ranking changes twice",
                 fontsize=15, fontweight="bold", color=INK, x=0.005, ha="left", y=0.985)
    fig.text(0.005, 0.905,
             "Education leads between countries and has no consistent signal inside them. Health and "
             "social trust do the reverse. Nothing survives the move to year-to-year change. The "
             "three panels are three different questions, and the\ndirection of the shift is the "
             "finding: what predicts WHERE wellbeing is high is structural, what predicts where it "
             "is high INSIDE a country is experiential.",
             fontsize=9, color="#5A5A5A", va="top", linespacing=1.5)
    fig.text(0.005, 0.012,
             "Panels (a) and (b) are the same HDI indicators on the same 150–151 countries against WHR happiness, "
             "so the collapse between them is exact; education is mean years of schooling, health is life\n"
             "expectancy, development the HDI composite. Panel (c) is a different instrument at a different scale "
             "— 16 ESS countries with ≥6 matched regions — so it is read alongside (a) and (b), not\nsubtracted "
             "from them. The count of countries with a POSITIVE correlation is given because a median near zero "
             "can mean consistently tiny or wildly inconsistent: health and trust are 12 and 14 of 16\npositive, "
             "education 8 of 16 with its significant countries pointing both ways. Sources: UNDP HDR; World "
             "Happiness Report; Global Data Lab; European Social Survey rounds 5–11.",
             fontsize=7.6, color=GREY, va="bottom", linespacing=1.5)
    fig.tight_layout(rect=(0, 0.105, 1, 0.865), w_pad=3.0)
    out = "figures_out/L1_three_specifications.png"
    fig.savefig(out, dpi=200, facecolor=BG)
    print(f"Saved: {out}")


def main():
    d = collect()
    d.to_csv("processed/specification_synthesis.csv", index=False)
    cols = [c for c in ["domain", "hdi_indicator", "levels_pct", "diffs_pct",
                        "ext_pred", "ext_r", "ext_sig", "ext_pos", "self_pred",
                        "self_r", "self_sig", "self_pos"] if c in d]
    print(d[cols].to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    # the aggregation education is sensitive to, printed rather than buried
    pooled_r, pooled_sig, pooled_n = pooled_regional_education()
    g3_r = float(d.loc[d.domain == "Education", "self_r"].iloc[0])
    print(f"\nEducation within countries is aggregation-sensitive: "
          f"{g3_r:+.3f} from round means (used in the figure) against "
          f"{pooled_r:+.3f} pooling respondents ({pooled_sig} of {pooled_n} sig.). "
          f"Both are near zero and the sign is not stable -- report it that way.")
    figure(d)


if __name__ == "__main__":
    main()
