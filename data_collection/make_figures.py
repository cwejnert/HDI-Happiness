"""
Diagnostic figures for the ESS x HDI/SHDI wellbeing expansion.

Mirrors the analytic structure of HappinessHDI.R -- per-country-indicator
OLS in levels and first-differences, the "collapse" between them, FDR-style
significance framing, heatmaps, dumbbell charts, quadrant plots -- across
three comparisons:

    B. National HDI (composite + 4 sub-components) x ESS respondents
       (stflife, happy), country-round aggregates.
    C. National SHDI x WHR happiness -- literally the original R script's
       design, indicator swapped from UNDP HDI to GDL's SHDI national
       aggregate, to check the two development indices agree.
    D. Subnational SHDI x ESS respondents, region-round aggregates --
       the novel within-country test, kept separate from B/C throughout.
    E. HDI/SHDI vs. two mechanism variables (social trust, self-rated
       health) as a first look beyond the headline wellbeing outcomes.

Run after merge_national_hdi_ess.py and merge_shdi_ess.py:

    python make_figures.py

Output: figures_out/*.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd

from config import ESS_ROUND_YEAR, HDI_COMPOSITE, HDI_SUBCOMPS, ind_short as HDI_IND_SHORT

OUT_DIR = Path("figures_out")
OUT_DIR.mkdir(exist_ok=True)

# ---- Palette (dataviz skill reference palette; light-mode, static/print use) ----
INK_PRIMARY, INK_SECONDARY, INK_MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
CAT = {
    "blue": "#2a78d6", "aqua": "#1baf7a", "yellow": "#eda100", "green": "#008300",
    "violet": "#4a3aa7", "red": "#e34948", "magenta": "#e87ba4", "orange": "#eb6834",
}
TIER_COLORS = {"Very High": CAT["blue"], "High": CAT["aqua"], "Medium": CAT["yellow"], "Low": CAT["red"]}
TIER_ORDER = ["Very High", "High", "Medium", "Low"]
SIG_COLORS = {"ns": "#D0D0D0", "weak": "#9ECAE1", "sig": "#2171B5"}

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.labelcolor": INK_SECONDARY,
    "text.color": INK_PRIMARY, "xtick.color": INK_MUTED, "ytick.color": INK_MUTED,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.grid": True,
    "axes.axisbelow": True, "font.size": 10.5, "font.family": "sans-serif",
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.facecolor": SURFACE,
})

ESS_YEARS_USED = sorted(ESS_ROUND_YEAR[r] for r in range(5, 12))
ESS_YEARS_LABEL = ", ".join(str(y) for y in ESS_YEARS_USED)
SOURCE_ESS = f"Sources: ESS survey years {ESS_YEARS_USED[0]}-{ESS_YEARS_USED[-1]} ({ESS_YEARS_LABEL}); UNDP HDR; Global Data Lab SHDI."
SOURCE_WHR = "Sources: UNDP HDR; World Happiness Report / Our World in Data; Global Data Lab SHDI."


def dev_tier(hdi):
    if pd.isna(hdi):
        return np.nan
    if hdi >= 0.800:
        return "Very High"
    if hdi >= 0.700:
        return "High"
    if hdi >= 0.550:
        return "Medium"
    return "Low"


def fast_r2(x, y):
    ok = x.notna() & y.notna()
    x, y = x[ok].to_numpy(), y[ok].to_numpy()
    if len(x) < 4 or np.std(x) == 0 or np.std(y) == 0:
        return np.nan
    return np.corrcoef(x, y)[0, 1] ** 2


def levels_r2(panel, unit_col, x_col, y_col):
    return panel.groupby(unit_col).apply(lambda g: fast_r2(g[x_col], g[y_col]))


def diffs_r2(panel, unit_col, time_col, x_col, y_col):
    out = {}
    for unit, grp in panel.sort_values(time_col).groupby(unit_col):
        grp = grp.dropna(subset=[x_col, y_col])
        if len(grp) < 5:
            out[unit] = np.nan
            continue
        dx, dy = grp[x_col].diff().to_numpy()[1:], grp[y_col].diff().to_numpy()[1:]
        ok = ~np.isnan(dx) & ~np.isnan(dy)
        if ok.sum() < 4 or np.std(dx[ok]) == 0 or np.std(dy[ok]) == 0:
            out[unit] = np.nan
            continue
        out[unit] = np.corrcoef(dx[ok], dy[ok])[0, 1] ** 2
    return pd.Series(out)


def _corr_p(x, y):
    """Two-sided p-value for a Pearson correlation (t-test on r), mirrors HappinessHDI.R's fast_ols."""
    from scipy import stats
    n = len(x)
    if n < 4 or np.std(x) == 0 or np.std(y) == 0:
        return np.nan
    r = np.corrcoef(x, y)[0, 1]
    if abs(r) >= 1:
        return 0.0
    t = r * np.sqrt((n - 2) / (1 - r ** 2))
    return 2 * stats.t.sf(np.abs(t), df=n - 2)


def levels_p(panel, unit_col, x_col, y_col):
    def _p(g):
        sub = g.dropna(subset=[x_col, y_col])
        return _corr_p(sub[x_col].to_numpy(), sub[y_col].to_numpy())
    return panel.groupby(unit_col).apply(_p)


def diffs_p(panel, unit_col, time_col, x_col, y_col):
    out = {}
    for unit, grp in panel.sort_values(time_col).groupby(unit_col):
        grp = grp.dropna(subset=[x_col, y_col])
        if len(grp) < 5:
            out[unit] = np.nan
            continue
        dx, dy = grp[x_col].diff().to_numpy()[1:], grp[y_col].diff().to_numpy()[1:]
        ok = ~np.isnan(dx) & ~np.isnan(dy)
        out[unit] = _corr_p(dx[ok], dy[ok]) if ok.sum() >= 4 else np.nan
    return pd.Series(out)


def bh_fdr(pvals):
    """Benjamini-Hochberg FDR correction, matching R's p.adjust(method='BH')."""
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    valid = ~np.isnan(p)
    q = np.full(n, np.nan)
    if valid.sum() == 0:
        return q
    pv = p[valid]
    order = np.argsort(pv)
    ranked = pv[order]
    m = len(pv)
    adj = ranked * m / np.arange(1, m + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    adj = np.clip(adj, 0, 1)
    out = np.empty(m)
    out[order] = adj
    q[valid] = out
    return q


def significance_share(panel, unit_col, indicators, outcome, spec, time_col=None, alpha=0.05):
    """
    For each indicator, the share of units (countries/regions) where that
    indicator is FDR-significant (q < alpha) -- FDR correction applied
    jointly across `indicators` within each unit, matching HappinessHDI.R's
    per-country Benjamini-Hochberg design.

    spec: "levels" or "diffs". Returns a dict {indicator: (n_sig, n_total, pct)}.
    """
    units = panel[unit_col].unique()
    sig_counts = {ind: 0 for ind in indicators}
    total_counts = {ind: 0 for ind in indicators}
    for unit in units:
        grp = panel[panel[unit_col] == unit]
        pvals = []
        for ind in indicators:
            if spec == "levels":
                sub = grp.dropna(subset=[ind, outcome])
                p = _corr_p(sub[ind].to_numpy(), sub[outcome].to_numpy())
            else:
                sub = grp.sort_values(time_col).dropna(subset=[ind, outcome])
                dx = sub[ind].diff().to_numpy()[1:]
                dy = sub[outcome].diff().to_numpy()[1:]
                ok = ~np.isnan(dx) & ~np.isnan(dy)
                p = _corr_p(dx[ok], dy[ok]) if ok.sum() >= 4 else np.nan
            pvals.append(p)
        q = bh_fdr(pvals)
        for ind, qi in zip(indicators, q):
            if not np.isnan(qi):
                total_counts[ind] += 1
                if qi < alpha:
                    sig_counts[ind] += 1
    return {
        ind: (sig_counts[ind], total_counts[ind],
              100 * sig_counts[ind] / total_counts[ind] if total_counts[ind] else np.nan)
        for ind in indicators
    }


def savefig(fig, name, note=None, top=0.88):
    fig.subplots_adjust(top=top)
    if note:
        fig.text(0.01, 0.005, note, fontsize=7, color=INK_MUTED)
    fig.savefig(OUT_DIR / name, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {OUT_DIR / name}")


def suptitle(fig, title, subtitle=None):
    fig.suptitle(title, fontsize=13.5, fontweight="bold", x=0.01, ha="left", y=0.985)
    if subtitle:
        fig.text(0.01, 0.93, subtitle, fontsize=8.5, color=INK_SECONDARY, wrap=True)


# =============================================================================
# SECTION A -- Feasibility diagnostics
# =============================================================================

def section_a():
    cov = pd.read_csv("processed/ess_region_coverage.csv")
    shdi_ess = pd.read_csv("processed/ess_with_shdi.csv", low_memory=False)

    match_by_country = (
        shdi_ess.assign(matched=shdi_ess["shdi"].notna())
        .groupby("cntry")["matched"].mean().sort_values(ascending=False) * 100
    )
    fig, ax = plt.subplots(figsize=(11, 6))
    colors = [CAT["blue"] if v >= 50 else CAT["orange"] if v > 0 else INK_MUTED for v in match_by_country]
    ax.bar(match_by_country.index, match_by_country.values, color=colors, width=0.7)
    ax.axhline(50, color=BASELINE, linewidth=1, linestyle="--")
    ax.set_ylabel("% of respondents matched to an SHDI region value")
    ax.set_ylim(0, 100)
    plt.setp(ax.get_xticklabels(), rotation=60, ha="right", fontsize=8)
    suptitle(fig, "A1. SHDI Region-Crosswalk Match Rate by Country")
    savefig(fig, "A1_shdi_match_rate_by_country.png",
            f"Blue >=50% matched, orange <50%, grey no crosswalk match. {SOURCE_ESS}")

    cov["nuts_max"] = cov["nuts_levels_seen"].fillna("").apply(
        lambda s: max([lvl for lvl in s.split(", ") if lvl.startswith("NUTS")], default="none",
                       key=lambda x: x[4] if len(x) > 4 and x[4].isdigit() else "0")
    )
    level_rank = {"NUTS3": 3, "NUTS2": 2, "NUTS1": 1, "NUTS0 (country only)": 0, "none": -1}
    country_level = cov.groupby("cntry")["nuts_max"].agg(lambda s: s.value_counts().idxmax())
    country_level_rank = country_level.map(level_rank).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(11, 6))
    level_colors = {3: CAT["blue"], 2: CAT["aqua"], 1: CAT["yellow"], 0: CAT["red"], -1: INK_MUTED}
    ax.bar(country_level_rank.index, country_level_rank.values,
           color=[level_colors[v] for v in country_level_rank.values], width=0.7)
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["NUTS0\n(country only)", "NUTS1", "NUTS2", "NUTS3"])
    plt.setp(ax.get_xticklabels(), rotation=60, ha="right", fontsize=8)
    suptitle(fig, "A2. Finest Regional Detail Available in ESS, by Country")
    savefig(fig, "A2_nuts_level_by_country.png", SOURCE_ESS)

    # A3: which actual survey years each country has data for -- answers
    # "what years are we looking at" directly, in years rather than round numbers.
    ess = pd.read_csv("processed/ess_with_national_hdi.csv", low_memory=False, usecols=["cntry", "essround"])
    ess["year"] = ess["essround"].map(ESS_ROUND_YEAR)
    present = ess[["cntry", "year"]].drop_duplicates()
    present["present"] = 1
    grid = present.pivot(index="cntry", columns="year", values="present")
    grid = grid.reindex(columns=ESS_YEARS_USED)
    order = grid.sum(axis=1).sort_values(ascending=False).index
    grid = grid.loc[order]

    fig, ax = plt.subplots(figsize=(9, 11))
    ax.imshow(grid.notna().values, cmap=ListedColormap([SURFACE, CAT["blue"]]), aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(len(ESS_YEARS_USED))); ax.set_xticklabels(ESS_YEARS_USED, fontsize=9)
    ax.set_yticks(range(len(grid.index))); ax.set_yticklabels(grid.index, fontsize=7.5)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=SURFACE, linewidth=1.5))
    n_years = grid.notna().sum(axis=1)
    for i, n in enumerate(n_years):
        ax.text(len(ESS_YEARS_USED) - 0.3, i, f"{n}/7", va="center", fontsize=6.5, color=INK_MUTED)
    suptitle(fig, "A3. Which Survey Years Each Country Actually Has",
             f"ESS is a rotating panel of countries, not a fixed set surveyed every wave. Filled = country "
             f"fielded ESS that year. Years used: {ESS_YEARS_LABEL}.")
    savefig(fig, "A3_ess_year_coverage.png", SOURCE_ESS, top=0.88)


# =============================================================================
# SECTION B -- National HDI x ESS (Approach 1)
# =============================================================================

def build_country_round_panel():
    df = pd.read_csv("processed/ess_with_national_hdi.csv", low_memory=False)
    panel = (
        df.groupby(["cntry", "essround"])
        .agg(stflife=("stflife", "mean"), happy=("happy", "mean"),
             hdi=("hdi", "mean"), le=("le", "mean"), eys=("eys", "mean"),
             mys=("mys", "mean"), gnipc=("gnipc", "mean"),
             ppltrst=("ppltrst", "mean"), health=("health", "mean"),
             whr_happiness=("whr_happiness", "mean"), n=("stflife", "size"))
        .reset_index()
    )
    panel["year"] = panel["essround"].map(ESS_ROUND_YEAR)
    latest_hdi = df.sort_values("essround").groupby("cntry")["hdi"].last()
    panel["dev_tier"] = panel["cntry"].map(latest_hdi).apply(dev_tier)
    return panel


def section_b():
    panel = build_country_round_panel()
    panel.to_csv("processed/country_round_panel.csv", index=False)
    indicators = [HDI_COMPOSITE] + HDI_SUBCOMPS

    # B1: heatmap -- country x HDI indicator, FDR significance tier (levels + diffs), for stflife.
    # BH correction applied across the 5 indicators within each country/spec,
    # exactly like HappinessHDI.R's sig_levels_fdr / sig_diffs_fdr.
    def _levels_r2_single(g, ind):
        sub = g.dropna(subset=[ind, "stflife"])
        return fast_r2(sub[ind], sub["stflife"])

    def _diffs_r2_single(g, ind):
        sub = g.sort_values("essround").dropna(subset=[ind, "stflife"])
        dx, dy = sub[ind].diff().to_numpy()[1:], sub["stflife"].diff().to_numpy()[1:]
        ok = ~np.isnan(dx) & ~np.isnan(dy)
        if ok.sum() < 4 or np.std(dx[ok]) == 0 or np.std(dy[ok]) == 0:
            return np.nan
        return np.corrcoef(dx[ok], dy[ok])[0, 1] ** 2

    rows = []
    for cntry, grp in panel.groupby("cntry"):
        p_lev = [_corr_p(*[grp.dropna(subset=[ind, "stflife"])[c].to_numpy() for c in (ind, "stflife")])
                 for ind in indicators]
        q_lev = bh_fdr(p_lev)
        p_dif = []
        for ind in indicators:
            sub = grp.sort_values("essround").dropna(subset=[ind, "stflife"])
            dx, dy = sub[ind].diff().to_numpy()[1:], sub["stflife"].diff().to_numpy()[1:]
            ok = ~np.isnan(dx) & ~np.isnan(dy)
            p_dif.append(_corr_p(dx[ok], dy[ok]) if ok.sum() >= 4 else np.nan)
        q_dif = bh_fdr(p_dif)
        for i, ind in enumerate(indicators):
            rows.append({"cntry": cntry, "indicator": ind,
                         "r2_levels": _levels_r2_single(grp, ind), "r2_diffs": _diffs_r2_single(grp, ind),
                         "q_levels": q_lev[i], "q_diffs": q_dif[i]})
    heat = pd.DataFrame(rows)
    heat["ind_label"] = heat["indicator"].map(HDI_IND_SHORT)

    def sig_tier(q):
        if pd.isna(q):
            return np.nan
        return 2 if q < 0.05 else 1 if q < 0.10 else 0

    heat["tier_levels"] = heat["q_levels"].apply(sig_tier)
    heat["tier_diffs"] = heat["q_diffs"].apply(sig_tier)

    has_any = heat.groupby("cntry")["r2_levels"].apply(lambda s: s.notna().any())
    keep_countries = has_any[has_any].index
    dropped = sorted(set(heat["cntry"].unique()) - set(keep_countries))
    heat = heat[heat["cntry"].isin(keep_countries)]
    order = heat.groupby("cntry")["r2_levels"].median().sort_values(ascending=False).index.tolist()
    heat["cntry"] = pd.Categorical(heat["cntry"], categories=order, ordered=True)
    heat = heat.sort_values("cntry")

    sig_cmap = ListedColormap([SIG_COLORS["ns"], SIG_COLORS["weak"], SIG_COLORS["sig"]])

    fig, axes = plt.subplots(1, 2, figsize=(12, 10), sharey=True)
    for ax, spec, col, rcol in zip(axes, ["Levels", "Across-year differences"],
                                    ["tier_levels", "tier_diffs"], ["r2_levels", "r2_diffs"]):
        piv = heat.pivot(index="cntry", columns="ind_label", values=col)[[HDI_IND_SHORT[i] for i in indicators]]
        rpiv = heat.pivot(index="cntry", columns="ind_label", values=rcol)[[HDI_IND_SHORT[i] for i in indicators]]
        ax.imshow(piv.values, cmap=sig_cmap, vmin=0, vmax=2, aspect="auto")
        ax.set_xticks(range(len(piv.columns))); ax.set_xticklabels(piv.columns, rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(len(piv.index))); ax.set_yticklabels(piv.index, fontsize=6.5)
        ax.set_title(spec, fontsize=10.5, loc="left")
        for i in range(piv.shape[0]):
            for j in range(piv.shape[1]):
                v, r = piv.values[i, j], rpiv.values[i, j]
                if not np.isnan(v):
                    txt_color = "white" if v == 2 else INK_SECONDARY
                    ax.text(j, i, f"{r:.2f}", ha="center", va="center", fontsize=5.2, color=txt_color)
        pct_sig = 100 * (piv.values == 2).sum() / np.isfinite(piv.values).sum()
        ax.set_xlabel(f"{pct_sig:.0f}% of cells FDR-significant (q<.05)", fontsize=8.5, color=INK_SECONDARY)
    handles = [plt.Rectangle((0, 0), 1, 1, color=SIG_COLORS[k]) for k in ("ns", "weak", "sig")]
    fig.legend(handles, ["Not significant", "FDR q<.10", "FDR q<.05"], loc="lower center",
               bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False, fontsize=9)
    suptitle(fig, "B1. HDI vs. Life Satisfaction: Significance Heatmap (FDR-Corrected)",
             "Countries ordered by median levels R². Color = significance tier (BH-corrected across the 5 "
             "indicators per country); number in each cell is still R² for reference.")
    note = (f"Excluded (fewer than 4 ESS survey years with HDI/stflife data): {', '.join(dropped)}. "
            f"{SOURCE_ESS}") if dropped else SOURCE_ESS
    savefig(fig, "B1_heatmap_country_indicator.png", note, top=0.90)

    # B2: collapse scatter (levels vs diffs), tier-colored + labeled, HDI composite, both outcomes
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.5))
    for ax, outcome in zip(axes, ["stflife", "happy"]):
        lev = levels_r2(panel, "cntry", "hdi", outcome).rename("r2_levels")
        dif = diffs_r2(panel, "cntry", "essround", "hdi", outcome).rename("r2_diffs")
        comp = pd.concat([lev, dif], axis=1).dropna()
        comp = comp.join(panel.groupby("cntry")["dev_tier"].first())
        ax.plot([0, 1], [0, 1], color=BASELINE, linewidth=1, linestyle="--")
        for tier in TIER_ORDER:
            sub = comp[comp["dev_tier"] == tier]
            ax.scatter(sub["r2_levels"], sub["r2_diffs"], s=36, alpha=0.8, color=TIER_COLORS[tier],
                       label=tier, edgecolors="white", linewidths=0.4)
        for cntry, row in comp.iterrows():
            if row["r2_levels"] > 0.45 or row["r2_diffs"] > 0.35:
                ax.annotate(cntry, (row["r2_levels"], row["r2_diffs"]), fontsize=7, color=INK_SECONDARY,
                            xytext=(3, 3), textcoords="offset points")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xlabel("R² -- Levels"); ax.set_ylabel("R² -- Across-year differences")
        ax.set_title(f"HDI composite x {outcome}", fontsize=11, loc="left")
    axes[1].legend(title="Dev. tier", frameon=False, fontsize=8, loc="upper right")
    suptitle(fig, "B2. Per-Country Collapse: National HDI vs. ESS Wellbeing",
             "Mirrors HappinessHDI.R's D2 collapse scatter. Points on the dashed line show no collapse.")
    savefig(fig, "B2_collapse_scatter_national.png", SOURCE_ESS)

    # B3: dumbbell -- per-country R^2, open=levels filled=diffs, HDI composite x stflife
    lev = levels_r2(panel, "cntry", "hdi", "stflife").rename("r2_levels")
    dif = diffs_r2(panel, "cntry", "essround", "hdi", "stflife").rename("r2_diffs")
    db = pd.concat([lev, dif], axis=1).dropna().join(panel.groupby("cntry")["dev_tier"].first())
    db = db.sort_values("r2_levels")
    fig, ax = plt.subplots(figsize=(9, 11))
    y = np.arange(len(db))
    for yi, (cntry, row) in zip(y, db.iterrows()):
        ax.plot([row["r2_diffs"], row["r2_levels"]], [yi, yi], color=TIER_COLORS.get(row["dev_tier"], INK_MUTED),
                linewidth=1.2, alpha=0.6)
    ax.scatter(db["r2_levels"], y, s=45, facecolors="white", edgecolors=[TIER_COLORS.get(t, INK_MUTED) for t in db["dev_tier"]],
               linewidths=1.4, zorder=3, label="Levels")
    ax.scatter(db["r2_diffs"], y, s=32, color=[TIER_COLORS.get(t, INK_MUTED) for t in db["dev_tier"]],
               edgecolors=INK_SECONDARY, linewidths=0.3, zorder=3, label="Across-year differences")
    ax.set_yticks(y); ax.set_yticklabels(db.index, fontsize=7.5)
    ax.set_xlabel("R² (HDI composite x stflife)")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    suptitle(fig, "B3. HDI Composite R² Collapse by Country",
             "Open circle = levels; filled circle = across-year differences. Mirrors HappinessHDI.R's D3 dumbbell.")
    savefig(fig, "B3_dumbbell_national.png", SOURCE_ESS, top=0.93)

    # B4: collapse bar -- share of countries FDR-significant (q<.05), levels vs diffs, per indicator x outcome
    bar_rows = []
    for outcome in ["stflife", "happy"]:
        share_lev = significance_share(panel, "cntry", indicators, outcome, "levels")
        share_dif = significance_share(panel, "cntry", indicators, outcome, "diffs", time_col="essround")
        for ind in indicators:
            n_sig, n_tot, pct = share_lev[ind]
            bar_rows.append({"indicator": HDI_IND_SHORT[ind], "outcome": outcome, "spec": "Levels",
                             "pct_sig": pct, "n_sig": n_sig, "n_tot": n_tot})
            n_sig, n_tot, pct = share_dif[ind]
            bar_rows.append({"indicator": HDI_IND_SHORT[ind], "outcome": outcome, "spec": "Diffs",
                             "pct_sig": pct, "n_sig": n_sig, "n_tot": n_tot})
    bar_df = pd.DataFrame(bar_rows)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, outcome in zip(axes, ["stflife", "happy"]):
        sub = bar_df[bar_df.outcome == outcome]
        ind_order = [HDI_IND_SHORT[i] for i in indicators]
        x = np.arange(len(ind_order)); width = 0.35
        for i, spec in enumerate(["Levels", "Diffs"]):
            rows_i = [sub[(sub.indicator == ii) & (sub.spec == spec)].iloc[0] for ii in ind_order]
            vals = [r["pct_sig"] for r in rows_i]
            color = CAT["blue"] if spec == "Levels" else CAT["red"]
            bars = ax.bar(x + (i - 0.5) * width, vals, width, label=spec, color=color, alpha=0.88)
            labels = [f"{r['n_sig']:.0f}/{r['n_tot']:.0f}" for r in rows_i]
            ax.bar_label(bars, labels=labels, padding=2, fontsize=7, color=INK_SECONDARY)
        ax.set_xticks(x); ax.set_xticklabels(ind_order, rotation=30, ha="right", fontsize=8.5)
        ax.set_title(outcome, fontsize=11, loc="left")
        ax.set_ylim(0, 100)
    axes[0].set_ylabel("% of countries FDR-significant (q<.05)")
    axes[1].legend(frameon=False, fontsize=9)
    suptitle(fig, "B4. Share of Countries Statistically Significant: Levels vs. Differences",
             "BH-FDR corrected across the 5 indicators within each country. Bar labels show sig./total countries.")
    savefig(fig, "B4_collapse_bar_national.png", SOURCE_ESS)

    # B5: quadrant plot -- HDI trend vs stflife trend, per actual survey year
    # (not per round-index: ESS waves are ~2 years apart except one 3-year
    # gap, 2020->2023, so slope-per-round would understate that gap's rate).
    def ols_slope(x, y):
        ok = x.notna() & y.notna()
        x, y = x[ok].to_numpy(), y[ok].to_numpy()
        if len(x) < 4 or np.std(x) == 0:
            return np.nan
        return np.polyfit(x, y, 1)[0]
    slopes = panel.groupby("cntry").apply(
        lambda g: pd.Series({"slope_hdi": ols_slope(g["year"], g["hdi"]),
                             "slope_stflife": ols_slope(g["year"], g["stflife"])})
    ).dropna()
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.axhline(0, color=BASELINE, linewidth=1); ax.axvline(0, color=BASELINE, linewidth=1)
    q_colors = np.where((slopes.slope_hdi > 0) & (slopes.slope_stflife > 0), CAT["blue"],
                np.where((slopes.slope_hdi < 0) & (slopes.slope_stflife > 0), CAT["aqua"],
                np.where((slopes.slope_hdi > 0) & (slopes.slope_stflife < 0), CAT["orange"], CAT["red"])))
    ax.scatter(slopes["slope_hdi"], slopes["slope_stflife"], s=45, c=q_colors, edgecolors="white", linewidths=0.5)
    for cntry, row in slopes.iterrows():
        ax.annotate(cntry, (row["slope_hdi"], row["slope_stflife"]), fontsize=6.5, color=INK_SECONDARY,
                    xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel(f"HDI trend, {ESS_YEARS_USED[0]}-{ESS_YEARS_USED[-1]} (per-year slope)")
    ax.set_ylabel(f"Life satisfaction trend, {ESS_YEARS_USED[0]}-{ESS_YEARS_USED[-1]} (per-year slope)")
    n_q = {
        "HDI up / stflife up": ((slopes.slope_hdi > 0) & (slopes.slope_stflife > 0)).sum(),
        "HDI down / stflife up": ((slopes.slope_hdi < 0) & (slopes.slope_stflife > 0)).sum(),
        "HDI up / stflife down": ((slopes.slope_hdi > 0) & (slopes.slope_stflife < 0)).sum(),
        "both down": ((slopes.slope_hdi < 0) & (slopes.slope_stflife < 0)).sum(),
    }
    subtitle_txt = "  |  ".join(f"{k}: n={v}" for k, v in n_q.items())
    suptitle(fig, "B5. HDI Progress vs. Life-Satisfaction Trend, by Country", subtitle_txt)
    savefig(fig, "B5_quadrant_national.png", SOURCE_ESS)

    print(f"Section B: {len(panel)} country-year cells, {panel['cntry'].nunique()} countries.")


# =============================================================================
# SECTION C -- National SHDI vs. WHR happiness (replicates HappinessHDI.R design)
# =============================================================================

def section_c():
    panel = pd.read_csv("processed/national_hdi_shdi_whr_panel.csv")
    latest_hdi = panel.sort_values("year").groupby("iso3")["hdi"].last()
    panel["dev_tier"] = panel["iso3"].map(latest_hdi).apply(dev_tier)

    # C1: levels scatter -- WHR happiness vs SHDI-national, tier-colored (mirrors original F2)
    fig, ax = plt.subplots(figsize=(9, 7.5))
    for tier in TIER_ORDER:
        sub = panel[panel["dev_tier"] == tier]
        ax.scatter(sub["shdi_national"], sub["whr_happiness"], s=20, alpha=0.6, color=TIER_COLORS[tier],
                   label=tier, edgecolors="none")
    r2 = fast_r2(panel["shdi_national"], panel["whr_happiness"])
    ax.annotate(f"Pooled R² = {r2:.3f}  (n={panel[['shdi_national','whr_happiness']].dropna().shape[0]} country-years)",
                xy=(0.03, 0.95), xycoords="axes fraction", fontsize=9, color=INK_SECONDARY)
    ax.set_xlabel("SHDI (national-level aggregate)")
    ax.set_ylabel("WHR Cantril Ladder")
    ax.legend(title="Dev. tier", frameon=False, fontsize=8, loc="lower right")
    suptitle(fig, "C1. WHR Happiness vs. SHDI (National Aggregate)",
             "Replicates the original HappinessHDI.R scatter with GDL's SHDI as the indicator instead of UNDP HDI. "
             "Note: this pooled R² mixes between- and within-country variation -- see C2 for the "
             "per-country-median R² that's directly comparable to HappinessHDI.R's headline 0.322.")
    savefig(fig, "C1_whr_vs_shdi_national_levels.png", SOURCE_WHR)

    # C2: collapse bar -- share of countries FDR-significant, HDI vs SHDI-national, levels vs diffs
    inds_c2 = ["hdi", "shdi_national"]
    labels_c2 = {"hdi": "UNDP HDI", "shdi_national": "GDL SHDI (national)"}
    share_lev = significance_share(panel, "iso3", inds_c2, "whr_happiness", "levels")
    share_dif = significance_share(panel, "iso3", inds_c2, "whr_happiness", "diffs", time_col="year")
    fig, ax = plt.subplots(figsize=(8, 6.5))
    x = np.arange(2); width = 0.35
    inds = [labels_c2[i] for i in inds_c2]
    for i, (spec_label, share) in enumerate([("Levels", share_lev), ("Year-to-year differences", share_dif)]):
        vals = [share[ind][2] for ind in inds_c2]
        labels = [f"{share[ind][0]:.0f}/{share[ind][1]:.0f}" for ind in inds_c2]
        color = CAT["blue"] if spec_label == "Levels" else CAT["red"]
        bars = ax.bar(x + (i - 0.5) * width, vals, width, label=spec_label, color=color, alpha=0.88)
        ax.bar_label(bars, labels=labels, padding=3, fontsize=9, color=INK_SECONDARY)
    ax.set_xticks(x); ax.set_xticklabels(inds)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of countries FDR-significant (q<.05) vs. WHR happiness")
    ax.legend(frameon=False, fontsize=9)
    suptitle(fig, "C2. Does SHDI Show the Same Levels-Diffs Collapse as HDI?",
             "Same design as the original analysis; FDR-corrected jointly across HDI and SHDI.")
    savefig(fig, "C2_collapse_bar_hdi_vs_shdi.png", SOURCE_WHR, top=0.82)

    # C3: HDI vs SHDI-national agreement check
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.plot([panel.hdi.min(), panel.hdi.max()], [panel.hdi.min(), panel.hdi.max()],
            color=BASELINE, linewidth=1, linestyle="--")
    ax.scatter(panel["hdi"], panel["shdi_national"], s=10, alpha=0.4, color=CAT["violet"])
    r2 = fast_r2(panel["hdi"], panel["shdi_national"])
    ax.annotate(f"R² = {r2:.3f}", xy=(0.03, 0.95), xycoords="axes fraction", fontsize=9, color=INK_SECONDARY)
    ax.set_xlabel("UNDP HDI"); ax.set_ylabel("GDL SHDI (national aggregate)")
    suptitle(fig, "C3. UNDP HDI vs. GDL SHDI: Do the Two National Indices Agree?")
    savefig(fig, "C3_hdi_vs_shdi_national_agreement.png", SOURCE_WHR)

    print(f"Section C: {panel.dropna(subset=['hdi','shdi_national']).shape[0]} country-year cells with both indices.")


# =============================================================================
# SECTION D -- Subnational SHDI x ESS (Approach 2, kept separate throughout)
# =============================================================================

def build_region_round_panel():
    df = pd.read_csv("processed/ess_with_shdi.csv", low_memory=False)
    df = df.dropna(subset=["gdl_region_name"])
    panel = (
        df.groupby(["cntry", "gdl_region_name", "essround"])
        .agg(stflife=("stflife", "mean"), happy=("happy", "mean"), shdi=("shdi", "mean"),
             ppltrst=("ppltrst", "mean"), health=("health", "mean"), n=("stflife", "size"))
        .reset_index()
    )
    panel["region_key"] = panel["cntry"] + " / " + panel["gdl_region_name"]
    panel["year"] = panel["essround"].map(ESS_ROUND_YEAR)
    return panel


def section_d():
    panel = build_region_round_panel()
    panel.to_csv("processed/region_round_panel.csv", index=False)

    region_counts = panel.groupby("cntry")["gdl_region_name"].nunique().sort_values(ascending=False)
    top_countries = region_counts.head(8).index.tolist()
    palette_cycle = list(CAT.values())

    # D1: region-round scatter, colored by country
    fig, ax = plt.subplots(figsize=(10, 7.5))
    for i, cntry in enumerate(top_countries):
        sub = panel[panel["cntry"] == cntry].dropna(subset=["shdi", "stflife"])
        ax.scatter(sub["shdi"], sub["stflife"], s=24, alpha=0.75, color=palette_cycle[i % len(palette_cycle)],
                   label=cntry, edgecolors="white", linewidths=0.3)
    r2_all = fast_r2(panel["shdi"], panel["stflife"])
    n_region_years = panel[["shdi", "stflife"]].dropna().shape[0]
    ax.annotate(f"Pooled R² = {r2_all:.3f}  (n={n_region_years} region-years)",
                xy=(0.03, 0.95), xycoords="axes fraction", fontsize=9, color=INK_SECONDARY)
    ax.set_xlabel("Subnational HDI (SHDI)"); ax.set_ylabel("Region mean Life Satisfaction (pooled across years)")
    ax.legend(title="Country (top 8 by region count)", frameon=False, fontsize=8, loc="lower right", ncol=2)
    suptitle(fig, "D1. Within- and Between-Country Regional Variation: Life Satisfaction vs. SHDI",
             "Pooled R² mixes between-country and within-country (regional) variation -- see D2 for the "
             "within-country-only test, and D3 for the per-region levels-vs-diffs collapse.")
    savefig(fig, "D1_region_scatter_stflife_vs_shdi.png", SOURCE_ESS)

    # D2: within-country small multiples
    n_top = min(6, len(top_countries))
    fig, axes = plt.subplots(2, 3, figsize=(14, 8.5), sharey=True)
    for ax, cntry in zip(axes.flat, top_countries[:n_top]):
        sub = panel[panel["cntry"] == cntry].dropna(subset=["shdi", "stflife"])
        rmeans = sub.groupby("gdl_region_name").agg(shdi=("shdi", "mean"), stflife=("stflife", "mean"))
        ax.scatter(rmeans["shdi"], rmeans["stflife"], s=45, alpha=0.85, color=CAT["blue"], edgecolors="white", linewidths=0.5)
        if len(rmeans) >= 4:
            r2 = fast_r2(rmeans["shdi"], rmeans["stflife"])
            ax.annotate(f"R²={r2:.2f}, n={len(rmeans)}", xy=(0.05, 0.9), xycoords="axes fraction",
                        fontsize=8, color=INK_SECONDARY)
        ax.set_title(cntry, fontsize=10.5, loc="left", fontweight="bold")
    for ax in axes.flat[n_top:]:
        ax.axis("off")
    fig.supxlabel("SHDI (region mean across matched survey years)", fontsize=10)
    fig.supylabel("Life Satisfaction (region mean)", fontsize=10)
    suptitle(fig, "D2. Do More-Developed Regions Report Higher Life Satisfaction Within the Same Country?",
             "Core Approach-2 test: within-country regional development vs. wellbeing, national context held fixed.")
    savefig(fig, "D2_within_country_region_smallmultiples.png", SOURCE_ESS, top=0.87)

    # D3: region-level collapse scatter
    lev = levels_r2(panel, "region_key", "shdi", "stflife").rename("r2_levels")
    dif = diffs_r2(panel, "region_key", "essround", "shdi", "stflife").rename("r2_diffs")
    comp = pd.concat([lev, dif], axis=1).dropna()
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.plot([0, 1], [0, 1], color=BASELINE, linewidth=1, linestyle="--")
    ax.scatter(comp["r2_levels"], comp["r2_diffs"], s=20, alpha=0.5, color=CAT["aqua"])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel("R² -- Levels (region x SHDI)"); ax.set_ylabel("R² -- Across-year differences")
    suptitle(fig, f"D3. Per-Region Collapse: stflife x SHDI (n={len(comp)} regions with >=5 survey years)")
    savefig(fig, "D3_collapse_scatter_regional.png", SOURCE_ESS)

    # D4: SHDI distribution by country (within-country heterogeneity)
    order = panel.groupby("cntry")["shdi"].median().sort_values(ascending=False).index.tolist()
    data = [panel[panel["cntry"] == c]["shdi"].dropna().values for c in order]
    fig, ax = plt.subplots(figsize=(13, 6.5))
    bp = ax.boxplot(data, tick_labels=order, patch_artist=True, widths=0.6, showfliers=False,
                     medianprops={"color": INK_PRIMARY, "linewidth": 1.2})
    for box in bp["boxes"]:
        box.set(facecolor=CAT["blue"], alpha=0.55, edgecolor=CAT["blue"])
    ax.set_ylabel("SHDI (region observations, pooled across years)")
    plt.setp(ax.get_xticklabels(), rotation=60, ha="right", fontsize=8)
    suptitle(fig, "D4. Within-Country Spread in Subnational HDI",
             "Wider boxes = more regional development inequality within that country.")
    savefig(fig, "D4_shdi_distribution_by_country.png", SOURCE_ESS)

    print(f"Section D: {len(panel)} region-year cells, {panel['gdl_region_name'].nunique()} distinct regions, "
          f"{panel['cntry'].nunique()} countries.")


# =============================================================================
# SECTION E -- Beyond wellbeing: HDI/SHDI vs. two mechanism variables
# =============================================================================

def section_e():
    nat = pd.read_csv("processed/country_round_panel.csv")
    reg = pd.read_csv("processed/region_round_panel.csv")

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    specs = [
        (axes[0, 0], nat, "hdi", "ppltrst", "National HDI vs. Social Trust", CAT["blue"]),
        (axes[0, 1], nat, "hdi", "health", "National HDI vs. Self-Rated Health", CAT["green"]),
        (axes[1, 0], reg, "shdi", "ppltrst", "Subnational SHDI vs. Social Trust", CAT["aqua"]),
        (axes[1, 1], reg, "shdi", "health", "Subnational SHDI vs. Self-Rated Health", CAT["violet"]),
    ]
    for ax, data, xcol, ycol, title, color in specs:
        sub = data.dropna(subset=[xcol, ycol])
        ax.scatter(sub[xcol], sub[ycol], s=16, alpha=0.4, color=color, edgecolors="none")
        r2 = fast_r2(sub[xcol], sub[ycol])
        ax.annotate(f"R² = {r2:.3f}  (n={len(sub)})", xy=(0.03, 0.93), xycoords="axes fraction",
                    fontsize=8.5, color=INK_SECONDARY)
        ax.set_title(title, fontsize=10.5, loc="left")
        ax.set_xlabel(xcol.upper())
        ax.set_ylabel("mean (country/region, pooled across years)")
    suptitle(fig, "E. Development vs. Two Mechanism Variables",
             "health is self-rated (1=very good...5=very bad, reverse of intuition -- check sign). "
             "ppltrst is 0-10 generalized trust. First look only; concept note's full mechanism model is a next step.")
    savefig(fig, "E1_mechanism_variables.png", SOURCE_ESS, top=0.87)

    # E2: same layout, but mechanism variables plotted directly against stflife
    # (not against HDI/SHDI) -- isolates each variable's own link to wellbeing.
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    specs2 = [
        (axes[0, 0], nat, "ppltrst", "stflife", "National: Social Trust vs. Life Satisfaction", CAT["blue"]),
        (axes[0, 1], nat, "health", "stflife", "National: Self-Rated Health vs. Life Satisfaction", CAT["green"]),
        (axes[1, 0], reg, "ppltrst", "stflife", "Regional: Social Trust vs. Life Satisfaction", CAT["aqua"]),
        (axes[1, 1], reg, "health", "stflife", "Regional: Self-Rated Health vs. Life Satisfaction", CAT["violet"]),
    ]
    for ax, data, xcol, ycol, title, color in specs2:
        sub = data.dropna(subset=[xcol, ycol])
        ax.scatter(sub[xcol], sub[ycol], s=16, alpha=0.4, color=color, edgecolors="none")
        r2 = fast_r2(sub[xcol], sub[ycol])
        ax.annotate(f"R² = {r2:.3f}  (n={len(sub)})", xy=(0.03, 0.93), xycoords="axes fraction",
                    fontsize=8.5, color=INK_SECONDARY)
        ax.set_title(title, fontsize=10.5, loc="left")
        ax.set_xlabel(xcol.upper())
        ax.set_ylabel("stflife (mean, pooled across years)")
    suptitle(fig, "E2. Mechanism Variables vs. Life Satisfaction Directly",
             "Same variables as E1, now regressed straight onto stflife instead of onto HDI/SHDI -- "
             "compare these R² to E3's ranking to see whether trust or health tracks wellbeing "
             "more tightly than development itself.")
    savefig(fig, "E2_mechanism_vs_stflife.png", SOURCE_ESS, top=0.85)

    # E3: ranking bar chart -- share of units where HDI/SHDI, trust, or health
    # significantly predicts stflife (levels), national and regional side by
    # side. FDR-corrected jointly across the 3 predictors within each unit.
    nat_share = significance_share(nat, "cntry", ["hdi", "ppltrst", "health"], "stflife", "levels")
    reg_share = significance_share(reg, "region_key", ["shdi", "ppltrst", "health"], "stflife", "levels")
    nat_labels = {"hdi": "HDI", "ppltrst": "Social trust", "health": "Self-rated health"}
    reg_labels = {"shdi": "SHDI", "ppltrst": "Social trust", "health": "Self-rated health"}

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    for ax, share, lbl_map, level in zip(
        axes, [nat_share, reg_share], [nat_labels, reg_labels],
        ["National (country-level)", "Regional (region-level)"]
    ):
        ordered = sorted(share.items(), key=lambda kv: kv[1][2], reverse=True)
        labels = [lbl_map[k] for k, _ in ordered]
        vals = [v[2] for _, v in ordered]
        counts = [f"{v[0]:.0f}/{v[1]:.0f}" for _, v in ordered]
        colors = [CAT["blue"] if lbl in ("HDI", "SHDI") else CAT["aqua"] if lbl == "Social trust" else CAT["violet"]
                  for lbl in labels]
        bars = ax.bar(labels, vals, color=colors, width=0.6, alpha=0.9)
        ax.bar_label(bars, labels=counts, padding=3, fontsize=10, color=INK_SECONDARY)
        ax.set_title(level, fontsize=11, loc="left")
        ax.set_ylim(0, 100)
        plt.setp(ax.get_xticklabels(), fontsize=9.5)
    axes[0].set_ylabel("% of units FDR-significant (q<.05) vs. stflife")
    suptitle(fig, "E3. Which Predictor Explains Life Satisfaction Best?",
             "Share of countries/regions where each predictor is individually FDR-significant, corrected "
             "jointly across the 3 predictors per unit. Bar labels show sig./total units.")
    savefig(fig, "E3_r2_ranking_stflife.png", SOURCE_ESS)

    print(f"Section E significance share -- National: {sorted(nat_share.items(), key=lambda kv: -kv[1][2])}")
    print(f"Section E significance share -- Regional: {sorted(reg_share.items(), key=lambda kv: -kv[1][2])}")


if __name__ == "__main__":
    section_a()
    section_b()
    section_c()
    section_d()
    section_e()
    print(f"\nAll figures saved to {OUT_DIR}/")
