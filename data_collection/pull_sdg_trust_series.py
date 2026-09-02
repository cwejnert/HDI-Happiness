"""
Pull the raw values behind the SDG framework's trust- and satisfaction-adjacent
series from the UN SDG Global Database API.

`robust_all_for_figures.csv` carries fitted statistics only, so the deck could
say how many country-series were testable in the time-series design (16 of 163)
but could not run any other design on them. This fetches the underlying values
so a CROSS-SECTIONAL test is possible: the four broad series have 22-30
countries at one year apiece, which is useless longitudinally and perfectly
usable across countries.

Only fully-aggregated cells are kept -- the API returns each series broken out
by sex, age, location, quantile, disability and population group, and a country
appears many times over. Anything less than the total-of-every-dimension cell
would be a subpopulation, not the national figure.

Output: raw/sdg_trust_series_values.csv  (long: series x country x year)
"""
from __future__ import annotations

import time

import pandas as pd
import requests

API = "https://unstats.un.org/sdgapi/v1/sdg/Series/Data"

# the 13 trust-, satisfaction- and integrity-adjacent series identified in the
# SDG results file; kept in one place so domain_scorecard.py and this agree
TRUST_SERIES = [
    "IU_DMK_INCL", "IU_COR_BRIB", "IC_FRM_BRIB", "SP_PSR_OSATIS_HLTH",
    "IU_DMK_ICRS", "SP_PSR_OSATIS_GOV", "SP_PSR_OSATIS_SEC",
    "SP_PSR_SATIS_GOV", "SP_PSR_SATIS_HLTH", "SP_PSR_OSATIS_PRM",
    "SP_PSR_SATIS_PRM", "SP_PSR_SATIS_SEC", "VC_VOV_GDSD",
]

# Reporting Type is a provenance flag (national / global / regional), not a
# population breakdown, so it has no total code and is handled separately
NOT_A_BREAKDOWN = {"Reporting Type"}


def total_codes(payload: dict) -> dict[str, str]:
    """Each dimension declares its own "no breakdown" code, sdmx-tagged _T.

    Series differ in which dimensions they carry -- VC_VOV_GDSD splits on
    grounds of discrimination and education level as well as the usual five --
    so read the total codes off the response rather than hardcoding them.
    """
    out = {}
    for dim in payload.get("dimensions", []):
        if dim["id"] in NOT_A_BREAKDOWN:
            continue
        tot = [c["code"] for c in dim["codes"] if c["sdmx"] == "_T"]
        if tot:
            out[dim["id"]] = tot[0]
    return out


def fetch_series(code: str, page_size: int = 2000) -> pd.DataFrame:
    """Page through one series. The API caps page size, so loop until done."""
    rows, page, totals = [], 1, {}
    while True:
        r = requests.get(API, params={"seriesCode": code, "pageSize": page_size,
                                      "page": page}, timeout=120)
        r.raise_for_status()
        payload = r.json()
        totals = totals or total_codes(payload)
        rows.extend(payload["data"])
        if page >= payload["totalPages"]:
            break
        page += 1
        time.sleep(0.3)

    if not rows:
        return pd.DataFrame()

    out = []
    for d in rows:
        dims = d.get("dimensions", {}) or {}
        # drop any cell that is a subpopulation on any dimension
        if any(dims.get(k) != code_ for k, code_ in totals.items()):
            continue
        out.append({
            "SeriesCode": d["series"],
            "SeriesDescription": d["seriesDescription"],
            "Goal": (d["goal"] or [None])[0],
            "geoAreaCode": d["geoAreaCode"],
            "GeoAreaName": d["geoAreaName"],
            "year": d["timePeriodStart"],
            "value": d["value"],
            "source": d.get("source"),
            "nature": (d.get("attributes") or {}).get("Nature"),
            "reporting_type": dims.get("Reporting Type"),
        })
    return pd.DataFrame(out)


def main():
    frames = []
    for code in TRUST_SERIES:
        df = fetch_series(code)
        print(f"{code:22s} {len(df):5d} total-cell rows  "
              f"{df.GeoAreaName.nunique() if len(df) else 0:4d} areas")
        frames.append(df)

    s = pd.concat([f for f in frames if len(f)], ignore_index=True)
    s["value"] = pd.to_numeric(s["value"], errors="coerce")
    s["year"] = pd.to_numeric(s["year"], errors="coerce").astype("Int64")
    s = s.dropna(subset=["value", "year"])

    # regional and global aggregates carry a geoAreaCode above the M49 country
    # range; countries are 1-899 in M49 but the API also emits groupings there,
    # so filter on reporting type instead, which marks them explicitly
    s = s[s.reporting_type.ne("R")]

    # a country-year can still appear twice when two producers report it (a
    # national survey and a cross-national one). Prefer the national figure;
    # average only when the tie is between like sources.
    s["_natl"] = s.reporting_type.eq("N")
    keep = s.sort_values("_natl", ascending=False).groupby(
        ["SeriesCode", "GeoAreaName", "year"], as_index=False).first()
    dupes = len(s) - len(keep)
    s = keep.drop(columns="_natl")
    print(f"\n{dupes} duplicate country-years resolved (national figure preferred)")

    out = "raw/sdg_trust_series_values.csv"
    s.to_csv(out, index=False)
    print(f"\nSaved: {out}  ({len(s):,} rows, "
          f"{s.GeoAreaName.nunique()} areas, {s.SeriesCode.nunique()} series)")
    print("\nSources (this matters -- a Gallup-sourced series is not "
          "independent of the WHR ladder):")
    print(s.groupby(["SeriesCode", "source"]).size().to_string())


if __name__ == "__main__":
    main()
