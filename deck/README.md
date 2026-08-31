# The commentary, in three acts

Presentation and synthesis layer for the follow-on paper. `content.py` holds
the argument; the two build scripts render it two ways.

```bash
python build_artifact.py   # -> education_exception.html  (self-contained)
python build_pptx.py       # -> The_Education_Exception.pptx  (16:9)
```

Both read `content.py` and `figures/`. Edit the argument in one place and
rebuild both; don't edit the HTML or the PPTX directly.

## The arc

The three acts follow the agreed narrative: replicate the SDG result, ask
what is different about education, then turn that into a policy question.

| | |
|---|---|
| **Opening** | Development rose; wellbeing didn't follow. The dismissal this commentary has to close. |
| **Act I** | Replication. The levels-to-differences collapse holds on the HDI, on the subnational HDI, against ESS, and at the regional scale — so it is not an SDG artifact. The ESS and subnational work lives here. |
| **Act II** | So what is it about education? It is the one construct significant at every level of aggregation down to the individual — but only measured as attainment and access. |
| **Act III** | Priorities (where the lever is, which turns on scale) and what kind of education, ending on the policy question. |

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

| Result | Status |
|---|---|
| SDG goal percentages, SDG4 construct split, top-20 ranking | verified against `robust_all_for_figures.csv` |
| HDI composite and sub-components, both specs | verified against `HDI_indicator_summary.csv`, reproduced independently |
| SHDI national collapse (66/148 → 6/148) | reproduced from the GDL export |
| **Everything ESS** — Act I replication 3–4, Act II individual level and triangulation, Act III priorities | **unverified.** Rests on a pipeline run whose inputs were lost; needs the ESS extract re-exported and the merges re-run. |
