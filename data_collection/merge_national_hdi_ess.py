"""
Approach 1 (concept note): ESS respondents + national HDI.

Accepts either:
  - HDI_with_happiness.csv -- the country-year panel HappinessHDI.R already
    produces (country, iso3, year, indicatorCode, indicator, value,
    happiness), long format. Preferred: it carries iso3 directly, so no
    country-name guessing is needed, and it comes with the WHR Cantril
    Ladder happiness score as a bonus column for comparing against ESS's
    own stflife/happy.
  - hdr-data.xlsx -- the raw HDR file (same one HappinessHDI.R reads from
    scratch), if you'd rather not depend on the R script's output.

Either way, each ESS respondent gets the HDI value (composite + sub-
components) for their country in the year closest to their ESS round's
fieldwork year.

    python merge_national_hdi_ess.py raw/ess_extract.csv raw/HDI_with_happiness.csv

Output: processed/ess_with_national_hdi.csv
    One row per ESS respondent, with hdi/le/eys/mys/gnipc (+ whr_happiness
    if available) columns attached.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from config import ESS_ISO2_TO_ISO3, ESS_ROUND_YEAR, HDI_COMPOSITE, HDI_SUBCOMPS
from io_utils import read_ess_extract

ESS_ISO3_TO_ISO2 = {v: k for k, v in ESS_ISO2_TO_ISO3.items()}

# A few HDR country names don't resolve through ISO3 cleanly and need
# spelling out explicitly (mirrors HappinessHDI.R's hdr_to_whr_xwalk fixes) --
# only used on the raw hdr-data.xlsx path, where iso3 sometimes needs a
# name-based override.
HDR_NAME_TO_ISO3 = {
    "Turkiye": "TUR", "Russian Federation": "RUS", "Czechia": "CZE",
    "Moldova (Republic of)": "MDA", "Korea (Republic of)": "KOR",
}


def load_hdr(hdr_path: str | Path) -> pd.DataFrame:
    """Load either HDI_with_happiness.csv or raw hdr-data.xlsx; return a
    wide iso3-year panel with hdi/le/eys/mys/gnipc (+ whr_happiness if present)."""
    hdr_path = Path(hdr_path)

    if hdr_path.suffix.lower() == ".xlsx":
        hdr = pd.read_excel(hdr_path, sheet_name="Data")
        hdr = hdr[hdr["indicatorCode"] != "hdi_rank"].copy()
        hdr["iso3"] = hdr["country"].map(HDR_NAME_TO_ISO3).fillna(hdr["countryIsoCode"])
        happiness_col = None
    else:
        hdr = pd.read_csv(hdr_path)
        happiness_col = "happiness" if "happiness" in hdr.columns else None

    hdr = hdr[hdr["indicatorCode"].isin([HDI_COMPOSITE] + HDI_SUBCOMPS)].dropna(subset=["value"]).copy()
    hdr["year"] = hdr["year"].astype(int)

    wide = hdr.pivot_table(
        index=["iso3", "year"], columns="indicatorCode", values="value", aggfunc="mean"
    ).reset_index()

    if happiness_col:
        happy = hdr.groupby(["iso3", "year"])[happiness_col].mean().reset_index()
        happy = happy.rename(columns={happiness_col: "whr_happiness"})
        wide = wide.merge(happy, on=["iso3", "year"], how="left")

    return wide


def nearest_year_merge(ess: pd.DataFrame, hdr_wide: pd.DataFrame) -> pd.DataFrame:
    ess = ess.copy()
    ess["iso3"] = ess["cntry"].map(ESS_ISO2_TO_ISO3)
    ess["hdi_match_year"] = ess["essround"].map(ESS_ROUND_YEAR)

    value_cols = [c for c in ([HDI_COMPOSITE] + HDI_SUBCOMPS + ["whr_happiness"]) if c in hdr_wide.columns]

    merged_parts = []
    for iso3, ess_grp in ess.groupby("iso3"):
        hdr_grp = hdr_wide[hdr_wide["iso3"] == iso3]
        ess_grp = ess_grp.copy()
        if hdr_grp.empty:
            for col in value_cols:
                ess_grp[col] = pd.NA
            ess_grp["hdi_year_used"] = pd.NA
            merged_parts.append(ess_grp)
            continue

        hdr_years = hdr_grp["year"].to_numpy()
        nearest_idx = ess_grp["hdi_match_year"].apply(
            lambda y: (abs(hdr_years - y)).argmin() if pd.notna(y) else None
        )
        ess_grp["hdi_year_used"] = nearest_idx.map(lambda i: hdr_years[i] if i is not None else None)
        ess_grp = ess_grp.merge(
            hdr_grp.rename(columns={"year": "hdi_year_used"}),
            on=["iso3", "hdi_year_used"], how="left",
        )
        merged_parts.append(ess_grp)

    return pd.concat(merged_parts, ignore_index=True)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {Path(__file__).name} <ess_extract.csv|.sav|.dta> <HDI_with_happiness.csv|hdr-data.xlsx>")
        sys.exit(1)

    ess_path, hdr_path = sys.argv[1], sys.argv[2]
    ess = read_ess_extract(ess_path)
    hdr_wide = load_hdr(hdr_path)

    merged = nearest_year_merge(ess, hdr_wide)

    out_path = Path("processed") / "ess_with_national_hdi.csv"
    out_path.parent.mkdir(exist_ok=True)
    merged.to_csv(out_path, index=False)

    n_matched = merged[HDI_COMPOSITE].notna().sum() if HDI_COMPOSITE in merged else 0
    print(f"{n_matched} / {len(merged)} respondents matched to a national HDI value.")
    unmatched_countries = sorted(merged.loc[merged[HDI_COMPOSITE].isna(), "cntry"].unique()) if HDI_COMPOSITE in merged else []
    if unmatched_countries:
        print(f"Countries with no HDI match (check ESS_ISO2_TO_ISO3 / HDR country coverage): {unmatched_countries}")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
