"""
Feasibility check, step 4-6 (concept note, "Practical Feasibility Check"):

    4. Load SHDI regional data from Global Data Lab.
    5. Build a crosswalk between ESS regions and SHDI regions.
    6. Count how many country-round-region observations can be matched.

Confirmed against a real ESS export (2026-07): the 'region' variable is a
genuine NUTS code (e.g. "DE1", "FR71"), not a labeled name -- CSV exports
from the Data Builder don't carry value labels. GDL region codes (e.g.
"DEUr101") don't correspond to NUTS codes directly, though, so the actual
match still has to happen on region *name*. This script bridges the gap in
two steps:

    1. NUTS code -> name, via reference/nuts_all_vintages_names.csv (built
       from Eurostat's NUTS 2003-2021 correspondence tables, since ESS
       rounds span multiple NUTS revisions and a region's code can change
       vintage to vintage while GDL keeps using whichever name it settled
       on). Non-EU ESS countries (Norway, Russia, Ukraine, etc.) use their
       own regional coding, not Eurostat NUTS, and won't resolve here --
       they show up in the review file for manual handling.
    2. name -> GDL region name, fuzzy-matched (difflib) within country,
       same as before.

    python build_region_crosswalk.py raw/ess_extract.csv raw/shdi_subnational.csv

Outputs:
    processed/region_crosswalk.csv        -- one row per matched ESS region code
    processed/region_crosswalk_review.csv -- unresolved / low-confidence pairs, for manual review
"""
from __future__ import annotations

import difflib
import sys
import unicodedata
from pathlib import Path

import pandas as pd

from config import ESS_ISO2_TO_ISO3, SHDI_LEVEL_SUBNATIONAL
from io_utils import read_ess_extract, read_shdi_extract

# Below this similarity score (0-1), a match is flagged for manual review
# rather than trusted automatically.
MATCH_SCORE_THRESHOLD = 0.6

NUTS_LOOKUP_PATH = Path(__file__).parent / "reference" / "nuts_all_vintages_names.csv"


def load_nuts_lookup() -> dict[str, str]:
    nuts = pd.read_csv(NUTS_LOOKUP_PATH)
    return dict(zip(nuts["nuts_code"], nuts["name"]))


def _normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    # Strip diacritics (e.g. "Šiaulių" -> "Siauliu") so cross-language
    # spelling differences don't tank the similarity score, then drop
    # generic administrative-unit words that show up on one side but not
    # the other (English "county"/"province" vs. e.g. Lithuanian
    # "apskritis", Slavic "kraj"/"zupanija", Nordic "lan").
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = name.lower().strip()
    for junk in ["region", "province", "county", "oblast", "state", "district",
                 "apskritis", "kraj", "zupanija", "zupanijos", "lan", "county of",
                 "-", "_", "'"]:
        name = name.replace(junk, " ")
    return " ".join(name.split())


def match_region_names(ess_names: list[str], gdl_names: list[str]) -> pd.DataFrame:
    """For each ESS region name, find the best-scoring GDL region name."""
    gdl_norm = {g: _normalize_name(g) for g in gdl_names}
    rows = []
    for ess_name in ess_names:
        ess_norm = _normalize_name(ess_name)
        best_gdl, best_score = None, 0.0
        for gdl_name, gdl_n in gdl_norm.items():
            score = difflib.SequenceMatcher(None, ess_norm, gdl_n).ratio()
            if score > best_score:
                best_gdl, best_score = gdl_name, score
        rows.append({"ess_region_name": ess_name, "gdl_region_name": best_gdl,
                     "match_score": round(best_score, 3)})
    return pd.DataFrame(rows)


def build_crosswalk(ess_df: pd.DataFrame, shdi_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if "region" not in ess_df.columns:
        raise ValueError("ESS extract has no 'region' column -- re-export with the regional identifier included.")

    nuts_lookup = load_nuts_lookup()
    subnational = shdi_df[shdi_df["level"] == SHDI_LEVEL_SUBNATIONAL].drop_duplicates(["iso3", "gdlcode", "region_name"])

    ess_regions = (
        ess_df[["cntry", "region"]].dropna().drop_duplicates()
        .rename(columns={"region": "ess_region_code"})
    )
    ess_regions["ess_region_name"] = ess_regions["ess_region_code"].map(nuts_lookup)

    all_matches, all_review = [], []
    for cntry_code, grp in ess_regions.groupby("cntry"):
        unresolved = grp[grp["ess_region_name"].isna()]
        if not unresolved.empty:
            rev = unresolved.copy()
            rev["gdl_region_name"] = None
            rev["match_score"] = 0.0
            rev["reason"] = "NUTS code not found (likely a non-EU ESS country with its own regional coding)"
            all_review.append(rev)

        resolved = grp[grp["ess_region_name"].notna()]
        if resolved.empty:
            continue

        iso3 = ESS_ISO2_TO_ISO3.get(cntry_code)
        gdl_regions_for_country = (
            subnational[subnational["iso3"] == iso3] if iso3 else subnational.iloc[0:0]
        )
        if gdl_regions_for_country.empty:
            rev = resolved.copy()
            rev["gdl_region_name"] = None
            rev["match_score"] = 0.0
            rev["reason"] = "no GDL subnational regions found for this country"
            all_review.append(rev)
            continue

        matches = match_region_names(resolved["ess_region_name"].tolist(), gdl_regions_for_country["region_name"].unique().tolist())
        matches["cntry"] = cntry_code
        matches["ess_region_code"] = resolved["ess_region_code"].tolist()
        good = matches[matches["match_score"] >= MATCH_SCORE_THRESHOLD]
        low = matches[matches["match_score"] < MATCH_SCORE_THRESHOLD]
        all_matches.append(good)
        if not low.empty:
            low = low.copy()
            low["reason"] = "match score below threshold"
            all_review.append(low)

    crosswalk = pd.concat(all_matches, ignore_index=True) if all_matches else pd.DataFrame()
    review = pd.concat(all_review, ignore_index=True) if all_review else pd.DataFrame()
    return crosswalk, review


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {Path(__file__).name} <ess_extract> <shdi_subnational.csv>")
        sys.exit(1)

    ess_path, shdi_path = sys.argv[1], sys.argv[2]
    ess_df = read_ess_extract(ess_path)
    shdi_df = read_shdi_extract(shdi_path)

    crosswalk, review = build_crosswalk(ess_df, shdi_df)

    out_dir = Path("processed")
    out_dir.mkdir(exist_ok=True)
    crosswalk.to_csv(out_dir / "region_crosswalk.csv", index=False)
    review.to_csv(out_dir / "region_crosswalk_review.csv", index=False)

    n_ess_regions = ess_df["region"].nunique()
    print(f"Matched {len(crosswalk)} / {n_ess_regions} distinct ESS region codes to a GDL region "
          f"(score >= {MATCH_SCORE_THRESHOLD}).")
    print(f"{len(review)} pairs need manual review -> processed/region_crosswalk_review.csv")
    print(f"Confident matches -> processed/region_crosswalk.csv")


if __name__ == "__main__":
    main()
