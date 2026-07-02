"""
Feasibility check, step 1-3 (concept note, "Practical Feasibility Check"):

    1. Identify available ESS regional variables.
    2. Determine whether public ESS data include usable regional
       identifiers for each country-round.
    3. Infer whether ESS regional identifiers correspond to NUTS1, NUTS2,
       or NUTS3 (or are absent / country-only).

Run after exporting an ESS extract with `region` included (see README.md).

    python ess_region_coverage.py raw/ess_extract.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from io_utils import read_ess_extract

# ESS 'region' codes are (almost always) NUTS codes: 2-letter country
# prefix + digits/letters. NUTS level = number of characters after the
# 2-letter prefix (NUTS0 = country only, NUTS1 = 1 char, NUTS2 = 2 chars,
# NUTS3 = 3 chars). Some countries report non-NUTS national codes instead
# (flagged as "non_nuts" below) -- inspect these manually.
def infer_nuts_level(code: str) -> str:
    if not isinstance(code, str) or len(code) < 2:
        return "missing"
    prefix, rest = code[:2], code[2:]
    if not prefix.isalpha():
        return "non_nuts"
    if rest == "":
        return "NUTS0 (country only)"
    if rest.isalnum() and len(rest) in (1, 2, 3):
        return f"NUTS{len(rest)}"
    return "non_nuts"


def build_coverage_report(df: pd.DataFrame) -> pd.DataFrame:
    if "region" not in df.columns:
        raise ValueError(
            "'region' not present in the ESS extract. Re-export from the "
            "Data Builder with the regional identifier variable included."
        )

    work = df.copy()
    work["region_str"] = work["region"].astype(str).str.strip()
    work.loc[work["region_str"].isin(["nan", "", "None"]), "region_str"] = pd.NA
    work["nuts_level"] = work["region_str"].apply(infer_nuts_level)

    report = (
        work.groupby(["cntry", "essround"])
        .agg(
            n_respondents=("region_str", "size"),
            n_with_region=("region_str", lambda s: s.notna().sum()),
            n_distinct_regions=("region_str", lambda s: s.dropna().nunique()),
            nuts_levels_seen=("nuts_level", lambda s: ", ".join(sorted(set(s.dropna())))),
        )
        .reset_index()
    )
    report["pct_with_region"] = (
        100 * report["n_with_region"] / report["n_respondents"]
    ).round(1)
    return report.sort_values(["cntry", "essround"])


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <ess_extract.csv|.sav|.dta>")
        sys.exit(1)

    ess_path = sys.argv[1]
    df = read_ess_extract(ess_path)
    report = build_coverage_report(df)

    out_path = Path("processed") / "ess_region_coverage.csv"
    out_path.parent.mkdir(exist_ok=True)
    report.to_csv(out_path, index=False)

    print(f"\n=== ESS regional identifier coverage ({len(report)} country-round cells) ===")
    print(report.to_string(index=False))
    print(f"\nSaved: {out_path}")

    usable = report[report["pct_with_region"] > 0]
    print(
        f"\n{len(usable)} / {len(report)} country-round cells have any "
        f"regional identifier at all. Country-rounds with 0% coverage cannot "
        f"be used in the SHDI (Approach 2) design and fall back to national "
        f"HDI (Approach 1) only."
    )


if __name__ == "__main__":
    main()
