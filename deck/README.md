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

Two results and a discussion, in that order: **education**, then **health**,
then **social trust**. The within-country regional analysis has been cut — see
below.

| | |
|---|---|
| **Opening** | Development rose; wellbeing didn't follow. Which of its parts tracks wellbeing at all? |
| **Act I** | Replication. The levels-to-differences collapse holds on the HDI, against ESS, and at regional scale — not an SDG artifact. The subnational HDI is a disaggregation test, not a replication. |
| **Act II** | Result 1 education, Result 2 health, the ESS horse race, then social trust in discussion. Every disagreement between frameworks is about operationalisation. |
| **Act III** | The disconnect, then one implication per result, then an exploratory conclusion. No within-country evidence — see below. |

**The three signatures.**

- **Education** (Result 1) — leads the HDI: highest median R² of the five
  indicators (0.326, just above the composite's 0.322) and 40.7% of countries.
  In the SDGs its rank is entirely a construct artefact: pooled SDG4 is 3.3%
  and twelfth of 17 goals, but the two access-and-participation series alone
  reach **12.7%**, which would rank third of 17 — above SDG3 health. Learning
  outcomes sit at 0.9%, parity ratios at 2.5%, and parity ratios are half the
  goal by series count. Near-universal at the individual level (32–34 of 36)
  and the smallest effect of any domain (median R² 0.0098).
- **Health** (Result 2) — leads the SDG framework (Goal 3, 11.5%, 4th of 17;
  16 of the top 25 series), leads the ESS (36 of 36, median R² 0.091, the
  largest effect anywhere here), and is weak in exactly one place: the HDI,
  whose single health input is close to saturated. The only domain that can be
  put through the administrative-source method check at all, and it passes.
- **Social trust** (discussion, not a headline) — significant in 34 of 36 ESS
  countries at a median R² of 0.041, four times education's and well below
  health's, and invisible to every development framework. It is in the paper
  because the reason it can't be a headline is the paper's subject.

## The within-country analysis is out

The ESS × subnational-HDI regional work — the ranking flip, the within-country
gradients, the GDL sub-index check — is no longer part of the commentary. It is
a separate paper. The code, figures and processed files all stay in the
repository; they are simply no longer published into `deck/figures/` or cited
by `content.py`.

Why it came out:

- **Europe-only, 16 countries** with ≥6 matched regions, and coverage is uneven
  — Italy matches 30% of respondents to a region, Sweden 57%, Croatia 69%.
- **It is specification-sensitive in a way that needs room to examine.**
  Education's median regional correlation changes sign between two defensible
  aggregations (−0.08 from per-round region means, +0.13 pooling respondents),
  and the health-versus-trust ordering swaps under the same choice. Those are
  interesting problems given a robustness section and liabilities without one.
- **It costs both display items.** A commentary carries one or two figures; the
  flip needs its own, and so does the composite.

What the commentary loses: social trust drops to the individual ESS result (34
of 36 countries, median R² 0.041) plus the SDG coverage and cross-section work,
which is enough for a discussion but not for a headline. Education's
universal-but-tiny pattern keeps its explanation from the individual-vs-country
contrast in the horse race rather than from the regional layer.

What survives untouched: the whole of Act I, including the regional-scale
collapse replication — that beat is about the collapse generalising, not about
which domain wins, so it stays — and all of Act II's framework and construct
work.

**The education finding that prompted this.** Adding education to G3 and G4
showed it has no consistent within-country signal: 8 of 16 countries positive
and 8 negative, with the three significant countries pointing both ways
(Austria −0.81, France +0.50, the Netherlands +0.60), against 12 of 16 positive
for health and 14 of 16 for trust. `specification_synthesis.py` prints both
aggregations on every run. That result travels with the separate paper.

## Act III's altitude: implications, not recommendations

The act was rewritten to sit where the evidence sits. The claim is a
**disconnect**, not an indictment:

- **Not** that development frameworks should be kept away from wellbeing, or
  that they have failed. The HDI and the SDGs were built to track development
  and on those terms they work. The text says this explicitly, in the act
  thesis and again in "The disconnect".
- **The claim** is that what these frameworks currently capture and what tracks
  individual lived experience are assumed to move together, and that
  assumption holds between countries and weakens sharply everywhere else.
- **The conclusion** is deliberately exploratory: development frameworks may
  need to work harder at capturing the components that shape lived experience.
  Education is pooled with constructs pointing the other way; health is read
  through a variable that has largely stopped moving; social trust is not
  measured with the coverage any longitudinal design needs.
- **The ask is a question**, not a prescription — what would a development
  framework look like if these components were among the things it was built
  to capture? The commentary shows the question isn't rhetorical; it doesn't
  answer it.

Each of the three implication beats keeps its own caveat rather than deferring
them all to a limitations paragraph: education's signal is between-country and
tiny within, health's turns on saturation, trust's rests on one instrument in
Europe with a live shared-method objection.

`DECISIONS` carries the open question of whether this is the right altitude for
the venue, or whether the health and education implications should be sharpened
into named recommendations. The evidence supports either — the framing does not
change the analysis.

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

`figures/` is populated by `../data_collection/publish_deck_figures.py`, which
holds the deck-name → `figures_out` name mapping. That mapping used to exist
only as a set of hand-renamed copies, so a rebuild meant guessing — and guessing
wrong is silent, since the deck embeds whatever PNG carries the right name.
(`mechanisms_trust_health.png` is E1, not G3, for instance.) Add a figure there
when you add one here.

Sources are `make_figures.py`, `make_commentary_figure.py`, and three
standalone builders — `domain_scorecard.py` (`J1_`),
`sdg_trust_cross_section.py` (`K1_`), `specification_synthesis.py` (`L1_`):

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

## Three wording cautions carried in the text

Education is **not** an exception to the differences collapse. Expected years
of schooling leads that column with 7 of 150 countries — a lead over the
composite's 3, and still a collapse. It is the exception in *consistency*
across frameworks, producers, instruments, and units of observation.

Education leading is a **between-country** claim. At the individual level it is
significant in 32–34 of 36 countries at a median R² of 0.0098 — the smallest
effect of any domain tested. Act III's education implication says what a global
monitoring framework should count; it is not a claim that a given schooling
gain moves a given person's life satisfaction, and the text says so explicitly.

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
| Ranking flip: +0.117 (3/16), health +0.513 (8/16), trust +0.487 (6/16) | reproduced exactly — now carried by the separate within-country paper, not this one |
| Region crosswalk, 217,422 / 351,023 | reproduced; three hand-rejected mismatches now excluded |
| SDG trust cross-section, 9 of 13 testable, 4 significant | computed fresh from the UN SDG API; comparators on each series' own country set |
| SDG4 access 12.7% = 3rd of 17 goals if it were one | checked against `sdg_education_category_significance.csv` and the goal table; 2 series / 63 pairs, and the text says so |

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
