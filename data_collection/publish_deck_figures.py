"""
Copy figures_out/ into deck/figures/ under the names the deck refers to.

Until now this mapping existed only as a set of hand-renamed copies. Nothing in
the repository recorded that `ranking_flip.png` is G4 or that
`mechanisms_trust_health.png` is E1 rather than G3, so a rebuild meant guessing
-- and guessing wrong is silent, because the deck just embeds whatever PNG has
the right name.

Every figure the deck uses is listed here. Run after make_figures.py and the
standalone builders:

    python make_figures.py
    python make_commentary_figure.py
    python domain_scorecard.py
    python sdg_trust_cross_section.py
    python specification_synthesis.py
    python subindex_within_country.py
    python publish_deck_figures.py

Then rebuild the deck itself from deck/.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

SRC = Path(__file__).parent / "figures_out"
DST = Path(__file__).parent.parent / "deck" / "figures"

# deck name -> figures_out name. Names on the left are what content.py cites.
MAPPING = {
    # Act I -- the replicated collapse
    "collapse_hdi_shdi_whr.png": "collapse_hdi_shdi_whr.png",
    "hdi_full_structure.png": "hdi_full_structure.png",
    "collapse_hdi_ess.png": "B4_collapse_bar_national.png",
    "collapse_shdi_ess_regional.png": "D3_collapse_scatter_regional.png",

    # Act II -- frameworks, the two results, the synthesis
    "framework_three_comparisons.png": "I1_framework_three_comparisons.png",
    "sdg_indicator_top20.png": "F6_sdg_indicator_ranking.png",
    "sdg4_unpooled.png": "F2_sdg4_education_categories.png",
    "ess_individual_education.png": "F4_ess_individual_education_boxplot.png",
    "sdg_by_goal.png": "F1_sdg_goal_significance_ranking.png",
    "health_trust_corroboration.png": "health_trust_corroboration.png",
    "domain_horse_race.png": "domain_horse_race.png",
    "L1_three_specifications.png": "L1_three_specifications.png",
    "K1_sdg_trust_cross_section.png": "K1_sdg_trust_cross_section.png",
    "domain_scorecard.png": "J1_domain_framework_scorecard.png",
    "Figure1_commentary.png": "Figure1_commentary.png",
    "Figure1_commentary.pdf": "Figure1_commentary.pdf",

    # Act III -- the within-country evidence
    "within_country_gradient.png": "G2_within_country_gradients.png",
    "ranking_flip.png": "G4_ranking_flip_national_vs_within.png",
    "within_country_external.png": "H1_within_country_external_domains.png",

    # Appendix
    "ess_year_coverage.png": "A3_ess_year_coverage.png",
    "region_crosswalk_match.png": "A1_shdi_match_rate_by_country.png",
    "hdi_ess_heatmap.png": "B1_heatmap_country_indicator.png",
    "hdi_ess_collapse_scatter.png": "B2_collapse_scatter_national.png",
    "hdi_vs_lifesat_trends.png": "B5_quadrant_national.png",
    "shdi_whr_levels_scatter.png": "C1_whr_vs_shdi_national_levels.png",
    "shdi_vs_hdi_validation.png": "C3_hdi_vs_shdi_national_agreement.png",
    "region_shdi_lifesat_pooled.png": "D1_region_scatter_stflife_vs_shdi.png",
    "within_country_small_multiples.png": "D2_within_country_region_smallmultiples.png",
    "european_regional_inequality.png": "D4_shdi_distribution_by_country.png",
    "mechanisms_trust_health.png": "E1_mechanism_variables.png",
    "mechanisms_percountry_detail.png": "G3_within_country_mechanisms.png",
    "shdi_within_country_spread.png": "G1_within_country_shdi_inequality.png",
    "hdi_vs_sdg_frameworks.png": "F3_hdi_vs_sdg_crossref.png",
    "ess_triangulation.png": "F5_ess_agg_education_vs_whr.png",
}


def main():
    DST.mkdir(parents=True, exist_ok=True)
    copied, missing = 0, []
    for deck_name, src_name in sorted(MAPPING.items()):
        src = SRC / src_name
        if not src.exists():
            missing.append(f"{src_name} -> {deck_name}")
            continue
        shutil.copy2(src, DST / deck_name)
        copied += 1
    print(f"Copied {copied} of {len(MAPPING)} figures into {DST}")

    if missing:
        print("\nMissing from figures_out (run the builder that makes them):")
        for m in missing:
            print(f"  {m}")

    # a name in deck/figures that nothing maps to is a leftover from an earlier
    # hand-copy and will quietly go stale, so say so rather than deleting it
    strays = sorted(p.name for p in DST.iterdir()
                    if p.is_file() and p.name not in MAPPING)
    if strays:
        print("\nIn deck/figures but not in MAPPING (stale, or add them here):")
        for s in strays:
            print(f"  {s}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
