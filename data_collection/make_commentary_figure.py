"""
Composite Figure 1 for the commentary submission.

Commentaries allow one or two display items, so the three results that carry
the argument have to share a single figure:

    (a) the levels-to-differences collapse, replicated on the HDI against the
        World Happiness Report;
    (b) SDG4 un-pooled, showing that its apparent weakness is a construct
        artifact of pooling equity/parity ratios with access measures;
    (c) education's signal as the unit of measurement changes, from pooled
        SDG indicators down to individual ESS respondents.

Unlike make_figures.py, this script does not read the microdata. Every number
below is a result already produced by that pipeline (see PROVENANCE), so the
figure can be rebuilt for a revision without re-running the merges. If any
upstream number changes, change it here too -- these are transcriptions, not
computations.

    python make_commentary_figure.py [outdir]

Output: <outdir>/Figure1_commentary.png (+ .pdf for submission)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# --------------------------------------------------------------------------
# Palette: matches the figures already produced by make_figures.py.
# --------------------------------------------------------------------------
BLUE = "#2A78D6"
ORANGE = "#EDA100"
GREEN = "#1BAF7A"
PURPLE = "#4A3AA7"
VERMILION = "#EB6834"
RED = "#E34948"
GREY = "#8A8A8A"
BG = "#FCFCFB"
INK = "#1A1A1A"

PROVENANCE = """Panel a, SDG: robust_all_for_figures.csv, countries with >=1 FDR-significant
series (42 countries carry SDG coverage; median 456 series each).
Panel a, HDI: HDI_indicator_summary.csv, the `hdi` composite row (HappinessHDI.R);
independently reproduced here to 63/150 -> 3/150.
Panel a: GDL's national SHDI is deliberately absent -- it reproduces the UNDP
HDI exactly (1,696/1,696 country-years identical), being derived from it, so it
cannot serve as an independent replication.
Panel b: SDG4's 35 series classified by construct (make_figures.py section F).
Panel c: as above plus ESS individual-level tests. Denominators differ by row."""

# --------------------------------------------------------------------------
# (a) The collapse: countries FDR-significant in levels vs. first-differences
# --------------------------------------------------------------------------
# NB the Global Data Lab's SHDI at NATIONAL level is numerically identical to
# the UNDP HDI -- all 1,696 overlapping country-years match to 0.000 -- so it
# is not an independent replication and is deliberately not shown here. GDL's
# subnational values are genuine and carry the regional analysis instead.
COLLAPSE = [
    # label,                  n_sig_levels, n_sig_diffs, n_countries
    ("SDG indicators\n(any of ~456 series)", 30, 2, 42),
    ("Human Development\nIndex (composite)", 64, 3, 151),
]

# --------------------------------------------------------------------------
# (b) SDG4 un-pooled by construct: % of country-indicator pairs significant
# --------------------------------------------------------------------------
SDG4_POOLED_PCT = 3.3
SDG4_BY_CONSTRUCT = [
    ("Access & participation", 12.7, 2, BLUE),
    ("Financing", 11.5, 1, ORANGE),
    ("Attainment & completion", 3.8, 1, GREEN),
    ("Equity / parity ratios", 2.5, 18, PURPLE),
    ("Infrastructure & inputs", 2.0, 7, VERMILION),
    ("Quality & learning", 0.9, 6, RED),
]

# --------------------------------------------------------------------------
# (c) Education as the unit of measurement changes
# --------------------------------------------------------------------------
EDU_LADDER = [
    # label,                            denominator note,               pct,  colour
    ("SDG4, all 35 indicators pooled", "of country × indicator pairs", 3.3, GREY),
    ("SDG4, access indicators only", "of country × indicator pairs", 12.7, VERMILION),
    ("HDI expected years of schooling", "of 150 countries", 34.0, BLUE),
    ("HDI mean years of schooling", "of 150 countries", 40.7, BLUE),
    ("ESS respondents' own attainment", "of 36 countries (32 of 36)", 88.9, GREEN),
]


def style_axes(ax):
    ax.set_facecolor(BG)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#CFCFCF")
    ax.tick_params(colors="#555555", labelsize=9)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)


def panel_a(ax):
    labels = [c[0] for c in COLLAPSE]
    lev = [100 * c[1] / c[3] for c in COLLAPSE]
    dif = [100 * c[2] / c[3] for c in COLLAPSE]
    x = range(len(COLLAPSE))
    w = 0.36

    ax.bar([i - w / 2 for i in x], lev, w, color=BLUE, label="Levels")
    ax.bar([i + w / 2 for i in x], dif, w, color=RED, label="First differences")

    for i, (lv, dv, c) in enumerate(zip(lev, dif, COLLAPSE)):
        ax.text(i - w / 2, lv + 1.2, f"{lv:.0f}%", ha="center", fontsize=9,
                color=INK, fontweight="bold")
        ax.text(i - w / 2, lv + 4.4, f"{c[1]}/{c[3]}", ha="center", fontsize=7.5, color=GREY)
        ax.text(i + w / 2, dv + 1.2, f"{dv:.0f}%", ha="center", fontsize=9,
                color=INK, fontweight="bold")
        ax.text(i + w / 2, dv + 4.4, f"{c[2]}/{c[3]}", ha="center", fontsize=7.5, color=GREY)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylim(0, 88)
    ax.set_ylabel("% of countries with a significant\ndevelopment–happiness association", fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, loc="upper center", ncol=2,
              bbox_to_anchor=(0.5, 1.02))
    style_axes(ax)
    ax.set_title("a  The collapse is not an artifact of the SDG framework",
                 fontsize=10.5, fontweight="bold", color=INK, loc="left", pad=34)
    ax.text(0, 1.012,
            "One outcome (WHR Cantril ladder). The SDG test asks whether ANY of a country's\n"
            "series is significant, so its levels rate is higher by construction — "
            "the collapse ratio is what compares.\n"
            "Also replicates against a second wellbeing survey and at regional scale (Act I).",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")


# --------------------------------------------------------------------------
# (b) The inversion: which of health / education dominates, by instrument.
# Bars are each instrument's own metric, normalised to the pair so the
# ORDERING is readable across instruments; raw values are annotated.
# --------------------------------------------------------------------------
INVERSION = [
    # instrument,                    health, education, metric note
    ("HDI\n(vs WHR happiness)", 19.9, 40.7, "% of countries significant\nhealth = life expectancy"),
    ("SDG data\n(high-income only)", 11.2, 1.2, "% of country × indicator pairs\nhealth = SDG3 series"),
    ("ESS\n(individual respondents)", 0.0910, 0.0098, "median within-country R²\nhealth = self-rated"),
]

# --------------------------------------------------------------------------
# (c) The method check: administrative vs self-report, three domains.
# --------------------------------------------------------------------------
METHOD = [
    ("Health", 11.5, 0.513, RED),
    ("Education", 3.3, -0.078, BLUE),
    ("Social trust", 1.5, 0.487, GREEN),
]


def panel_b(ax):
    x = range(len(INVERSION))
    for i, (label, h, e, note) in enumerate(INVERSION):
        tot = h + e
        hs, es = 100 * h / tot, 100 * e / tot
        ax.bar(i, hs, 0.55, color=RED)
        ax.bar(i, es, 0.55, bottom=hs, color=BLUE)
        ax.text(i, hs / 2, f"health\n{h:g}", ha="center", va="center",
                fontsize=8.5, color="white", fontweight="bold")
        ax.text(i, hs + es / 2, f"education\n{e:g}", ha="center", va="center",
                fontsize=8.5, color="white", fontweight="bold")
        ax.text(i, 103, note, ha="center", va="bottom", fontsize=7, color=GREY)

    ax.set_xticks(list(x))
    ax.set_xticklabels([r[0] for r in INVERSION], fontsize=8.5)
    ax.set_ylim(0, 118)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("Share of the health + education pair (%)", fontsize=9)
    style_axes(ax)
    ax.set_title("b  The ranking inverts with the instrument",
                 fontsize=10.5, fontweight="bold", color=INK, loc="left", pad=34)
    ax.text(0, 1.012,
            "Each instrument uses its own metric (noted above each bar), so only the\n"
            "ordering compares. Education leads under the HDI; health leads by an order of\n"
            "magnitude in both sources that measure it somewhere it still varies.",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")


def panel_c(ax):
    # Each source is normalised to its own leading domain, so the two very
    # different metrics can sit on one axis without implying comparability.
    sdg_max = max(m[1] for m in METHOD)
    ess_max = max(m[2] for m in METHOD)
    y = list(range(len(METHOD)))[::-1]
    w = 0.36

    for yi, m in zip(y, METHOD):
        a, b = m[1] / sdg_max, m[2] / ess_max
        ax.barh(yi + w / 2, a, w, color=m[3], alpha=0.95)
        ax.barh(yi - w / 2, b, w, color=m[3], alpha=0.40)
        ax.text(a + 0.015, yi + w / 2, f"{m[1]}%", va="center", fontsize=8.5, color=INK)
        ax.text(b + (0.015 if b >= 0 else -0.015), yi - w / 2, f"{m[2]:+.3f}",
                va="center", ha="left" if b >= 0 else "right", fontsize=8.5, color=INK)

    # empty barh containers render with the axes' colour cycle rather than the
    # colour asked for, so build the legend from explicit patches
    ax.legend(handles=[
        Patch(facecolor="#6E6E6E", alpha=0.95, label="UN SDG database (administrative)"),
        Patch(facecolor="#6E6E6E", alpha=0.40, label="European Social Survey (self-reported)")],
        frameon=False, fontsize=8.5, loc="upper right", bbox_to_anchor=(1.0, 0.62))
    ax.set_yticks(y)
    ax.set_yticklabels([m[0] for m in METHOD], fontsize=9.5)
    ax.set_xlim(-0.30, 1.22)
    ax.axvline(0, color=INK, linewidth=0.9)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(["0", "half the leader", "leading domain"], fontsize=8)
    ax.set_xlabel("Position relative to the leading domain within each source", fontsize=9)
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color="#E6E6E6", linewidth=0.8)
    ax.set_title("c  Only health leads in both an administrative and a self-report source",
                 fontsize=10.5, fontweight="bold", color=INK, loc="left", pad=34)
    ax.text(0, 1.012,
            "Labels give the raw values: % of SDG country × indicator pairs significant, "
            "and median within-country\nregional correlation in the ESS. Trust tops the "
            "self-report source and sits near the bottom of the administrative one. Education "
            "is weak\nin both, and inside countries its correlations are not even consistently "
            "signed — positive in 8 of 16.",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")


def main():
    outdir = Path(sys.argv[1] if len(sys.argv) > 1 else "figures_out")
    outdir.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(12.6, 9.2))
    fig.patch.set_facecolor(BG)
    # Two gridspecs rather than one: panel c's row labels need a much wider
    # left margin than a and b do.
    gs_top = fig.add_gridspec(1, 2, left=0.085, right=0.985, top=0.855,
                              bottom=0.575, wspace=0.30)
    gs_bot = fig.add_gridspec(1, 1, left=0.135, right=0.985, top=0.355, bottom=0.105)
    panel_a(fig.add_subplot(gs_top[0, 0]))
    panel_b(fig.add_subplot(gs_top[0, 1]))
    panel_c(fig.add_subplot(gs_bot[0, 0]))

    fig.text(0.008, 0.975,
             "Development, wellbeing, and the measurement problem",
             fontsize=16, fontweight="bold", color=INK, va="top")
    fig.text(0.008, 0.940,
             "Significance is Benjamini–Hochberg FDR-corrected within country.",
             fontsize=9, color="#5A5A5A", va="top")
    fig.text(0.008, 0.018,
             "Sources: UN SDG Global Database; UNDP Human Development Report; "
             "Global Data Lab Subnational HDI; European Social Survey rounds 5–11 "
             "(2010–2023); World Happiness Report.",
             fontsize=8, color=GREY, va="bottom")
    for ext in ("png", "pdf"):
        path = outdir / f"Figure1_commentary.{ext}"
        fig.savefig(path, dpi=220, facecolor=BG)
        print(f"Saved: {path}")
    plt.close(fig)
    build_c2(outdir)
    build_hdi_structure(outdir)
    build_horse_race(outdir)
    build_corroboration(outdir)




# ==========================================================================
# Replacement for the pipeline's C2 figure.
#
# Also drops the GDL SHDI bar: at national level GDL reports the UNDP HDI
# verbatim (verified, 1,696/1,696 country-years identical), so showing it
# beside the HDI implied an independent replication that does not exist.
#
# The original C2 reported the HDI composite as 67/150 -> 6/150. That does not
# reproduce: HappinessHDI.R's own HDI_indicator_summary.csv gives 64/151 -> 3/151
# for the `hdi` row, and an independent recomputation from HDI_with_happiness.csv
# gives 63/150 -> 3/150. The SHDI side (66/148 -> 6/148) does reproduce and is
# unchanged. This rebuilds the figure on the authoritative numbers.
# ==========================================================================
C2 = [
    ("SDG indicators\n(any of a country's series)", 30, 2, 42),
    ("UNDP HDI\n(composite)", 64, 3, 151),
]


def build_c2(outdir: Path):
    fig, ax = plt.subplots(figsize=(11, 6.2))
    fig.patch.set_facecolor(BG)
    lev = [100 * c[1] / c[3] for c in C2]
    dif = [100 * c[2] / c[3] for c in C2]
    x, w = range(len(C2)), 0.32

    ax.bar([i - w / 2 for i in x], lev, w, color=BLUE, label="Levels")
    ax.bar([i + w / 2 for i in x], dif, w, color=RED, label="Year-to-year differences")
    for i, (lv, dv, c) in enumerate(zip(lev, dif, C2)):
        ax.text(i - w / 2, lv + 1.0, f"{c[1]}/{c[3]}", ha="center", fontsize=10, color=INK)
        ax.text(i + w / 2, dv + 1.0, f"{c[2]}/{c[3]}", ha="center", fontsize=10, color=INK)

    ax.set_xticks(list(x))
    ax.set_xticklabels([c[0] for c in C2], fontsize=10)
    ax.set_ylim(0, 60)
    ax.set_ylabel("% of countries FDR-significant (q<.05) vs. WHR happiness", fontsize=9.5)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    style_axes(ax)
    ax.set_title("The collapse replicates outside the SDG framework",
                 fontsize=13, fontweight="bold", color=INK, loc="left", pad=38)
    ax.text(0, 1.015,
            "Benjamini–Hochberg corrected within country. The SDG bar asks whether any of a "
            "country's series is\nsignificant and the HDI bar asks about one composite, so the "
            "levels rates are not directly comparable;\nthe order-of-magnitude collapse in both is.",
            transform=ax.transAxes, fontsize=9, color="#5A5A5A", va="bottom")
    fig.text(0.008, 0.02,
             "Sources: UN SDG Global Database (HappinessSDG.R); UNDP HDR "
             "(HDI_indicator_summary.csv, HappinessHDI.R); World Happiness Report. "
             "GDL's national SHDI is omitted: it is numerically identical to the UNDP HDI.",
             fontsize=8, color=GREY)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    path = outdir / "collapse_hdi_shdi_whr.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close(fig)
    print(f"Saved: {path}")

# ==========================================================================
# The HDI's full structure: composite + 4 sub-components, both specifications.
#
# HappinessHDI.R reports all five indicators in levels AND first differences;
# the acts were carrying the composite in one place and the sub-components'
# levels in another, which loses the two results below.
#
# Transcribed from HDI_indicator_summary.csv (reproduced independently from
# HDI_with_happiness.csv to within one country on every row).
# ==========================================================================
HDI_STRUCTURE = [
    # label,                    n,   sig_lev, sig_dif, r2_lev, r2_dif, is_education
    ("HDI\n(composite)",         151, 64, 3, 0.322, 0.063, False),
    ("Mean years\nof schooling", 150, 61, 2, 0.326, 0.069, True),
    ("Expected years\nof schooling", 150, 51, 7, 0.269, 0.056, True),
    ("GNI\nper capita",          151, 61, 2, 0.318, 0.051, False),
    ("Life\nexpectancy",         151, 30, 4, 0.160, 0.056, False),
]


def build_hdi_structure(outdir: Path):
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.8))
    fig.patch.set_facecolor(BG)
    x, w = range(len(HDI_STRUCTURE)), 0.36
    labels = [r[0] for r in HDI_STRUCTURE]

    # (a) share of countries significant
    ax = axes[0]
    lev = [100 * r[2] / r[1] for r in HDI_STRUCTURE]
    dif = [100 * r[3] / r[1] for r in HDI_STRUCTURE]
    ax.bar([i - w / 2 for i in x], lev, w, color=BLUE, label="Levels")
    ax.bar([i + w / 2 for i in x], dif, w, color=RED, label="First differences")
    for i, r in enumerate(HDI_STRUCTURE):
        ax.text(i - w / 2, lev[i] + 0.9, f"{r[2]}", ha="center", fontsize=8.5, color=INK)
        ax.text(i + w / 2, dif[i] + 0.9, f"{r[3]}", ha="center", fontsize=8.5, color=INK)
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 52)
    ax.set_ylabel("% of countries FDR-significant", fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    style_axes(ax)
    ax.set_title("a  Countries significant, by indicator", fontsize=10.5,
                 fontweight="bold", color=INK, loc="left", pad=24)
    ax.text(0, 1.012, "Bar labels are country counts. Expected years of schooling "
                      "leads in differences (7).",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")

    # (b) median R-squared
    ax = axes[1]
    rl = [r[4] for r in HDI_STRUCTURE]
    rd = [r[5] for r in HDI_STRUCTURE]
    ax.bar([i - w / 2 for i in x], rl, w, color=BLUE)
    ax.bar([i + w / 2 for i in x], rd, w, color=RED)
    for i in x:
        ax.text(i - w / 2, rl[i] + .008, f"{rl[i]:.3f}", ha="center", fontsize=8, color=INK)
        ax.text(i + w / 2, rd[i] + .008, f"{rd[i]:.3f}", ha="center", fontsize=8, color=INK)
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 0.40)
    ax.set_ylabel("Median R² across countries", fontsize=9)
    style_axes(ax)
    ax.set_title("b  Median explanatory power, by indicator", fontsize=10.5,
                 fontweight="bold", color=INK, loc="left", pad=24)
    ax.text(0, 1.012, "Mean years of schooling is the highest of the five in both "
                      "specifications — above the composite.",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")

    # mark the education pair on both panels
    for ax in axes:
        ax.axvspan(0.55, 2.45, color=GREEN, alpha=0.07, zorder=0)
        ax.text(1.5, ax.get_ylim()[1] * 0.955, "education", ha="center",
                fontsize=8, color="#0E7A55", style="italic")

    fig.text(0.007, 0.972, "The HDI in full: composite and sub-components, both specifications",
             fontsize=13.5, fontweight="bold", color=INK, va="top")
    fig.text(0.007, 0.022,
             "Source: HDI_indicator_summary.csv (HappinessHDI.R); World Happiness Report. "
             "Benjamini–Hochberg corrected across the five indicators within each country.",
             fontsize=8, color=GREY, va="bottom")
    fig.tight_layout(rect=(0, 0.05, 1, 0.925))
    path = outdir / "hdi_full_structure.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close(fig)
    print(f"Saved: {path}")


# ==========================================================================
# The domain horse race: what actually predicts life satisfaction, at three
# levels of aggregation, using one instrument (ESS) so the comparison is fair.
#
# Computed from processed/ess_with_national_hdi.csv and ess_with_shdi.csv.
# ==========================================================================
HORSE = {
    # level: [(label, value, n_sig, n_tot, colour)]
    "individual": [
        ("Self-rated health", 0.0910, 36, 36, RED),
        ("Household income", 0.0434, 36, 36, ORANGE),
        ("Social trust", 0.0407, 34, 36, GREEN),
        ("Education (ISCED)", 0.0098, 33, 36, BLUE),
        ("Education (years)", 0.0075, 32, 36, BLUE),
    ],
    "country": [
        ("HDI composite", 0.760, None, 35, PURPLE),
        ("Social trust", 0.676, None, 36, GREEN),
        ("Self-rated health", 0.423, None, 36, RED),
        ("Household income", 0.379, None, 36, ORANGE),
        ("Education (years)", 0.292, None, 36, BLUE),
    ],
    "within": [
        ("Social trust", 0.565, 8, 16, GREEN),
        ("Self-rated health", 0.502, 7, 16, RED),
        ("Household income", 0.230, 2, 16, ORANGE),
        ("Development (SHDI)", 0.219, 3, 16, PURPLE),
        ("Education (years)", -0.078, 3, 16, BLUE),
    ],
}
PANELS = [
    ("individual", "a  Individual respondents",
     "Median within-country R², own attribute vs own life satisfaction",
     "Median R² across 36 countries", 0.10),
    ("country", "b  Across countries",
     "Country means, 36 ESS countries", "R² across countries", 0.85),
    ("within", "c  Within countries, across regions",
     "Median regional correlation, 16 countries",
     "Median r within country", 0.65),
]


def build_horse_race(outdir: Path):
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 6.2))
    fig.patch.set_facecolor(BG)
    for ax, (key, title, sub, xlab, xmax) in zip(axes, PANELS):
        rows = HORSE[key]
        y = list(range(len(rows)))[::-1]
        ax.barh(y, [r[1] for r in rows], 0.6, color=[r[4] for r in rows])
        for yi, r in zip(y, rows):
            txt = f"{r[1]:.3f}" if key != "individual" else f"{r[1]:.4f}"
            if r[2] is not None:
                txt += f"   ({r[2]}/{r[3]} sig.)"
            ax.text(r[1] + xmax * 0.02, yi, txt, va="center", fontsize=8.5, color=INK)
        ax.set_yticks(y)
        ax.set_yticklabels([r[0] for r in rows], fontsize=9)
        ax.set_xlim(0, xmax)
        ax.set_xlabel(xlab, fontsize=8.5)
        style_axes(ax)
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", color="#E6E6E6", linewidth=0.8)
        ax.set_title(title, fontsize=11, fontweight="bold", color=INK, loc="left", pad=26)
        ax.text(0, 1.015, sub, transform=ax.transAxes, fontsize=8.2,
                color="#5A5A5A", va="bottom")

    fig.text(0.006, 0.972,
             "What actually predicts life satisfaction? Health and social trust — not schooling",
             fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.006, 0.930,
             "One instrument (European Social Survey, 36 countries, 351,023 respondents, "
             "2010–2023) at three levels of aggregation, so the domains compete on equal terms.",
             fontsize=9, color="#5A5A5A", va="top")
    fig.text(0.006, 0.030,
             "Self-rated health reversed so higher = better. Education is significant almost "
             "everywhere but carries the smallest effect of any domain tested; the HDI leads "
             "between countries, where it proxies everything at once, and falls to 4th within them.",
             fontsize=8, color=GREY, va="bottom")
    fig.text(0.006, 0.008,
             "CAVEAT: health and trust are self-reported by the same respondent in the same "
             "survey as life satisfaction, so part of their lead is shared method variance. "
             "The externally measured predictors (HDI, SHDI) carry no such advantage.",
             fontsize=8, color=RED, va="bottom")
    fig.tight_layout(rect=(0, 0.05, 1, 0.895))
    path = outdir / "domain_horse_race.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close(fig)
    print(f"Saved: {path}")

# ==========================================================================
# Does the SDG evidence corroborate what the ESS says?
#
# The ESS horse race puts self-rated health and social trust ahead of
# everything, but both are self-reported by the same respondent in the same
# survey as life satisfaction. The SDG database is administrative and shares
# no method with any wellbeing measure, so it is the natural check: a domain
# that leads in both is corroborated; one that leads only in ESS is not.
# ==========================================================================
CORROB = [
    # domain,            SDG pooled %, SDG goal rank, ESS within-country r, colour, verdict
    ("Health", 11.5, "SDG3, 4th of 17 goals; 16 of the top 25 series overall",
     0.513, RED, "corroborated"),
    ("Education", 3.3, "SDG4, 12th of 17; best series 100th of 609",
     -0.078, BLUE, "weak in both"),
    ("Social trust /\ninstitutions", 1.5, "SDG16, 15th of 17; no trust indicator exists",
     0.487, GREEN, "ESS only"),
]


def build_corroboration(outdir: Path):
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.4))
    fig.patch.set_facecolor(BG)
    y = list(range(len(CORROB)))[::-1]
    labels = [c[0] for c in CORROB]

    ax = axes[0]
    ax.barh(y, [c[1] for c in CORROB], 0.55, color=[c[4] for c in CORROB])
    for yi, c in zip(y, CORROB):
        ax.text(c[1] + 0.3, yi + 0.16, f"{c[1]}%", va="center", fontsize=9.5,
                color=INK, fontweight="bold")
        ax.text(c[1] + 0.3, yi - 0.18, c[2], va="center", fontsize=7.6, color=GREY)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlim(0, 14); ax.set_xlabel("% of country × indicator pairs significant in levels", fontsize=9)
    style_axes(ax); ax.grid(axis="y", visible=False)
    ax.set_title("a  Administrative evidence (UN SDG database)", fontsize=11,
                 fontweight="bold", color=INK, loc="left", pad=24)
    ax.text(0, 1.015, "Objective, externally measured — shares no method with any wellbeing survey.",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")

    ax = axes[1]
    ax.barh(y, [c[3] for c in CORROB], 0.55, color=[c[4] for c in CORROB])
    for yi, c in zip(y, CORROB):
        ax.text(c[3] + 0.012, yi, f"+{c[3]:.3f}", va="center", fontsize=9.5,
                color=INK, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels([])
    ax.set_xlim(0, 0.68)
    ax.set_xlabel("Median within-country regional correlation with life satisfaction", fontsize=9)
    style_axes(ax); ax.grid(axis="y", visible=False)
    ax.set_title("b  Self-reported evidence (European Social Survey)", fontsize=11,
                 fontweight="bold", color=INK, loc="left", pad=24)
    ax.text(0, 1.015, "Reported by the same respondent, in the same survey, as life satisfaction.",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")

    fig.text(0.006, 0.972,
             "Health survives the method check. Social trust does not.",
             fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.006, 0.928,
             "Health leads in both an administrative source and a self-report source, so its "
             "showing is not shared-method variance.\nTrust is the strongest ESS predictor and "
             "close to the weakest SDG domain — the framework has no trust indicator at all.",
             fontsize=9, color="#5A5A5A", va="top", linespacing=1.4)
    fig.text(0.006, 0.020,
             "SDG health series in the top 25 are survival measures — infant and under-five "
             "mortality, stunting, neonatal mortality, sanitation, drinking water — none self-reported. "
             "Sources: UN SDG Global Database; European Social Survey rounds 5–11.",
             fontsize=8, color=GREY, va="bottom")
    fig.tight_layout(rect=(0, 0.055, 1, 0.855))
    path = outdir / "health_trust_corroboration.png"
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close(fig)
    print(f"Saved: {path}")

if __name__ == "__main__":
    main()
