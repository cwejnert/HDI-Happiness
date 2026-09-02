"""
Which framework can see which domain?

The paper's three takeaway domains are health, education and social trust.
They are not equally visible to the instruments that measure development, and
the pattern of visibility is itself the finding:

    HEALTH     testable everywhere, and leads almost everywhere it is measured
               with variance. Weak ONLY inside the HDI, whose single health
               input (life expectancy) is close to saturated.

    EDUCATION  testable everywhere. Leads the HDI, trails badly in the SDG
               framework (pooling parity ratios with access), near-universal
               but tiny at the individual level.

    TRUST      near the top of the one instrument that measures it repeatedly,
               and effectively INVISIBLE to every development framework. This
               is the key correction to an earlier draft, which recorded trust
               as "no SDG indicator exists". That was wrong: the SDG database
               carries 13 trust- and satisfaction-adjacent series (SDG16
               mostly -- satisfaction with public services, belief that
               decision-making is inclusive, bribery prevalence). But their
               median coverage is ONE observation per country-series against 6
               for the database as a whole, so almost none can support a
               time-series test at all. Of 163 country-tests across those
               series exactly 1 is significant. That is a measurement gap, not
               a substantive null, and the deck must not report it as evidence
               that trust does not matter.

Inputs:  raw/robust_all_for_figures.csv (trust-series coverage check)
         plus results transcribed from the other pipeline scripts
Output:  figures_out/J1_domain_framework_scorecard.png
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle

BG, INK, GREY = "#FCFCFB", "#1A1A1A", "#8A8A8A"
STRONG = "#1BAF7A"   # domain clearly tracks wellbeing here
WEAK = "#EDA100"     # measurable, but little or no signal
BLIND = "#C9CDD4"    # the framework cannot test this domain

COLUMNS = [
    ("UN SDG\n42 countries", "% of country × indicator\npairs significant, levels"),
    ("UNDP HDI\n150 countries", "% of countries\nsignificant, levels"),
    ("Subnational HDI\n16 countries", "median within-country\nregional r (external)"),
    ("ESS individual\n36 countries", "countries significant,\nmedian R²"),
    ("ESS regional\n16 countries", "median within-country\nregional r"),
]

# value, status, optional footnote marker
ROWS = [
    ("Health", [
        ("11.5%\nSDG3, 4th of 17 goals", STRONG),
        ("19.9%\nlife expectancy — last of 5", WEAK),
        ("+0.344\n6 of 15 countries", STRONG),
        ("36 of 36\nR² = 0.091", STRONG),
        ("+0.513\n8 of 16 countries", STRONG),
    ]),
    ("Education", [
        ("3.3% pooled · 12.7% access\nbest series 100th of 609", WEAK),
        ("40.7% / 34.0%\nmean / expected schooling", STRONG),
        ("+0.057\n2 of 16 countries", WEAK),
        ("33 of 36\nR² = 0.0098", STRONG),
        ("+0.130\n2 of 16 countries", WEAK),
    ]),
    ("Social trust", [
        ("13 series exist,\n1 of 163 tests significant —\nmedian 1 year of data", BLIND),
        ("not measured", BLIND),
        ("not measured", BLIND),
        ("34 of 36\nR² = 0.041", STRONG),
        ("+0.487\n6 of 16 countries", STRONG),
    ]),
]


def verify_trust_coverage():
    """The trust claim rests on coverage, so recompute it rather than trust a note."""
    s = pd.read_csv("raw/robust_all_for_figures.csv", low_memory=False)
    s["sig"] = s.sig_levels_fdr.eq("q<.05")
    codes = ["IU_DMK_INCL", "IU_COR_BRIB", "IC_FRM_BRIB", "SP_PSR_OSATIS_HLTH",
             "IU_DMK_ICRS", "SP_PSR_OSATIS_GOV", "SP_PSR_OSATIS_SEC",
             "SP_PSR_SATIS_GOV", "SP_PSR_SATIS_HLTH", "SP_PSR_OSATIS_PRM",
             "SP_PSR_SATIS_PRM", "SP_PSR_SATIS_SEC", "VC_VOV_GDSD"]
    t = s[s.SeriesCode.isin(codes)]
    print(f"SDG trust/satisfaction series: {t.SeriesCode.nunique()} series, "
          f"{len(t)} country-tests, {int(t.sig.sum())} significant")
    print(f"  median years of data per country-series: {t.n_levels.median():.0f}  "
          f"(all 661 series: {s.n_levels.median():.0f})")
    return t.SeriesCode.nunique(), len(t), int(t.sig.sum())


def main():
    verify_trust_coverage()

    fig, ax = plt.subplots(figsize=(16.5, 6.6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ncol, nrow = len(COLUMNS), len(ROWS)
    cw, ch = 1.0, 1.0
    left_pad = 1.15

    for j, (head, metric) in enumerate(COLUMNS):
        x = left_pad + j * cw
        ax.text(x + cw / 2, nrow + 0.62, head, ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=INK)
        ax.text(x + cw / 2, nrow + 0.44, metric, ha="center", va="top",
                fontsize=7.6, color=GREY, linespacing=1.35)

    for i, (domain, cells) in enumerate(ROWS):
        y = nrow - 1 - i
        ax.text(left_pad - 0.12, y + ch / 2, domain, ha="right", va="center",
                fontsize=12.5, fontweight="bold", color=INK)
        for j, (txt, status) in enumerate(cells):
            x = left_pad + j * cw
            hatch = "///" if status is BLIND else None
            ax.add_patch(Rectangle((x + 0.03, y + 0.05), cw - 0.06, ch - 0.10,
                                   facecolor=status, alpha=0.20 if status is BLIND else 0.28,
                                   edgecolor=status, linewidth=1.4, hatch=hatch))
            ax.text(x + cw / 2, y + ch / 2, txt, ha="center", va="center",
                    fontsize=8.2, color=INK, linespacing=1.5)

    ax.set_xlim(0, left_pad + ncol * cw + 0.05)
    ax.set_ylim(-0.95, nrow + 1.15)
    ax.axis("off")

    handles = [Rectangle((0, 0), 1, 1, facecolor=c, alpha=a, edgecolor=c, linewidth=1.4, hatch=h)
               for c, a, h in [(STRONG, .28, None), (WEAK, .28, None), (BLIND, .20, "///")]]
    ax.legend(handles, ["Tracks wellbeing here",
                        "Measurable, but little signal",
                        "Framework cannot test it"],
              loc="lower center", bbox_to_anchor=(0.5, -0.10), ncol=3,
              frameon=False, fontsize=9)

    fig.text(0.005, 0.972,
             "Health, education and social trust — and which frameworks can see them",
             fontsize=15.5, fontweight="bold", color=INK, va="top")
    fig.text(0.005, 0.928,
             "The pattern of blind spots is the finding. Health is testable everywhere and leads "
             "almost everywhere it varies. Education is testable everywhere and its rank depends "
             "entirely on construct.\nTrust is near the top of the one instrument that measures it "
             "repeatedly — and effectively invisible to every development framework.",
             fontsize=9, color="#5A5A5A", va="top", linespacing=1.5)
    fig.text(0.005, 0.028,
             "The SDG framework does carry 13 trust- and satisfaction-adjacent series (SDG16: "
             "satisfaction with public services, inclusive decision-making, bribery), but their "
             "median coverage is ONE year per country-series\nagainst six for the database as a "
             "whole — too thin for a time-series test. One of 163 country-tests is significant. "
             "That is a measurement gap, not evidence that trust does not matter.",
             fontsize=7.8, color=GREY, va="bottom", linespacing=1.5)
    fig.tight_layout(rect=(0, 0.06, 1, 0.885))
    out = "figures_out/J1_domain_framework_scorecard.png"
    fig.savefig(out, dpi=200, facecolor=BG)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
