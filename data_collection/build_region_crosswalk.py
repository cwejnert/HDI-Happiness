"""
Feasibility check, step 4-6 (concept note, "Practical Feasibility Check"):

    4. Load SHDI regional data from Global Data Lab.
    5. Build a crosswalk between ESS regions and SHDI regions.
    6. Count how many country-round-region observations can be matched.

GDL region codes (e.g. "DEUr101") don't correspond to NUTS codes directly,
so the match is done on region *name* within country: ESS's region value
label (e.g. "Stuttgart") against GDL's region_name (e.g. "Baden-Wurttemberg
- Stuttgart"). Matching is fuzzy (difflib) because naming conventions
differ between the two sources; every match is scored so low-confidence
pairs can be reviewed by hand before being trusted.

    python build_region_crosswalk.py raw/ess_extract.csv raw/shdi_subnational.csv

Outputs:
    processed/region_crosswalk.csv        -- one row per matched ESS region
    processed/region_crosswalk_review.csv -- matches below the score threshold, for manual review
"""
from __future__ import annotations

import difflib
import sys
from pathlib import Path

import pandas as pd

from config import ESS_ISO2_TO_ISO3
from io_utils import read_ess_extract, read_shdi_extract

# Below this similarity score (0-1), a match is flagged for manual review
# rather than trusted automatically.
MATCH_SCORE_THRESHOLD = 0.6


def _normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    name = name.lower().strip()
    for junk in ["region", "province", "county", "oblast", "state", "-", "_", "'"]:
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
    if "region_label" not in ess_df.columns:
        raise ValueError("ESS extract has no 'region_label' -- re-run read_ess_extract on a .sav/.dta file with value labels, or supply labels manually.")

    subnational = shdi_df[shdi_df["level"] == 4].drop_duplicates(["iso3", "gdlcode", "region_name"])

    all_matches, all_review = [], []
    for cntry_code, grp in ess_df.groupby("cntry"):
        ess_regions = sorted(grp["region_label"].dropna().unique().tolist())
        if not ess_regions:
            continue

        iso3 = ESS_ISO2_TO_ISO3.get(cntry_code)
        gdl_regions_for_country = (
            subnational[subnational["iso3"] == iso3] if iso3 else subnational.iloc[0:0]
        )
        if gdl_regions_for_country.empty:
            no_match = pd.DataFrame({
                "ess_region_name": ess_regions,
                "gdl_region_name": None,
                "match_score": 0.0,
                "cntry": cntry_code,
                "reason": "no GDL subnational regions found for this country",
            })
            all_review.append(no_match)
            continue

        matches = match_region_names(ess_regions, gdl_regions_for_country["region_name"].unique().tolist())
        matches["cntry"] = cntry_code
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
        print(f"Usage: python {Path(__file__).name} <ess_extract.sav|.dta> <shdi_subnational.csv>")
        sys.exit(1)

    ess_path, shdi_path = sys.argv[1], sys.argv[2]
    ess_df = read_ess_extract(ess_path)
    shdi_df = read_shdi_extract(shdi_path)

    crosswalk, review = build_crosswalk(ess_df, shdi_df)

    out_dir = Path("processed")
    out_dir.mkdir(exist_ok=True)
    crosswalk.to_csv(out_dir / "region_crosswalk.csv", index=False)
    review.to_csv(out_dir / "region_crosswalk_review.csv", index=False)

    n_ess_regions = ess_df["region_label"].dropna().nunique() if "region_label" in ess_df else 0
    print(f"Matched {len(crosswalk)} / {n_ess_regions} distinct ESS regions to a GDL region "
          f"(score >= {MATCH_SCORE_THRESHOLD}).")
    print(f"{len(review)} pairs need manual review -> processed/region_crosswalk_review.csv")
    print(f"Confident matches -> processed/region_crosswalk.csv")


if __name__ == "__main__":
    main()
