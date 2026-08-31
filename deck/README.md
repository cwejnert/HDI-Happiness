# The commentary, in four acts

Presentation and synthesis layer for the follow-on paper. `content.py` holds
the argument; the two build scripts render it two ways.

```bash
python build_artifact.py   # -> education_exception.html  (self-contained, ~5 MB)
python build_pptx.py       # -> The_Education_Exception.pptx  (43 slides, 16:9)
```

Both read `content.py` and `figures/`. Edit the argument in one place and
rebuild both; don't edit the HTML or the PPTX directly.

## Structure

| | |
|---|---|
| **Opening** | Development rose; wellbeing didn't follow. The dismissal this commentary has to close. |
| **Act I** | The levels-to-differences collapse replicates on the HDI, on the subnational HDI, against ESS, and at the regional scale. It is a property, not an SDG artifact. |
| **Act II** | Education is the exception in *consistency* — significant at every level of aggregation down to the individual — but only measured as attainment and access. |
| **Act III** | Between countries development leads; within them health and trust do, and development flattens. Europe-only. |
| **Act IV** | The policy question: the education architecture is built on measured learning, the wellbeing evidence points at attainment. |

`DECISIONS` carries the five open questions for the co-author team;
`APPENDIX` carries the 13 supporting figures not used in the acts.

## Figures

`figures/` holds the 25 PNGs produced by `../data_collection/make_figures.py`
plus the composite proposed for submission. These are aggregate results, not
microdata, so unlike `data_collection/processed/` they are committed — the
deck must be rebuildable without re-running the merges.

`Figure1_commentary.png` (and `.pdf`) is built by
`../data_collection/make_commentary_figure.py`. That script transcribes
already-computed results rather than reading the microdata; if an upstream
number changes, update it there too.

## A wording caution carried in Act II

Education is **not** an exception to the differences collapse — almost
nothing is; only 9 of 609 SDG series have any first-differences
significance. It is the exception in consistency across frameworks,
producers, wellbeing instruments, and units of observation. Act II's closing
paragraph states this precisely, and it should survive editing.
