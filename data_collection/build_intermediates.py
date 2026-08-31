"""
Rebuild the intermediates that make_figures.py sections C, F and G read.

Sections A, B, D and E build their own panels. Sections C, F and G do not:
they read CSVs that no committed script produced, so an empty processed/
directory made the pipeline unrunnable past section B. This closes that gap.

Run after the merges, before make_figures.py:

    python merge_national_hdi_ess.py raw/ess_extract.sav raw/HDI_with_happiness.csv
    python merge_shdi_ess.py raw/ess_extract.sav raw/shdi_subnational.csv processed/region_crosswalk.csv
    python build_intermediates.py
    python make_figures.py

Needs raw/HDI_with_happiness.csv, raw/shdi_subnational.csv,
raw/robust_all_for_figures.csv and processed/ess_with_national_hdi.csv.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from config import ESS_ROUND_YEAR
from io_utils import read_shdi_extract

OUT = Path("processed")
OUT.mkdir(exist_ok=True)

HDI_INDS = ["hdi", "mys", "gnipc", "eys", "le"]

# SDG4's 35 official series, classified by what each one actually measures.
# Pooling them produces 3.3%, a figure that describes none of these constructs.
SDG4_CONSTRUCT = {
    "Access & Participation": {"SE_PRE_PARTN", "SE_ADT_EDUCTRN"},
    "Financing": {"DC_TOF_SCHIPSL"},
    "Attainment & Completion": {"SE_TOT_CPLR"},
    "Equity / Parity (ratio)": {
        "SE_GPI_PTNPRE", "SE_ADT_AGP_LITR", "SE_ADT_ALP_LITR", "SE_AGP_CPRA",
        "SE_ALP_CPLR", "SE_AWP_CPRA", "SE_GPI_ICTS", "SE_GPI_PART",
        "SE_GPI_TCAQ", "SE_TOT_GPI", "SE_TOT_RUPI", "SE_ADT_AWP_LITR",
        "SE_LGP_ACHI", "SE_NAP_ACHI", "SE_TOT_SESPI", "SE_IMP_FPOF",
        "SE_TOT_GPI_FS", "SE_TOT_SESPI_FS",
    },
    "Infrastructure & Inputs": {
        "SE_ACC_HNDWSH", "SE_ACS_CMPTR", "SE_ACS_ELECT", "SE_ACS_INTNT",
        "SE_INF_DSBL", "SE_ACS_H2O", "SE_ACS_SANIT",
    },
    "Quality & Learning Outcomes": {
        "SE_DEV_ONTRK", "SE_ADT_ACTS", "SE_ADT_LITR", "SE_TOT_PRFL",
        "SE_DEV_ONTRKWB", "SE_TRA_GRDL",
    },
}


def bh_fdr(pvals) -> np.ndarray:
    p = np.asarray(pvals, dtype=float)
    out = np.full(p.shape, np.nan)
    ok = ~np.isnan(p)
    m = int(ok.sum())
    if m == 0:
        return out
    order = np.argsort(p[ok])
    q = p[ok][order] * m / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    tmp = np.empty(m)
    tmp[order] = np.clip(q, 0, 1)
    out[ok] = tmp
    return out


def _p(x, y):
    ok = ~np.isnan(x) & ~np.isnan(y)
    if ok.sum() < 4 or np.std(x[ok]) == 0 or np.std(y[ok]) == 0:
        return np.nan, np.nan
    r, p = stats.pearsonr(x[ok], y[ok])
    return r * r, p


def hdi_wide() -> pd.DataFrame:
    d = pd.read_csv("raw/HDI_with_happiness.csv")
    w = d.pivot_table(index=["iso3", "year"], columns="indicatorCode", values="value").reset_index()
    hp = d.groupby(["iso3", "year"])["happiness"].mean().reset_index().rename(
        columns={"happiness": "whr_happiness"})
    return w.merge(hp, on=["iso3", "year"]).sort_values(["iso3", "year"])


def national_panel(w: pd.DataFrame):
    """Section C: UNDP HDI + GDL national SHDI + WHR happiness.

    NB GDL's national SHDI reproduces the UNDP HDI exactly -- it is derived
    from it -- so C2 comparing the two is a consistency check, not an
    independent replication. The subnational values are GDL's own.
    """
    sh = read_shdi_extract("raw/shdi_subnational.csv")
    nat = (sh[(sh.level == "National") & (sh.indicator == "shdi")]
           .groupby(["iso3", "year"])["value"].mean().reset_index()
           .rename(columns={"value": "shdi_national"}))
    panel = w.merge(nat, on=["iso3", "year"], how="inner")
    panel.to_csv(OUT / "national_hdi_shdi_whr_panel.csv", index=False)
    print(f"  national_hdi_shdi_whr_panel.csv      {len(panel):6d} rows, {panel.iso3.nunique()} countries")


def hdi_significance(w: pd.DataFrame):
    """Section F3: per-country HDI indicator significance, levels and diffs."""
    rows = []
    for iso, g in w.groupby("iso3"):
        g = g.sort_values("year")
        res = {}
        for i in HDI_INDS:
            x, y = g[i].to_numpy(float), g["whr_happiness"].to_numpy(float)
            res[i] = (_p(x, y), _p(np.diff(x), np.diff(y)))
        ql = bh_fdr([res[i][0][1] for i in HDI_INDS])
        qd = bh_fdr([res[i][1][1] for i in HDI_INDS])
        for k, i in enumerate(HDI_INDS):
            rows.append({
                "iso3": iso, "indicator": i,
                "r2_levels": res[i][0][0], "r2_diffs": res[i][1][0],
                "sig_levels_fdr": "q<.05" if ql[k] < 0.05 else "ns/NA",
                "sig_diffs_fdr": "q<.05" if (qd[k] == qd[k] and qd[k] < 0.05) else "ns/NA",
            })
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "hdi_country_indicator_significance.csv", index=False)
    s = out.groupby("indicator")["sig_levels_fdr"].apply(lambda x: (x == "q<.05").sum())
    print(f"  hdi_country_indicator_significance.csv  levels-significant: {s.to_dict()}")


def sdg_intermediates():
    """Sections F1, F2, F6 -- goal, SDG4-construct, and series-level rollups."""
    s = pd.read_csv("raw/robust_all_for_figures.csv", low_memory=False)
    s["sig"] = s.sig_levels_fdr.eq("q<.05")
    s["sigd"] = s.sig_diffs_fdr.eq("q<.05")

    g = s.groupby("Goal").agg(n_pairs=("sig", "size"), n_sig=("sig", "sum"),
                              n_series=("SeriesCode", "nunique")).reset_index()
    g["pct_sig_levels"] = (100 * g.n_sig / g.n_pairs).round(4)
    g.to_csv(OUT / "sdg_goal_significance_pooled.csv", index=False)
    print(f"  sdg_goal_significance_pooled.csv     {len(g)} goals, education = {g.loc[g.Goal == 4, 'pct_sig_levels'].iat[0]}%")

    lookup = {c: name for name, codes in SDG4_CONSTRUCT.items() for c in codes}
    e = s[s.Goal == 4].copy()
    e["edu_category"] = e.SeriesCode.map(lookup)
    missing = sorted(e.loc[e.edu_category.isna(), "SeriesCode"].unique())
    if missing:
        raise SystemExit(f"Unclassified SDG4 series -- add them to SDG4_CONSTRUCT: {missing}")
    c = e.groupby("edu_category").agg(n_pairs=("sig", "size"), n_sig=("sig", "sum"),
                                      n_series=("SeriesCode", "nunique")).reset_index()
    c["pct_sig_levels"] = (100 * c.n_sig / c.n_pairs).round(4)
    c.to_csv(OUT / "sdg_education_category_significance.csv", index=False)
    print(f"  sdg_education_category_significance.csv  access = "
          f"{c.loc[c.edu_category == 'Access & Participation', 'pct_sig_levels'].iat[0]}%")

    rank = (s.groupby(["SeriesCode", "SeriesDescription", "Goal"])
              .agg(n_countries=("sig", "size"), n_sig_levels=("sig", "sum"),
                   n_sig_diffs=("sigd", "sum")).reset_index())
    rank["pct_sig_levels"] = (100 * rank.n_sig_levels / rank.n_countries).round(4)
    rank["pct_sig_diffs"] = (100 * rank.n_sig_diffs / rank.n_countries).round(4)
    rank.to_csv(OUT / "sdg_series_significance_ranking.csv", index=False)
    print(f"  sdg_series_significance_ranking.csv  {len(rank)} series, "
          f"{(rank.n_countries >= 8).sum()} rankable, {(rank.n_sig_diffs > 0).sum()} with any diffs signal")


def ess_education():
    """Sections F4, F5 -- individual-level education and the country aggregate."""
    d = pd.read_csv("processed/ess_with_national_hdi.csv", low_memory=False)

    rows = []
    for c, g in d.groupby("cntry"):
        for edu in ["eisced", "eduyrs"]:
            for outcome in ["stflife", "happy"]:
                sub = g.dropna(subset=[edu, outcome])
                if len(sub) < 50:
                    rows.append({"cntry": c, "edu_var": edu, "outcome": outcome,
                                 "r2": None, "p": None, "n": len(sub)})
                    continue
                r, p = stats.pearsonr(sub[edu], sub[outcome])
                rows.append({"cntry": c, "edu_var": edu, "outcome": outcome,
                             "r2": r * r, "p": p, "n": len(sub)})
    ind = pd.DataFrame(rows)
    ind.to_csv(OUT / "ess_individual_education_by_country.csv", index=False)
    n = ind[(ind.edu_var == "eisced") & (ind.outcome == "stflife")].dropna(subset=["r2"])
    print(f"  ess_individual_education_by_country.csv  eisced x stflife significant in "
          f"{int((n.p < 0.05).sum())}/{len(n)} countries")

    d["year"] = d["essround"].map(ESS_ROUND_YEAR)
    ce = (d.groupby(["cntry", "essround", "year"])
            .agg(mean_eisced=("eisced", "mean"), mean_eduyrs=("eduyrs", "mean"),
                 whr_happiness=("whr_happiness", "mean"), mys=("mys", "mean"),
                 eys=("eys", "mean"))
            .reset_index().dropna(subset=["whr_happiness"]))
    ce.to_csv(OUT / "ess_country_education_panel.csv", index=False)
    m = ce[["mean_eduyrs", "whr_happiness", "mys"]].dropna()
    r_ess = stats.pearsonr(m.mean_eduyrs, m.whr_happiness)[0] ** 2
    r_hdi = stats.pearsonr(m.mys, m.whr_happiness)[0] ** 2
    print(f"  ess_country_education_panel.csv      {len(ce)} country-rounds; "
          f"ESS schooling R2={r_ess:.3f} vs HDI mys R2={r_hdi:.3f} on the same cells")


def main():
    print("Rebuilding make_figures.py intermediates:")
    w = hdi_wide()
    national_panel(w)
    hdi_significance(w)
    sdg_intermediates()
    ess_education()
    print("Done. make_figures.py can now run end to end.")


if __name__ == "__main__":
    main()
