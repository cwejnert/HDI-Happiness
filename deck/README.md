# Measured Where It Varies

The commentary, in three acts.

Presentation and synthesis layer for the follow-on paper. `content.py` holds
the argument; the two build scripts render it two ways.

```bash
python build_artifact.py   # -> education_exception.html  (self-contained)
python build_pptx.py Measured_Where_It_Varies.pptx   # 16:9 deck
```

Both read `content.py` and `figures/`. Edit the argument in one place and
rebuild both; don't edit the HTML or the PPTX directly.

## The arc

Three domains — health, education, social trust — carried through Act II and
into the policy act.

| | |
|---|---|
| **Opening** | Development rose; wellbeing didn't follow. Which of its parts tracks wellbeing at all? |
| **Act I** | Replication. The levels-to-differences collapse holds on the HDI, against ESS, and at regional scale — not an SDG artifact. The subnational HDI is a disaggregation test, not a replication. |
| **Act II** | Three domains, and which frameworks can see them. Health, education and social trust each have a different signature across the five instruments, and every disagreement is about operationalisation. |
| **Act III** | Priorities, what kind of health and education, the trust gap, and the policy question. |

**The three signatures.**

- **Health** — testable in all five instruments, leads in four. Weak only
  inside the HDI, whose single health input (life expectancy) is close to
  saturated. Corroborated across an administrative source and a self-report
  source, and at national and regional scale.
- **Education** — testable in all five; its rank swings from first (HDI, 40.7%)
  to near-last (pooled SDG4, 3.3%) purely on whether the instrument measures
  attainment or parity. Near-universal at the individual level but the smallest
  effect of any domain (median R² 0.0098).
- **Social trust** — at or near the top of the one instrument that measures it
  repeatedly (34 of 36 countries; +0.49 within countries), and invisible to
  every development framework.

**The trust correction.** An earlier draft recorded "no SDG trust indicator
exists". That is wrong. The SDG database carries 13 trust- and
satisfaction-adjacent series (Goal 16: satisfaction with public services,
inclusive decision-making, bribery prevalence). But their median coverage is
**one observation per country-series** against six for the database as a
whole. The design needs ≥4 years, so **147 of 163 country-series cannot be
computed at all** and 16 can; 1 of those 16 is significant. Always report it as
"1 of 16 testable", never "1 of 163" — the latter reads as a null when it is
overwhelmingly a coverage gap, and would repeat exactly the error the
commentary accuses the frameworks of making. `domain_scorecard.py` recomputes
this rather than trusting a transcribed note.

**The cross-sectional test.** Untestable *in this design* is not untestable in
principle, so the raw values were pulled from the UN SDG Global Database API
(`../data_collection/pull_sdg_trust_series.py` → `raw/sdg_trust_series_values.csv`)
and the series run against the Cantril ladder across countries
(`sdg_trust_cross_section.py`). The API coverage is far wider than the analysis
file implied — 156 countries for `SP_PSR_OSATIS_HLTH`, not 30.

| | |
|---|---|
| Testable (≥12 countries with a matched ladder value) | **9 of 13** |
| Significant after BH across the nine | **4** — `IU_COR_BRIB` −0.55, `IC_FRM_BRIB` −0.51, `IU_DMK_INCL` −0.42, `SP_PSR_OSATIS_HLTH` +0.33 |
| HDI and components, same 134 countries | \|r\| **0.71–0.83** — every trust series is below the band |
| Net of log GNI per capita | **0 of 9** survive — and neither does the HDI (+0.82 → +0.09) |

Three cautions travel with this result and are stated in the figure, the deck
and the docstring:

1. **The income null is not trust-specific.** Net of log GNI nothing survives a
   cross-section of countries, the HDI included. Reporting "0 of 9" without the
   comparator would be the same category of error as "1 of 163".
2. **The broadest series shares its instrument with the outcome.**
   `SP_PSR_OSATIS_HLTH` is Gallup World Poll, which is where the WHR ladder
   comes from. It is a same-instrument comparison, not corroboration — exactly
   the objection the deck raises against the ESS self-reports.
3. **None of the 13 measures interpersonal trust.** They measure satisfaction
   with public services and experience of bribery: institutional confidence, a
   different construct. The commentary must not silently promote them.

`IU_DMK_INCL` correlates *negatively* (−0.42): countries where more people say
decision-making is inclusive are less happy. That is a known artefact of
subjective institutional scales compared across very unequal income levels, and
is footnoted rather than interpreted.

Net effect on the argument: the Act III recommendation to field a repeated trust
item is now supported rather than asserted — the alternative was tried and it
lands below every development indicator the frameworks already carry.

`DECISIONS` carries the open questions for the co-author team; `APPENDIX`
carries the supporting figures not used in the acts.

## Figures

`figures/` holds the PNGs produced by `../data_collection/make_figures.py`
plus three built by `../data_collection/make_commentary_figure.py`:

- `Figure1_commentary.png` / `.pdf` — the proposed submission figure
- `collapse_hdi_shdi_whr.png` — rebuilt; the original reported an HDI
  collapse of 67/150 → 6/150 that reproduces under no specification
- `hdi_full_structure.png` — composite plus sub-components, both specs

`make_commentary_figure.py` transcribes already-computed results rather than
reading microdata, so these survive without the data files. If an upstream
number changes, update it there too.

These are aggregate results, not microdata, so unlike `data_collection/raw/`
and `processed/` they are committed — the deck must be rebuildable without
re-running the merges.

## Two wording cautions carried in the text

Education is **not** an exception to the differences collapse. Expected years
of schooling leads that column with 7 of 150 countries — a lead over the
composite's 3, and still a collapse. It is the exception in *consistency*
across frameworks, producers, instruments, and units of observation.

The SDG and HDI **detection** rates (71% vs 51% of each dataset's countries
with any indicator significant) are a fair comparison, not an artifact:
Benjamini–Hochberg under the complete null controls the error rate at the same
α whatever the family size, so the SDG lead is genuine power bought with
breadth. An earlier draft claimed the opposite and normalised by the share of
each country's own indicators; that was dropped, because it penalises breadth
for its own sake. `framework_efficiency.py` now reports three comparisons —
detection, budget-matched (5 vs 5 random), and per-indicator — and nominates
none as the headline.

For **collapse** the comparable quantity is still the levels-to-differences
ratio, not the level, since the two frameworks differ in indicator count.

## Verification status

The ESS extract, the SDG results file, the HDI panel and the GDL export were
all restored, and `make_figures.py` now runs end to end again. Every headline
number has been checked against source.

| Result | Status |
|---|---|
| SDG goal percentages, SDG4 construct split, top-20 ranking, rank 100/609 | reproduced exactly |
| HDI composite and sub-components, both specs | matches `HDI_indicator_summary.csv`; independent recomputation differs by at most one country in the denominator |
| ESS individual education, 32–34 of 36 | reproduced exactly |
| HDI × ESS collapse, 14.8% / 8.8% | reproduced |
| Ranking flip: +0.150 (3/16), health +0.513 (8/16), trust +0.487 (6/16) | reproduced exactly |
| Region crosswalk, 217,422 / 351,023 | reproduced; three hand-rejected mismatches now excluded |
| SDG trust cross-section, 9 of 13 testable, 4 significant | computed fresh from the UN SDG API; comparators on each series' own country set |

Three region matches cleared the 0.6 similarity threshold but were the wrong
region (`SI` Notranjsko-kraška→Obalno-kraska, `SK` Trnavský→Bratislavsky,
`FI` Etelä-Pohjanmaa→Etela-Suomi) and are now blocklisted in
`build_region_crosswalk.py`. Only the Slovenian one touched Act III; removing
it moved the within-country development correlation from +0.150 to +0.117 and
left health and trust unchanged. Most other low scores are cross-language, not
wrong — Croatian county names and Finnish macro-regions score badly and match
correctly.

Act III coverage is uneven and the text now says so: Italy matches 30% of
respondents to a region, Sweden 57%, Croatia 69%, everywhere else 91–100%.
The ranking flip survives dropping those three and survives dropping regions
built on fewer than 200 respondents.

Three errors were found and corrected in the process:

1. **The SDG collapse figure.** `64/151 → 3/151` is the HDI composite, not the
   SDG result. The SDG framework gives `30/42 → 2/42`, and the two rates are
   not directly comparable — the SDG test asks whether any of a country's
   ~456 series is significant.
2. **The triangulation comparator.** ESS-aggregated schooling gives R² = 0.308
   against WHR happiness; the draft compared this to 0.326, which is a median
   *within*-country time-series R². The comparable figure is 0.161, so the
   finding is stronger than claimed, not equal.
3. **The subnational HDI as a replication.** GDL's national SHDI is
   numerically identical to the UNDP HDI (1,696/1,696 country-years, max
   difference 0.000) because it is derived from it. It is not an independent
   producer and is no longer counted as one. Its region-level values are
   genuine — only 655 of 58,224 region-years match their national figure — so
   the disaggregation test in Act III is unaffected.

## Rebuilding the pipeline intermediates

`make_figures.py` sections C, F and G depend on intermediates that no single
script produced. If `processed/` is ever empty again, these must be rebuilt
before the pipeline will run: `national_hdi_shdi_whr_panel.csv`,
`hdi_country_indicator_significance.csv`, `sdg_goal_significance_pooled.csv`,
`sdg_education_category_significance.csv`, `sdg_series_significance_ranking.csv`,
`ess_individual_education_by_country.csv`, `ess_country_education_panel.csv`.
See `../data_collection/build_intermediates.py`.
