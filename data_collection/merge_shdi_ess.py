"""
Approach 2 (concept note): ESS respondents + Subnational HDI (SHDI).

Uses the crosswalk built by build_region_crosswalk.py to attach GDL's
region code to each ESS respondent, then merges the SHDI panel (composite +
health/education/income dimension indices) at the region-year level,
matching each ESS round's fieldwork year to the nearest available SHDI year.

    python merge_shdi_ess.py raw/ess_extract.sav raw/shdi_subnational.csv processed/region_crosswalk.csv

Output: processed/ess_with_shdi.csv
    One row per ESS respondent with a crosswalk match, with shdi/healthindex/
    edindex/incindex/lifexp/esch/msch/gnic columns attached, plus 'cntry' kept
    for the country fixed effects the concept note's Model 1 calls for.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from config import ESS_ISO2_TO_ISO3, ESS_ROUND_YEAR, SHDI_INDICATORS, SHDI_LEVEL_SUBNATIONAL
from io_utils import read_ess_extract, read_shdi_extract


def main():
    if len(sys.argv) != 4:
        print(f"Usage: python {Path(__file__).name} <ess_extract> <shdi_subnational.csv> <region_crosswalk.csv>")
        sys.exit(1)

    ess_path, shdi_path, crosswalk_path = sys.argv[1], sys.argv[2], sys.argv[3]

    ess = read_ess_extract(ess_path)
    shdi = read_shdi_extract(shdi_path)
    crosswalk = pd.read_csv(crosswalk_path)

    if "region" not in ess.columns:
        raise ValueError("ESS extract has no 'region' column; re-export with the regional identifier included.")

    ess["iso3"] = ess["cntry"].map(ESS_ISO2_TO_ISO3)
    ess = ess.merge(
        crosswalk[["cntry", "ess_region_code", "ess_region_name", "gdl_region_name", "match_score"]],
        left_on=["cntry", "region"], right_on=["cntry", "ess_region_code"], how="left",
    )
    ess["shdi_match_year"] = ess["essround"].map(ESS_ROUND_YEAR)

    shdi_sub = shdi[(shdi["level"] == SHDI_LEVEL_SUBNATIONAL) & (shdi["indicator"].isin(SHDI_INDICATORS))]
    shdi_wide = shdi_sub.pivot_table(
        index=["iso3", "region_name", "year"], columns="indicator", values="value", aggfunc="mean"
    ).reset_index()

    # Several GDL region names recur across countries (e.g. "Central", "North"),
    # so every lookup below is scoped by iso3 as well as region_name -- matching
    # on name alone would silently fan-out the merge across unrelated countries.
    merged_parts = []
    for (iso3, region), grp in ess.groupby(["iso3", "gdl_region_name"], dropna=False):
        if pd.isna(region):
            grp = grp.copy()
            for ind in SHDI_INDICATORS:
                grp[ind] = pd.NA
            grp["shdi_year_used"] = pd.NA
            merged_parts.append(grp)
            continue

        region_shdi = shdi_wide[(shdi_wide["iso3"] == iso3) & (shdi_wide["region_name"] == region)]
        if region_shdi.empty:
            grp = grp.copy()
            for ind in SHDI_INDICATORS:
                grp[ind] = pd.NA
            grp["shdi_year_used"] = pd.NA
            merged_parts.append(grp)
            continue

        years_arr = region_shdi["year"].to_numpy()
        grp = grp.copy()
        grp["shdi_year_used"] = grp["shdi_match_year"].apply(
            lambda y: years_arr[(abs(years_arr - y)).argmin()] if pd.notna(y) else None
        )
        grp = grp.merge(
            region_shdi.drop(columns=["iso3", "region_name"]).rename(columns={"year": "shdi_year_used"}),
            on="shdi_year_used", how="left", suffixes=("", "_shdi"),
        )
        merged_parts.append(grp)

    merged = pd.concat(merged_parts, ignore_index=True)

    out_path = Path("processed") / "ess_with_shdi.csv"
    out_path.parent.mkdir(exist_ok=True)
    merged.to_csv(out_path, index=False)

    n_total = len(merged)
    n_region_matched = merged["gdl_region_name"].notna().sum()
    n_value_matched = merged["shdi"].notna().sum() if "shdi" in merged else 0
    print(f"Region crosswalk matched: {n_region_matched} / {n_total} respondents.")
    print(f"SHDI value attached:      {n_value_matched} / {n_total} respondents.")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
