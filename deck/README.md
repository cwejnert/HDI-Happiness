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

Health-led, with education carried as a marked sub-highlight thread inside
Act II.

| | |
|---|---|
| **Opening** | Development rose; wellbeing didn't follow. Which of its parts tracks wellbeing at all? |
| **Act I** | Replication. The levels-to-differences collapse holds on the HDI, against ESS, and at regional scale — not an SDG artifact. The subnational HDI is a disaggregation test, not a replication. |
| **Act II** | What matters is decided by how you measure it. Health is the HDI's weakest component and the strongest thing in both the SDG ranking and the ESS; education runs the same problem in reverse. Social trust cannot be checked. |
| **Act III** | Priorities (where the lever is, which turns on scale), what kind of health and education, and the policy question. |

**Why health leads.** It is the only domain that leads in both an
administrative source and a self-report source. Restricted to high-income
countries — the ESS's own stratum — the SDG data puts health at 11.2% against
education's 1.2%, the same ordering the ESS gives from entirely different
measurement. Social trust tops the ESS and has no SDG indicator at all, so it
enters as an open question rather than a result.

**Why the HDI disagrees.** Life expectancy is close to saturated across the
countries where it is tested, so the HDI's only health input has no variance
left to predict with. The SDG series carrying health's signal are survival
measures that still vary; self-rated health captures morbidity life expectancy
cannot see.

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

The SDG and HDI collapse rates are **not directly comparable**. The SDG test
asks whether any of a country's ~456 series is significant; the HDI test asks
about one composite. That is why SDG levels sit at 71% and HDI at 42%. The
collapse ratio is the comparable quantity.

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
