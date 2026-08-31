"""
Composite Figure 1 for the commentary submission.

Commentaries allow one or two display items, so the three results that carry
the argument have to share a single figure:

    (a) the levels-to-differences collapse, replicated across three
        development frameworks against the World Happiness Report;
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

PROVENANCE = """Panel a: HappinessSDG.R (SDG); make_figures.py section B (HDI), section C (SHDI).
Panel b: make_figures.py section F, SDG4 indicators classified by construct.
Panel c: sections B, D, F. Denominators differ by row and are labelled."""

# --------------------------------------------------------------------------
# (a) The collapse: countries FDR-significant in levels vs. first-differences
# --------------------------------------------------------------------------
COLLAPSE = [
    # label,                  n_sig_levels, n_sig_diffs, n_countries
    ("SDG indicators\n(original paper)", 64, 3, 151),
    ("Human Development\nIndex", 67, 6, 150),
    ("Subnational HDI\n(national aggregate)", 66, 6, 148),
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
    ("HDI expected years of schooling", "of 150 countries", 33.6, BLUE),
    ("HDI mean years of schooling", "of 150 countries", 40.9, BLUE),
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
    ax.set_ylim(0, 62)
    ax.set_ylabel("% of countries with a significant\ndevelopment–happiness association", fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, loc="upper center", ncol=2,
              bbox_to_anchor=(0.5, 1.02))
    style_axes(ax)
    ax.set_title("a  The collapse is not an artifact of the SDG framework",
                 fontsize=10.5, fontweight="bold", color=INK, loc="left", pad=24)
    ax.text(0, 1.012, "Same design, three development frameworks, one outcome (WHR Cantril ladder).",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")


def panel_b(ax):
    labels = [f"{s[0]}  ({s[2]})" for s in SDG4_BY_CONSTRUCT]
    vals = [s[1] for s in SDG4_BY_CONSTRUCT]
    cols = [s[3] for s in SDG4_BY_CONSTRUCT]
    x = range(len(vals))

    ax.bar(x, vals, 0.66, color=cols)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.35, f"{v:.1f}%", ha="center", fontsize=9, color=INK, fontweight="bold")

    ax.axhline(SDG4_POOLED_PCT, color=INK, linestyle=(0, (4, 3)), linewidth=1.1)
    ax.text(len(vals) - 0.42, SDG4_POOLED_PCT + 0.4,
            f"all 35 pooled: {SDG4_POOLED_PCT}%", ha="right", fontsize=8, color=INK)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=8, rotation=25, ha="right",
                       rotation_mode="anchor")
    ax.set_ylim(0, 14.5)
    ax.set_ylabel("% of country × indicator pairs\nsignificant in levels", fontsize=9)
    style_axes(ax)
    ax.set_title("b  SDG4's weakness is a pooling artifact",
                 fontsize=10.5, fontweight="bold", color=INK, loc="left", pad=24)
    ax.text(0, 1.012,
            "Its 35 official indicators, split by what each measures "
            "(number of series in brackets).",
            transform=ax.transAxes, fontsize=8.3, color="#5A5A5A", va="bottom")


def panel_c(ax):
    labels = [e[0] for e in EDU_LADDER]
    notes = [e[1] for e in EDU_LADDER]
    vals = [e[2] for e in EDU_LADDER]
    cols = [e[3] for e in EDU_LADDER]
    y = list(range(len(vals)))[::-1]

    ax.barh(y, vals, 0.58, color=cols)
    for yi, v, n in zip(y, vals, notes):
        ax.text(v + 1.4, yi, f"{v:.1f}%", va="center", fontsize=9.5,
                color=INK, fontweight="bold")
        ax.text(143, yi, n, va="center", ha="right", fontsize=8, color=GREY)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlim(0, 145)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("% of tests FDR-significant in levels", fontsize=9)
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color="#E6E6E6", linewidth=0.8)
    fig = ax.get_figure()
    fig.text(0.085, 0.418,
             "c  Education's signal strengthens as measurement moves toward attainment",
             fontsize=10.5, fontweight="bold", color=INK, va="bottom")
    fig.text(0.085, 0.382,
             "Each row's denominator is given at right: these are not one scale, "
             "so read the pattern rather than bar length.",
             fontsize=8.3, color="#5A5A5A", va="bottom")


def main():
    outdir = Path(sys.argv[1] if len(sys.argv) > 1 else "figures_out")
    outdir.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(12.6, 9.2))
    fig.patch.set_facecolor(BG)
    # Two gridspecs rather than one: panel c's row labels need a much wider
    # left margin than a and b do.
    gs_top = fig.add_gridspec(1, 2, left=0.085, right=0.985, top=0.855,
                              bottom=0.575, wspace=0.30)
    gs_bot = fig.add_gridspec(1, 1, left=0.215, right=0.985, top=0.355, bottom=0.105)
    panel_a(fig.add_subplot(gs_top[0, 0]))
    panel_b(fig.add_subplot(gs_top[0, 1]))
    panel_c(fig.add_subplot(gs_bot[0, 0]))

    fig.text(0.008, 0.975,
             "Development, wellbeing, and the education exception",
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


if __name__ == "__main__":
    main()
