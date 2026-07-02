"""
Readers for the two gated source files (ESS extract, GDL SHDI export).

Both ESS and Global Data Lab require a free account and a manual export
through their web UI before any file exists locally (see README.md for the
exact click-path). These functions only deal with what happens *after* that
file lands on disk: autodetecting format and normalizing column names, since
neither provider's export schema is guaranteed to stay fixed.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from config import ESS_ALL_VARIABLES


def read_ess_extract(path: str | Path) -> pd.DataFrame:
    """
    Load an ESS Data Builder export (.csv, .dta, or .sav) and return a
    DataFrame restricted to the variables in config.ESS_ALL_VARIABLES that
    are actually present.

    For SPSS (.sav) and Stata (.dta) files, value labels are applied to the
    'region' column specifically (kept alongside the raw numeric/string
    code as 'region_label') because ESS's regional codes are only
    interpretable as NUTS units through their labels, and GDL region
    matching in build_region_crosswalk.py needs the human-readable name.
    """
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(path, low_memory=False)
        df.columns = [c.strip().lower() for c in df.columns]
        if "region" in df.columns:
            df["region_label"] = df["region"]

    elif suffix in (".sav", ".dta"):
        import pyreadstat

        reader = pyreadstat.read_sav if suffix == ".sav" else pyreadstat.read_dta
        df_codes, meta = reader(str(path), apply_value_formats=False)
        df_labels, _ = reader(str(path), apply_value_formats=True)
        df_codes.columns = [c.strip().lower() for c in df_codes.columns]
        df_labels.columns = [c.strip().lower() for c in df_labels.columns]
        df = df_codes
        if "region" in df.columns:
            df["region_label"] = df_labels["region"]

    else:
        raise ValueError(
            f"Unrecognized ESS export format '{suffix}'. "
            "Expected .csv, .sav, or .dta from the ESS Data Builder."
        )

    keep = [c for c in ESS_ALL_VARIABLES if c in df.columns]
    keep += [c for c in ("region_label",) if c in df.columns and c not in keep]
    missing = sorted(set(ESS_ALL_VARIABLES) - set(df.columns))
    if missing:
        print(
            f"[read_ess_extract] {len(missing)} requested variables not found "
            f"in export (likely not selected in the Data Builder): {missing}"
        )
    return df[keep].copy()


def read_shdi_extract(path: str | Path) -> pd.DataFrame:
    """
    Load a Global Data Lab SHDI export and return a long-format DataFrame:
    iso3, country, gdlcode, region_name, level, year, indicator, value.

    Confirmed against a real export (2026-07): GDL's CSV is already
    long-by-year (one row per region-year, a 'Year' column, 'Level' as text
    -- "National" / "Subnat", not a numeric code) with one column per
    selected indicator (e.g. just 'shdi' if that's all you picked). Column
    names are matched case-insensitively against the aliases below, and
    anything left over after resolving the id columns is treated as an
    indicator column and melted to long -- so this also handles a
    multi-indicator export (shdi, healthindex, edindex, ... side by side)
    without changes.
    """
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path, low_memory=False)
    df.columns = [c.strip() for c in df.columns]

    col_aliases = {
        "iso3": ["iso_code", "iso3", "iso3_code", "isocode"],
        "country": ["country", "countryname"],
        "continent": ["continent"],
        "gdlcode": ["gdlcode", "gdl_code", "region_code"],
        "region_name": ["region", "regname", "region_name"],
        "level": ["level"],
        "year": ["year"],
    }

    def find_col(aliases):
        lower_map = {c.lower(): c for c in df.columns}
        for a in aliases:
            if a in lower_map:
                return lower_map[a]
        return None

    resolved = {k: find_col(v) for k, v in col_aliases.items()}
    missing_required = [k for k in ("iso3", "gdlcode") if resolved[k] is None]
    if missing_required:
        raise ValueError(
            f"Could not find required column(s) {missing_required} in "
            f"{path.name}. Actual columns: {list(df.columns)}. "
            "Update col_aliases in io_utils.read_shdi_extract() to match."
        )

    rename = {v: k for k, v in resolved.items() if v is not None}
    df = df.rename(columns=rename)

    id_cols_present = [c for c in ("iso3", "country", "continent", "gdlcode", "region_name", "level", "year") if c in df.columns]

    if "year" in df.columns:
        # Already long-by-year: whatever's left besides the id columns is
        # one-or-more indicator value columns (e.g. 'shdi', 'healthindex').
        indicator_cols = [c for c in df.columns if c not in id_cols_present]
        if not indicator_cols:
            raise ValueError(f"No indicator value column found in {path.name}. Actual columns: {list(df.columns)}")
        long = df.melt(id_vars=id_cols_present, value_vars=indicator_cols,
                        var_name="indicator", value_name="value")
        long["year"] = long["year"].astype(int)
    else:
        # Wide-by-year (one column per year): older/alternate GDL export style.
        year_cols = [c for c in df.columns if re.fullmatch(r"(19|20)\d{2}", str(c))]
        if not year_cols:
            raise ValueError(
                f"Could not detect a 'Year' column or year-named columns in {path.name}. "
                f"Actual columns: {list(df.columns)}"
            )
        id_vars = [c for c in df.columns if c not in year_cols]
        long = df.melt(id_vars=id_vars, value_vars=year_cols,
                        var_name="year", value_name="value")
        long["year"] = long["year"].astype(int)
        if "indicator" not in long.columns:
            long["indicator"] = path.stem

    keep = ["iso3", "country", "gdlcode", "region_name", "level", "year", "indicator", "value"]
    for c in keep:
        if c not in long.columns:
            long[c] = pd.NA
    long["indicator"] = long["indicator"].str.lower()
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    return long[keep]
