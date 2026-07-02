"""
Approach 1 (concept note): ESS respondents + national HDI.

Reuses the HDR data you already have (hdr-data.xlsx, same file as
HappinessHDI.R) and merges it onto the ESS extract at the country-year
level: each respondent gets the HDI value (composite + sub-components) for
their country in the year closest to their ESS round's fieldwork year.

    python merge_national_hdi_ess.py raw/ess_extract.csv raw/hdr-data.xlsx

Output: processed/ess_with_national_hdi.csv
    One row per ESS respondent, with hdi/le/eys/mys/gnipc columns attached.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from config import ESS_ISO2_TO_ISO3, ESS_ROUND_YEAR, HDI_COMPOSITE, HDI_SUBCOMPS
from io_utils import read_ess_extract

# HDR's countryIsoCode is ISO3; ESS's 'cntry' is ISO2. Reuse the ESS ISO2->ISO3
# map from config.py (inverted) rather than a lossy 2-letter substring guess.
HDR_ISO3_TO_ISO2 = {v: k for k, v in ESS_ISO2_TO_ISO3.items()}
# A few HDR country names use non-standard codes that need spelling out
# explicitly (mirrors HappinessHDI.R's hdr_to_whr_xwalk fixes).
HDR_NAME_TO_ISO2 = {
    "Turkiye": "TR", "Russian Federation": "RU", "Czechia": "CZ",
    "Moldova (Republic of)": "MD", "Korea (Republic of)": "KR",
    "Hong Kong, China (SAR)": "HK", "Palestine, State of": "PS",
}


def load_hdr(hdr_path: str | Path) -> pd.DataFrame:
    hdr = pd.read_excel(hdr_path, sheet_name="Data")
    hdr = hdr[hdr["indicatorCode"] != "hdi_rank"].copy()
    hdr = hdr[hdr["indicatorCode"].isin([HDI_COMPOSITE] + HDI_SUBCOMPS)]
    hdr = hdr.dropna(subset=["value"])
    hdr["year"] = hdr["year"].astype(int)

    hdr["iso2"] = hdr["country"].map(HDR_NAME_TO_ISO2)
    hdr["iso2"] = hdr["iso2"].fillna(hdr["countryIsoCode"].map(HDR_ISO3_TO_ISO2))

    wide = hdr.pivot_table(
        index=["iso2", "year"], columns="indicatorCode", values="value", aggfunc="mean"
    ).reset_index()
    return wide


def nearest_year_merge(ess: pd.DataFrame, hdr_wide: pd.DataFrame) -> pd.DataFrame:
    ess = ess.copy()
    ess["hdi_match_year"] = ess["essround"].map(ESS_ROUND_YEAR)

    merged_parts = []
    for iso2, ess_grp in ess.groupby("cntry"):
        hdr_grp = hdr_wide[hdr_wide["iso2"] == iso2]
        if hdr_grp.empty:
            ess_grp = ess_grp.copy()
            for col in [HDI_COMPOSITE] + HDI_SUBCOMPS:
                ess_grp[col] = pd.NA
            ess_grp["hdi_year_used"] = pd.NA
            merged_parts.append(ess_grp)
            continue

        hdr_years = hdr_grp["year"].to_numpy()
        ess_grp = ess_grp.copy()
        nearest_idx = ess_grp["hdi_match_year"].apply(
            lambda y: (abs(hdr_years - y)).argmin() if pd.notna(y) else None
        )
        matched_years = nearest_idx.map(
            lambda i: hdr_years[i] if i is not None else None
        )
        ess_grp["hdi_year_used"] = matched_years
        ess_grp = ess_grp.merge(
            hdr_grp.rename(columns={"year": "hdi_year_used"}),
            left_on=["cntry", "hdi_year_used"],
            right_on=["iso2", "hdi_year_used"],
            how="left",
        )
        merged_parts.append(ess_grp)

    return pd.concat(merged_parts, ignore_index=True)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {Path(__file__).name} <ess_extract.csv|.sav|.dta> <hdr-data.xlsx>")
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
        print(f"Countries with no HDI match (check HDR_NAME_TO_ISO2 / country coverage): {unmatched_countries}")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
