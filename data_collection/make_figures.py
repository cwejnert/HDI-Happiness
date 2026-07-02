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

SOURCE_ESS = "Sources: ESS rounds 5-11; UNDP HDR; Global Data Lab SHDI."
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

    # B1: heatmap -- country x HDI indicator, R^2 (levels + diffs), for stflife
    rows = []
    for cntry, grp in panel.groupby("cntry"):
        for ind in indicators:
            rows.append({
                "cntry": cntry, "indicator": ind,
                "r2_levels": fast_r2(grp[ind], grp["stflife"]),
                "r2_diffs": np.nan,
            })
    heat = pd.DataFrame(rows)
    diffs_by_ind = {ind: diffs_r2(panel, "cntry", "essround", ind, "stflife") for ind in indicators}
    heat["r2_diffs"] = heat.apply(lambda r: diffs_by_ind[r["indicator"]].get(r["cntry"], np.nan), axis=1)
    heat["ind_label"] = heat["indicator"].map(HDI_IND_SHORT)
    # Countries with < 4 ESS rounds available can't produce any levels R^2
    # (fast_r2 needs n>=4) -- drop them from the heatmap instead of showing
    # blank rows; they're still counted in the round-coverage figures (A1/A2).
    has_any = heat.groupby("cntry")["r2_levels"].apply(lambda s: s.notna().any())
    keep_countries = has_any[has_any].index
    dropped = sorted(set(heat["cntry"].unique()) - set(keep_countries))
    heat = heat[heat["cntry"].isin(keep_countries)]
    order = heat.groupby("cntry")["r2_levels"].median().sort_values(ascending=False).index.tolist()
    heat["cntry"] = pd.Categorical(heat["cntry"], categories=order, ordered=True)
    heat = heat.sort_values("cntry")

    fig, axes = plt.subplots(1, 2, figsize=(12, 10), sharey=True)
    im = None
    for ax, spec, col in zip(axes, ["Levels", "Across-round differences"], ["r2_levels", "r2_diffs"]):
        piv = heat.pivot(index="cntry", columns="ind_label", values=col)
        piv = piv[[HDI_IND_SHORT[i] for i in indicators]]
        im = ax.imshow(piv.values, cmap="Blues", vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(piv.columns))); ax.set_xticklabels(piv.columns, rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(len(piv.index))); ax.set_yticklabels(piv.index, fontsize=6.5)
        ax.set_title(spec, fontsize=10.5, loc="left")
        for i in range(piv.shape[0]):
            for j in range(piv.shape[1]):
                v = piv.values[i, j]
                if not np.isnan(v):
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=5.2,
                            color="white" if v > 0.5 else INK_SECONDARY)
    fig.subplots_adjust(right=0.88)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.015, 0.55])
    fig.colorbar(im, cax=cbar_ax, label="R²")
    suptitle(fig, "B1. HDI vs. Life Satisfaction: Country x Indicator Heatmap",
             "Countries ordered by median levels R². Mirrors HappinessHDI.R's D1 heatmap.")
    note = (f"Excluded (fewer than 4 ESS rounds with HDI/stflife data): {', '.join(dropped)}. "
            f"Diffs R^2 for a country with only 5 rounds rests on <=4 differenced points -- "
            f"treat high across-round values with caution (no LOYO cross-validation here, unlike HappinessHDI.R). "
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
        ax.set_xlabel("R² -- Levels"); ax.set_ylabel("R² -- Across-round differences")
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
               edgecolors=INK_SECONDARY, linewidths=0.3, zorder=3, label="Across-round differences")
    ax.set_yticks(y); ax.set_yticklabels(db.index, fontsize=7.5)
    ax.set_xlabel("R² (HDI composite x stflife)")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    suptitle(fig, "B3. HDI Composite R² Collapse by Country",
             "Open circle = levels; filled circle = across-round differences. Mirrors HappinessHDI.R's D3 dumbbell.")
    savefig(fig, "B3_dumbbell_national.png", SOURCE_ESS, top=0.93)

    # B4: collapse bar -- median R^2, levels vs diffs, per indicator x outcome
    bar_rows = []
    for ind in indicators:
        for outcome in ["stflife", "happy"]:
            lev = levels_r2(panel, "cntry", ind, outcome)
            dif = diffs_r2(panel, "cntry", "essround", ind, outcome)
            bar_rows.append({"indicator": HDI_IND_SHORT[ind], "outcome": outcome, "spec": "Levels", "median_r2": lev.median()})
            bar_rows.append({"indicator": HDI_IND_SHORT[ind], "outcome": outcome, "spec": "Diffs", "median_r2": dif.median()})
    bar_df = pd.DataFrame(bar_rows)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, outcome in zip(axes, ["stflife", "happy"]):
        sub = bar_df[bar_df.outcome == outcome]
        ind_order = [HDI_IND_SHORT[i] for i in indicators]
        x = np.arange(len(ind_order)); width = 0.35
        for i, spec in enumerate(["Levels", "Diffs"]):
            vals = [sub[(sub.indicator == ii) & (sub.spec == spec)]["median_r2"].iloc[0] for ii in ind_order]
            color = CAT["blue"] if spec == "Levels" else CAT["red"]
            bars = ax.bar(x + (i - 0.5) * width, vals, width, label=spec, color=color, alpha=0.88)
            ax.bar_label(bars, fmt="%.2f", padding=2, fontsize=7.5, color=INK_SECONDARY)
        ax.set_xticks(x); ax.set_xticklabels(ind_order, rotation=30, ha="right", fontsize=8.5)
        ax.set_title(outcome, fontsize=11, loc="left")
    axes[0].set_ylabel("Median country-level R²")
    axes[1].legend(frameon=False, fontsize=9)
    suptitle(fig, "B4. Median R² Across Countries: Levels vs. Across-Round Differences",
             "Mirrors HappinessHDI.R's D5 collapse bar chart.")
    savefig(fig, "B4_collapse_bar_national.png", SOURCE_ESS)

    # B5: quadrant plot -- HDI trend vs stflife trend across ESS rounds
    def ols_slope(x, y):
        ok = x.notna() & y.notna()
        x, y = x[ok].to_numpy(), y[ok].to_numpy()
        if len(x) < 4 or np.std(x) == 0:
            return np.nan
        return np.polyfit(x, y, 1)[0]
    slopes = panel.groupby("cntry").apply(
        lambda g: pd.Series({"slope_hdi": ols_slope(g["essround"], g["hdi"]),
                             "slope_stflife": ols_slope(g["essround"], g["stflife"])})
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
    ax.set_xlabel("HDI trend across ESS rounds (slope)")
    ax.set_ylabel("Life satisfaction trend across ESS rounds (slope)")
    n_q = {
        "HDI up / stflife up": ((slopes.slope_hdi > 0) & (slopes.slope_stflife > 0)).sum(),
        "HDI down / stflife up": ((slopes.slope_hdi < 0) & (slopes.slope_stflife > 0)).sum(),
        "HDI up / stflife down": ((slopes.slope_hdi > 0) & (slopes.slope_stflife < 0)).sum(),
        "both down": ((slopes.slope_hdi < 0) & (slopes.slope_stflife < 0)).sum(),
    }
    subtitle_txt = "  |  ".join(f"{k}: n={v}" for k, v in n_q.items())
    suptitle(fig, "B5. HDI Progress vs. Life-Satisfaction Trend, by Country", subtitle_txt)
    savefig(fig, "B5_quadrant_national.png", SOURCE_ESS)

    print(f"Section B: {len(panel)} country-round cells, {panel['cntry'].nunique()} countries.")


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

    # C2: collapse bar -- HDI vs SHDI-national, levels vs diffs, both vs WHR happiness
    rows = []
    for ind, label in [("hdi", "UNDP HDI"), ("shdi_national", "GDL SHDI (national)")]:
        lev = levels_r2(panel, "iso3", ind, "whr_happiness")
        dif = diffs_r2(panel, "iso3", "year", ind, "whr_happiness")
        rows.append({"indicator": label, "spec": "Levels", "median_r2": lev.median()})
        rows.append({"indicator": label, "spec": "Year-to-year differences", "median_r2": dif.median()})
    bar_df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(8, 6.5))
    x = np.arange(2); width = 0.35
    inds = ["UNDP HDI", "GDL SHDI (national)"]
    for i, spec in enumerate(["Levels", "Year-to-year differences"]):
        vals = [bar_df[(bar_df.indicator == ii) & (bar_df.spec == spec)]["median_r2"].iloc[0] for ii in inds]
        color = CAT["blue"] if spec == "Levels" else CAT["red"]
        bars = ax.bar(x + (i - 0.5) * width, vals, width, label=spec, color=color, alpha=0.88)
        ax.bar_label(bars, fmt="%.3f", padding=3, fontsize=9, color=INK_SECONDARY)
    ax.set_xticks(x); ax.set_xticklabels(inds)
    ax.set_ylabel("Median country-level R² vs. WHR happiness")
    ax.legend(frameon=False, fontsize=9)
    suptitle(fig, "C2. Does SHDI Show the Same Levels-Diffs Collapse as HDI?",
             "Same collapse design as the original analysis; both national indices tested against WHR happiness.")
    savefig(fig, "C2_collapse_bar_hdi_vs_shdi.png", SOURCE_WHR)

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
    ax.annotate(f"Pooled R² = {r2_all:.3f}  (n={panel[['shdi','stflife']].dropna().shape[0]} region-rounds)",
                xy=(0.03, 0.95), xycoords="axes fraction", fontsize=9, color=INK_SECONDARY)
    ax.set_xlabel("Subnational HDI (SHDI)"); ax.set_ylabel("Region-round mean Life Satisfaction")
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
    fig.supxlabel("SHDI (region mean across matched rounds)", fontsize=10)
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
    ax.set_xlabel("R² -- Levels (region x SHDI)"); ax.set_ylabel("R² -- Across-round differences")
    suptitle(fig, f"D3. Per-Region Collapse: stflife x SHDI (n={len(comp)} regions with >=5 rounds)")
    savefig(fig, "D3_collapse_scatter_regional.png", SOURCE_ESS)

    # D4: SHDI distribution by country (within-country heterogeneity)
    order = panel.groupby("cntry")["shdi"].median().sort_values(ascending=False).index.tolist()
    data = [panel[panel["cntry"] == c]["shdi"].dropna().values for c in order]
    fig, ax = plt.subplots(figsize=(13, 6.5))
    bp = ax.boxplot(data, tick_labels=order, patch_artist=True, widths=0.6, showfliers=False,
                     medianprops={"color": INK_PRIMARY, "linewidth": 1.2})
    for box in bp["boxes"]:
        box.set(facecolor=CAT["blue"], alpha=0.55, edgecolor=CAT["blue"])
    ax.set_ylabel("SHDI (region-round observations)")
    plt.setp(ax.get_xticklabels(), rotation=60, ha="right", fontsize=8)
    suptitle(fig, "D4. Within-Country Spread in Subnational HDI",
             "Wider boxes = more regional development inequality within that country.")
    savefig(fig, "D4_shdi_distribution_by_country.png", SOURCE_ESS)

    print(f"Section D: {len(panel)} region-round cells, {panel['gdl_region_name'].nunique()} distinct regions, "
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
        ax.set_ylabel("mean (country/region-round)")
    suptitle(fig, "E. Development vs. Two Mechanism Variables",
             "health is self-rated (1=very good...5=very bad, reverse of intuition -- check sign). "
             "ppltrst is 0-10 generalized trust. First look only; concept note's full mechanism model is a next step.")
    savefig(fig, "E1_mechanism_variables.png", SOURCE_ESS, top=0.87)


if __name__ == "__main__":
    section_a()
    section_b()
    section_c()
    section_d()
    section_e()
    print(f"\nAll figures saved to {OUT_DIR}/")
