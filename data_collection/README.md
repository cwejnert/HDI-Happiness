# Data collection: ESS × National HDI × SHDI

Pipeline for the expansion described in the concept note
("Human Development and Subjective Well-Being in Europe Using ESS, HDI, and
SHDI"). It covers both designs at once:

- **Approach 1** — ESS respondents + national HDI (`merge_national_hdi_ess.py`)
- **Approach 2** — ESS respondents + Subnational HDI, SHDI (`merge_shdi_ess.py`)

and the concept note's own **feasibility check** that should happen before
committing to Approach 2 (`ess_region_coverage.py`, `build_region_crosswalk.py`).

## Why this isn't fully automated

Both ESS and Global Data Lab (GDL, publisher of SHDI) require a free account
before you can bulk-download data. Confirmed directly against both sites:
GDL's download page says *"Login required — you need to be logged in to
download Subnational HDI files"*, and ESS's data portal (ess.sikt.no) is
now a login-gated web app. Neither exposes a stable, unauthenticated bulk
API, so step 1 for both sources is a one-time manual export through the
browser. Everything after that — cleaning, the regional crosswalk, the
merges — is scripted.

This also happens to be the right workflow for a paper: both ESS and GDL
ask you to cite the specific dataset **version** you downloaded, which their
web UI does for you automatically (a manual API scrape wouldn't).

## Step 0 — install dependencies

```bash
pip install -r requirements.txt
```

## Step 1 — get the ESS extract

1. Register at <https://ess.sikt.no/> (free).
2. Use the **Data Builder** (or "Search data" → build your own file) to
   select:
   - **Rounds**: 1–11 (or whichever subset you want; round→year mapping is
     in `config.ESS_ROUND_YEAR`)
   - **Countries**: all, or restrict to `config.ESS_COUNTRY_ISO3`
   - **Variables**: everything listed in `config.ESS_VARIABLES` — the
     Data Builder lets you search by variable name (e.g. `stflife`,
     `ppltrst`, `trstprl`). Don't forget `region` — it's easy to miss
     since it's grouped under "administrative variables," and it's the one
     variable the whole subnational design depends on.
   - **Format**: SPSS (`.sav`) is preferred because it preserves the value
     labels needed for `region_label` (e.g. "Stuttgart" rather than a bare
     numeric code). CSV also works but `region_label` will just duplicate
     the raw `region` value — fine for Approach 1, not for Approach 2's
     region-name crosswalk.
3. Download and save the file as `raw/ess_extract.sav` (or `.csv`/`.dta`).

## Step 2 — get the SHDI extract

1. Register at <https://globaldatalab.org/register/> (free).
2. Go to **Human Development → Subnational HDI → Download**.
3. Select:
   - **Indicators**: `shdi`, `healthindex`, `edindex`, `incindex`, `lifexp`,
     `esch`, `msch`, `gnic` (all in `config.SHDI_INDICATORS`) — these mirror
     the composite + sub-component structure already used in
     `HappinessHDI.R`.
   - **Levels**: both "National" and "Subnational regions" (so
     `load_shdi_extract` gets levels 1 and 4 in the same file).
   - **Countries**: the ESS country set (`config.ESS_COUNTRY_ISO3`).
   - **Years**: 2002–2023 (matches `config.YEAR_MIN`/`YEAR_MAX`).
   - **Format**: CSV.
4. Save as `raw/shdi_subnational.csv`.

GDL's export headers have changed across versions; `io_utils.read_shdi_extract`
auto-detects common column-name variants and reshapes wide (year-per-column)
or long exports either way. If it raises a "could not find required column"
error, open the CSV, check the actual header names, and add them to
`col_aliases` in `io_utils.py`.

## Step 3 — national HDI (already have it)

Reuse `hdr-data.xlsx`, the same file `HappinessHDI.R` already loads. Copy or
symlink it into `raw/`.

## Step 4 — run the feasibility check

```bash
python ess_region_coverage.py raw/ess_extract.sav
python build_region_crosswalk.py raw/ess_extract.sav raw/shdi_subnational.csv
```

`ess_region_coverage.py` answers the concept note's questions 1–3: which
country-rounds have a usable `region` variable at all, and what NUTS level
it looks like. `build_region_crosswalk.py` answers 4–6: it fuzzy-matches
each ESS region's label against GDL's region names *within the same
country* and reports a match score for every pair.

Check `processed/region_crosswalk_review.csv` by hand — anything below the
0.6 similarity threshold (`MATCH_SCORE_THRESHOLD` in the script) lands
there instead of being auto-accepted. Common causes: transliteration
differences (e.g. diacritics), GDL splitting/merging regions relative to
current NUTS boundaries, or a country ESS didn't survey below the national
level. Add manual overrides directly to `region_crosswalk.csv` once you've
resolved them — the merge script just reads whatever's in that file.

The printed match-rate (matched regions / total ESS regions, and
respondents / total respondents once you run `merge_shdi_ess.py`) is the
number to report back before deciding, per the concept note, whether the
SHDI design is viable as the main paper or a national-HDI-only fallback is
needed.

## Step 5 — build the analysis files

```bash
# Approach 1
python merge_national_hdi_ess.py raw/ess_extract.sav raw/hdr-data.xlsx

# Approach 2 (needs the crosswalk from step 4)
python merge_shdi_ess.py raw/ess_extract.sav raw/shdi_subnational.csv processed/region_crosswalk.csv
```

Outputs land in `processed/`:
- `ess_with_national_hdi.csv` — one row per respondent, HDI composite +
  sub-components attached at the country level, matched to the nearest
  available HDI year for that respondent's ESS round.
- `ess_with_shdi.csv` — same idea, but region-level via the crosswalk.

Both scripts print a match-rate summary; anything with widespread
`hdi`/`shdi` == NaN points to a country-code mismatch worth checking before
moving on to modeling.

## Step 6 — the SDG trust series (the one source that *is* an open API)

Unlike ESS and GDL, the UN SDG Global Database is unauthenticated, so this
part is scripted end to end:

```bash
python pull_sdg_trust_series.py      # -> raw/sdg_trust_series_values.csv
python sdg_trust_cross_section.py    # -> processed/sdg_trust_cross_section.csv
```

`robust_all_for_figures.csv` carries fitted statistics only, which is enough to
say that 147 of 163 trust/satisfaction country-series have too few years for
the levels-and-differences design but not enough to run any other design on
them. The pull fetches the underlying values so the cross-sectional test is
possible; the API's coverage is much wider than the analysis file implies (156
countries for `SP_PSR_OSATIS_HLTH`, against 30 in the filtered results).

Two things the puller has to get right, both handled from the API's own
metadata rather than hardcoded: every series is returned broken out by sex,
age, location, quantile and more, and only the all-dimensions-total cell is the
national figure — each dimension declares its own total code, sdmx-tagged
`_T`, and series differ in which dimensions they carry (`VC_VOV_GDSD` adds
grounds of discrimination and education level). Regional and global aggregates
come back in the same response and are dropped by `Reporting Type`, then by
whether the M49 `geoAreaCode` resolves to an ISO3 country at all.

## Step 7 — the synthesis figures

Three builders sit outside `make_figures.py` because each answers one question
the deck asks and each reads a different mix of its outputs:

```bash
python domain_scorecard.py         # J1  three domains x five instruments
python specification_synthesis.py  # L1  the same domains under three specifications
```

`specification_synthesis.py` also computes the one cell the pipeline never
produced. G3 in `make_figures.py` runs development, social trust and self-rated
health within countries across regions, but not education — so the deck had
been quoting education's regional standing against a number no script
generated. `ess_regional_education()` computes it the same way G3 does (region
means, Pearson within each country with ≥6 matched regions) and it reproduces
the quoted +0.130 with 2 of 16 countries significant.

## Notes / known rough edges

- `merge_national_hdi_ess.py`'s `HDR_NAME_TO_ISO2` only covers HDR country
  names that don't map cleanly through `config.ESS_ISO2_TO_ISO3`. If a new
  HDR vintage adds/renames a country, extend that dict the same way
  `HappinessHDI.R`'s `hdr_to_whr_xwalk` does for the WHR side.
- `ESS_ROUND_YEAR` currently stops at round 11 (2023) — update it when a
  new round is fielded.
- Region matching is name-based (via `difflib`), not NUTS-code-based,
  because GDL's region codes (e.g. `DEUr101`) don't correspond to NUTS
  codes directly. If you want tighter matching, a Eurostat NUTS
  correspondence table could be added as an intermediate step, but for the
  feasibility check the name match should be enough to get a first read on
  coverage.
- Nothing in `raw/` or `processed/` is committed to git (see `.gitignore`)
  — ESS's terms don't permit redistributing microdata, so treat both
  directories as local-only.
