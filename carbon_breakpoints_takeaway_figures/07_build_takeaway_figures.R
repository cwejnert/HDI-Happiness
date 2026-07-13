options(stringsAsFactors = FALSE)
suppressPackageStartupMessages({library(ggplot2); library(grid)})

root <- normalizePath(file.path(getwd(), "outputs"), winslash = "/", mustWork = TRUE)
dd <- file.path(root, "final_master", "derived")
od <- file.path(root, "final_master", "figures_takeaway")
os <- file.path(od, "supplement")
dir.create(od, recursive = TRUE, showWarnings = FALSE)
dir.create(os, recursive = TRUE, showWarnings = FALSE)

x <- read.csv(file.path(dd, "country_headline_final_classification.csv"))
panel <- read.csv(file.path(root, "global_harmonization/global_kaya_external_parent.csv"))
bs <- read.csv(file.path(root, "frozen_results_v1/breakpoint_bootstrap_summary.csv"))

# Palette: CVD-validated adjustment of the pipeline hues (direct labels everywhere).
kcols <- c("C/GDP" = "#3A66A5", "C/E" = "#2E8B57", "E/GDP" = "#C77F00")
col_policy <- "#1B7837"; col_other <- "#8A8A8A"; col_break <- "#B33A3A"
col_rio <- "#3A66A5"; col_paris <- "#2E7D32"; col_band <- "#D8E3EE"

theme_takeaway <- theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold", size = 17),
        plot.subtitle = element_text(color = "#555555", size = 11),
        panel.grid.minor = element_blank(), legend.position = "bottom",
        plot.margin = margin(12, 18, 12, 12))

save_both <- function(p, stem, w = 12, h = 7, supplemental = FALSE) {
  d <- if (supplemental) os else od
  ggsave(file.path(d, paste0(stem, ".png")), p, width = w, height = h, dpi = 300, bg = "white")
  if (capabilities("cairo")) { svg(file.path(d, paste0(stem, ".svg")), width = w, height = h, bg = "white"); print(p); dev.off() }
}
save_stack <- function(plots, heights, stem, w, h, supplemental = FALSE) {
  d <- if (supplemental) os else od
  draw <- function() {
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(length(plots), 1, heights = unit(heights, "null"))))
    for (i in seq_along(plots)) print(plots[[i]], vp = viewport(layout.pos.row = i, layout.pos.col = 1))
  }
  png(file.path(d, paste0(stem, ".png")), width = w, height = h, units = "in", res = 300, bg = "white")
  draw(); dev.off()
  if (capabilities("cairo")) { svg(file.path(d, paste0(stem, ".svg")), width = w, height = h, bg = "white"); draw(); dev.off() }
}

# Global aggregate Kaya series shared by Figures 1 and 2.
g <- aggregate(cbind(co2, primary_energy_consumption, gdp_usd) ~ Year, panel, FUN = sum, na.rm = TRUE)
g <- g[g$co2 > 0 & g$primary_energy_consumption > 0 & g$gdp_usd > 0, ]
hinge_fit <- function(z, bp) lm(value ~ Year + I(pmax(0, Year - bp)), data = z)
`%-na%` <- function(a, b) ifelse(is.na(a), b, a)

## Figure 1 — The global curve bent in the 1970s, not at Rio or Paris. ---------
g1 <- data.frame(Year = g$Year, value = log(g$co2 / g$gdp_usd))
g1 <- g1[g1$Year >= 1960 & is.finite(g1$value), ]
g1$index <- 100 * exp(g1$value - g1$value[g1$Year == min(g1$Year)])
bp_cgdp <- bs$grid_bp[bs$code == "WLD" & bs$variable == "log_C_GDP"]
f <- hinge_fit(transform(g1, value = log(index)), bp_cgdp)
g1$fit <- exp(predict(f))
sl <- coef(f); pre_pct <- 100 * (exp(sl[2]) - 1); post_pct <- 100 * (exp(sl[2] + sl[3]) - 1)
ymax <- max(g1$index)
p1a <- ggplot(g1, aes(Year, index)) +
  geom_vline(xintercept = c(1992, 2015), linetype = "dashed", color = c(col_rio, col_paris), linewidth = .7) +
  geom_point(color = "#8A8A8A", size = 1.7) +
  geom_line(aes(y = fit), color = col_break, linewidth = 1.3) +
  geom_vline(xintercept = bp_cgdp, color = col_break, linewidth = .9) +
  annotate("label", x = bp_cgdp, y = ymax * 1.04, label = paste0("Estimated break: ", bp_cgdp),
           color = col_break, fontface = "bold", size = 4.2, label.size = 0) +
  annotate("text", x = 1992, y = ymax * .97, label = "Rio 1992", color = col_rio, hjust = -.08, fontface = "bold", size = 3.8) +
  annotate("text", x = 2015, y = ymax * .97, label = "Paris 2015", color = col_paris, hjust = -.08, fontface = "bold", size = 3.8) +
  annotate("text", x = (min(g1$Year) + bp_cgdp)/2, y = 106,
           label = sprintf("%+.1f%% per year", pre_pct), color = "#333333", size = 3.6) +
  annotate("text", x = (bp_cgdp + max(g1$Year))/2, y = 62,
           label = sprintf("%+.1f%% per year", post_pct), color = "#333333", size = 3.6) +
  scale_y_log10() +
  labs(title = "The world's carbon-intensity curve bent in the early 1970s, decades before Rio or Paris",
       subtitle = paste0("Global CO2 per unit of GDP, indexed to ", min(g1$Year), " = 100 (log scale). ",
                         "The red line is a two-segment trend with a data-selected break year."),
       x = NULL, y = paste0("Global CO2 per unit of GDP (", min(g1$Year), " = 100)")) +
  theme_takeaway
w <- bs[bs$code == "WLD", ]
w$component <- sub(" \\(.*", "", w$indicator)
w$label <- factor(w$component, levels = rev(c("C/GDP", "C/E", "E/GDP")),
                  labels = rev(c("C/GDP: overall carbon intensity", "C/E: fuel mix (supply side)",
                                 "E/GDP: energy per GDP (demand side)")))
p1b <- ggplot(w, aes(grid_bp, label, color = component)) +
  geom_vline(xintercept = c(1992, 2015), linetype = "dashed", color = c(col_rio, col_paris), linewidth = .6) +
  geom_errorbarh(aes(xmin = boot_low, xmax = boot_high), height = .12, linewidth = 1.5) +
  geom_point(size = 4.5) +
  geom_label(aes(label = grid_bp), nudge_y = .3, size = 3.6, fontface = "bold", fill = "white", label.size = 0, show.legend = FALSE) +
  annotate("text", x = 2011, y = 2.62, label = "interval spans 1978-2011", color = "#555555", size = 3.2, hjust = 1) +
  scale_color_manual(values = kcols) +
  scale_x_continuous(breaks = seq(1965, 2020, 5), limits = range(c(w$boot_low, w$boot_high, 2016))) +
  labs(subtitle = "Each Kaya pathway's estimated global break year, with moving-block bootstrap 95% intervals",
       x = "Year", y = NULL) +
  theme_takeaway + theme(legend.position = "none")
save_stack(list(p1a, p1b), c(1.55, 1), "takeaway_fig01_global_bend_predates_treaties", 12, 9.5)

## Figure 2 — Many years look like turning points; few survive the placebo test. ----
g2 <- data.frame(Year = g$Year, value = log(g$co2 / g$primary_energy_consumption))
g2 <- g2[g2$Year >= 1965 & is.finite(g2$value), ]
cand <- (min(g2$Year) + 8):(max(g2$Year) - 8)
bic0 <- BIC(lm(value ~ Year, g2))
prof <- data.frame(year = cand, dbic = sapply(cand, function(b) bic0 - BIC(hinge_fit(g2, b))))
q90 <- quantile(prof$dbic, .9)
best <- prof[which.max(prof$dbic), ]
rio_row <- prof[prof$year == 1992, ]
p2a <- ggplot(prof, aes(year, dbic)) +
  geom_hline(yintercept = q90, linetype = "dotted", color = "#555555") +
  geom_line(color = "#3A66A5", linewidth = 1) +
  geom_point(color = "#3A66A5", size = 1.6) +
  geom_point(data = rio_row, color = col_break, size = 4) +
  annotate("text", x = 1992, y = rio_row$dbic + diff(range(prof$dbic)) * .09, label = "Rio 1992",
           color = col_break, fontface = "bold", size = 4) +
  annotate("text", x = max(prof$year), y = q90 + diff(range(prof$dbic)) * .05,
           label = "top decile of candidate years", color = "#555555", size = 3.3, hjust = 1) +
  labs(title = "Why a significant treaty-year break is weak evidence on its own",
       subtitle = "BIC improvement from placing the global fuel-mix (C/E) break in each candidate year (aggregate reconstruction): many years fit comparably well,\nwhich is exactly why the bootstrap interval in Figure 1 is so wide",
       x = "Candidate break year", y = "Model improvement (BIC points)") +
  theme_takeaway
ts <- read.csv(file.path(root, "global_harmonization/all_country_treaty_uniqueness_summary.csv"))
ts$treaty_lab <- factor(ifelse(ts$treaty == "UNFCCC/Rio", "Rio 1992", "Paris 2015"), levels = c("Rio 1992", "Paris 2015"))
sl2 <- rbind(
  data.frame(ts[, c("treaty_lab", "indicator")], stage = "Significant at the treaty date", share = ts$nominal_significant / ts$n_series, n = ts$nominal_significant),
  data.frame(ts[, c("treaty_lab", "indicator")], stage = "Also beats nearby placebo years", share = ts$uniquely_supported / ts$n_series, n = ts$uniquely_supported))
sl2$stage <- factor(sl2$stage, levels = c("Significant at the treaty date", "Also beats nearby placebo years"))
sl2$lab <- sprintf("%.0f%% (%d)", 100 * sl2$share, sl2$n)
grp <- interaction(sl2$treaty_lab, sl2$stage)
sl2$ny <- ave(sl2$share, grp, FUN = function(v) (rank(v, ties.method = "first") - (length(v) + 1) / 2) * .05) - sl2$share + sl2$share
sl2$ylab <- sl2$share + ave(sl2$share, grp, FUN = function(v) (rank(v, ties.method = "first") - (length(v) + 1) / 2) * .055)
p2b <- ggplot(sl2, aes(stage, share, group = indicator, color = indicator)) +
  geom_line(linewidth = 1.2) + geom_point(size = 3.4) +
  geom_text(aes(y = ylab, label = lab, hjust = ifelse(as.integer(stage) == 1, 1.15, -.15)), size = 3.3, show.legend = FALSE) +
  facet_wrap(~treaty_lab) +
  scale_color_manual(values = kcols) +
  scale_y_continuous(labels = scales::percent_format(), limits = c(0, .78)) +
  labs(subtitle = "Share of eligible country-component series surviving each evidentiary step",
       x = NULL, y = "Share of series", color = NULL) +
  theme_takeaway
save_stack(list(p2a, p2b), c(1.15, 1), "takeaway_fig02_placebo_test", 12, 10)

## Figure 3 — 97 countries, five decades, and the events that track them. ------
x <- x[order(x$bp, x$code), ]
x$stack <- ave(x$bp, x$bp, FUN = seq_along)
bands <- data.frame(
  xmin = c(1973, 1989, 1997, 2008, 2012), xmax = c(1980, 1995, 1999, 2010, 2020),
  lab = c("Oil shocks", "Post-Cold-War upheaval,\nliberalization & adjustment", "Asian\ncrisis", "Global financial\ncrisis", "Cheap renewables era"))
top <- max(x$stack) + 1.6
p3a <- ggplot() +
  geom_rect(data = bands, aes(xmin = xmin, xmax = xmax, ymin = 0, ymax = top), fill = col_band, alpha = .55) +
  geom_text(data = bands, aes(x = (xmin + xmax)/2, y = top + .4, label = lab), size = 3.1, color = "#41597A", lineheight = .9, vjust = 0) +
  geom_vline(xintercept = c(1992, 2015), linetype = "dashed", color = c(col_rio, col_paris), linewidth = .7) +
  annotate("text", x = 1992, y = -0.7, label = "Rio", color = col_rio, fontface = "bold", size = 3.6) +
  annotate("text", x = 2015, y = -0.7, label = "Paris", color = col_paris, fontface = "bold", size = 3.6) +
  geom_point(data = x[!x$policy_enabled, ], aes(bp, stack), color = col_other, size = 2.9) +
  geom_point(data = x[x$policy_enabled, ], aes(bp, stack), color = col_policy, shape = 17, size = 3.6) +
  scale_x_continuous(breaks = seq(1960, 2020, 10)) +
  coord_cartesian(ylim = c(-1.2, top + 2.2), clip = "off") +
  labs(title = "97 national breakpoints across five decades: tracking economic history, not treaty dates",
       subtitle = "One dot per country (statistically selected headline break). Green triangles: the 9 policy-enabled low-carbon cases. Shaded bands: major economic and political episodes.",
       x = "Estimated breakpoint year", y = NULL) +
  theme_takeaway + theme(axis.text.y = element_blank(), panel.grid.major.y = element_blank())
ev <- read.csv(file.path(root, "global_mechanisms/reconciled_event_random_timing_tests.csv"))
ev$criterion <- factor(ev$metric, levels = rev(c("within2", "within5", "inside_episode")),
                       labels = rev(c("Documented event within 2 years", "Documented event within 5 years", "Break inside the documented episode")))
ev$expected <- ev$random_mean / ev$n; ev$lo <- ev$random_low / ev$n; ev$hi <- ev$random_high / ev$n
p3b <- ggplot(ev, aes(y = criterion)) +
  geom_segment(aes(x = expected, xend = observed_share, yend = criterion), color = "#BDBDBD", linewidth = 1.2) +
  geom_errorbarh(aes(xmin = lo, xmax = hi), height = .12, color = "#3A66A5", linewidth = 1.1) +
  geom_point(aes(x = expected), color = "#3A66A5", size = 3.4) +
  geom_point(aes(x = observed_share), color = col_break, size = 4.4) +
  geom_text(aes(x = observed_share, label = paste0(round(100 * observed_share), "% observed")),
            nudge_x = .03, hjust = 0, size = 3.5, fontface = "bold", color = col_break) +
  geom_text(aes(x = expected, label = paste0(round(100 * expected), "% by chance")),
            nudge_y = -.24, size = 3.2, color = "#31598A") +
  scale_x_continuous(labels = scales::percent_format(), limits = c(0, 1)) +
  labs(subtitle = "And the breaks are not arbitrary: among 71 documented episodes, historical events sit near the estimated breaks far more often than chance",
       x = "Share of episodes matched", y = NULL) +
  theme_takeaway
save_stack(list(p3a, p3b), c(1.7, 1), "takeaway_fig03_when_and_why_curves_bend", 13, 10)

## Figure 4 — What accompanied the bends: a census of 97 countries. ------------
md <- as.data.frame(table(x$mechanism_main)); names(md) <- c("mechanism", "n")
lab_map <- c("Fossil-fuel and energy-market transformation" = "Fuel & energy markets changed",
             "Economic and sectoral restructuring" = "The economy restructured",
             "Political/geopolitical disruption" = "Political disruption or conflict",
             "Macroeconomic shock" = "Macroeconomic shock",
             "Development demographic and energy-access transition" = "Development & energy access",
             "Policy-enabled low-carbon transformation" = "Climate policy & low-carbon technology",
             "Other/undefined" = "Unresolved: no documented match")
row_order <- c("Fossil-fuel and energy-market transformation", "Economic and sectoral restructuring",
               "Political/geopolitical disruption", "Macroeconomic shock",
               "Development demographic and energy-access transition",
               "Policy-enabled low-carbon transformation", "Other/undefined")
md$label <- factor(lab_map[as.character(md$mechanism)], levels = rev(lab_map[row_order]))
md$fill <- ifelse(as.character(md$mechanism) == "Policy-enabled low-carbon transformation", "policy",
                  ifelse(as.character(md$mechanism) == "Other/undefined", "unresolved", "other"))
cells <- do.call(rbind, lapply(seq_len(nrow(md)), function(i) data.frame(label = md$label[i], fill = md$fill[i], pos = seq_len(md$n[i]))))
p4 <- ggplot(cells, aes(pos, label, fill = fill)) +
  geom_tile(width = .82, height = .68, color = "white") +
  geom_text(data = md, aes(x = n + .8, y = label, label = paste0(n, " of 97")), inherit.aes = FALSE, hjust = 0, size = 3.9, color = "#333333") +
  annotate("text", x = 13, y = which(levels(md$label) == "Climate policy & low-carbon technology"),
           label = "the policy signal: real, but rare", color = col_policy, fontface = "bold.italic", size = 3.7, hjust = 0) +
  scale_fill_manual(values = c(other = "#7392B5", policy = col_policy, unresolved = "#C9C9C9")) +
  scale_x_continuous(limits = c(0, 27), expand = c(0, 0)) +
  labs(title = "What accompanied the 97 bends? Mostly markets, restructuring, disruption",
       subtitle = "One square per country: the best-supported historical mechanism for each statistically selected headline breakpoint",
       x = NULL, y = NULL) +
  theme_takeaway + theme(legend.position = "none", axis.text.x = element_blank(),
                         panel.grid = element_blank(), axis.text.y = element_text(size = 11))
save_both(p4, "takeaway_fig04_mechanism_census", 12, 5.8)

## Figure 5 — Bending the curve is not the same as cutting emissions. ----------
x$imp <- -sign(x$slope_change) * abs(x$standardized_slope_change)
x$em <- 100 * x$absolute_emissions_post_slope
z5 <- x[is.finite(x$imp) & is.finite(x$em), ]
qn <- table(factor(paste(z5$imp > 0, z5$em < 0), levels = c("TRUE TRUE", "TRUE FALSE", "FALSE TRUE", "FALSE FALSE"),
                   labels = c("iF", "iR", "wF", "wR")))
big <- c("USA", "CHN", "IND", "DEU", "JPN", "RUS")
xr <- range(z5$imp); yr <- range(z5$em)
p5 <- ggplot(z5, aes(imp, em)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "#777777") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "#777777") +
  geom_point(data = z5[!z5$policy_enabled, ], color = col_other, size = 2.7, alpha = .8) +
  geom_point(data = z5[z5$policy_enabled, ], color = col_policy, shape = 17, size = 4) +
  geom_text(data = transform(z5[z5$policy_enabled, ],
              imp = imp + c(CHE = -.09, SWE = .09, FIN = -.13)[code] %-na% 0,
              em  = em + ifelse(code == "FIN", -diff(yr) * .04, diff(yr) * .035)),
            aes(label = code), color = col_policy, fontface = "bold", size = 3.3) +
  geom_text(data = z5[z5$code %in% big, ], aes(label = code), color = "#555555", nudge_y = diff(yr) * .035, size = 3) +
  annotate("text", x = xr[2] * .98, y = yr[1] * .96, hjust = 1, color = "#1B5E20", fontface = "bold", size = 3.8,
           label = sprintf("Intensity improved AND\nemissions falling (%d)", qn["iF"])) +
  annotate("text", x = xr[2] * .98, y = yr[2] * .96, hjust = 1, color = "#8A6D00", fontface = "bold", size = 3.8,
           label = sprintf("Intensity improved, but\nemissions still rising (%d)", qn["iR"])) +
  annotate("text", x = xr[1] * .98, y = yr[1] * .96, hjust = 0, color = "#555555", size = 3.6,
           label = sprintf("Intensity worsened,\nemissions falling (%d)", qn["wF"])) +
  annotate("text", x = xr[1] * .98, y = yr[2] * .96, hjust = 0, color = "#8A3A36", fontface = "bold", size = 3.8,
           label = sprintf("Intensity worsened AND\nemissions rising (%d)", qn["wR"])) +
  labs(title = "A favorable bend is not yet a success: intensity often improves while emissions keep rising",
       subtitle = "Green triangles: the 9 policy-enabled cases. Only 9 of 97 countries qualify as constructive, persistent decarbonization once persistence and mechanism are also required.",
       x = "Improvement in the intensity slope after the break (standardized; positive = improvement)",
       y = "Post-break trend in absolute CO2 (% per year)") +
  theme_takeaway
save_both(p5, "takeaway_fig05_bend_vs_success", 12, 8)

## Figure 6 — External raters recognize the same countries (thin coverage). ----
rat <- rbind(data.frame(code = x$code, source = "Climate Action\nTracker\n(26 covered)", policy = x$policy_enabled, score = x$cat_score),
             data.frame(code = x$code, source = "Climate Change\nPerformance Index\n(18 covered)", policy = x$policy_enabled, score = x$overall_score))
rat <- rat[is.finite(rat$score), ]
ordinal <- function(v) { v <- round(v); suf <- ifelse(v %% 100 %in% 11:13, "th", c("th","st","nd","rd", rep("th", 6))[v %% 10 + 1]); paste0(v, suf) }
rat$pct <- ave(rat$score, rat$source, FUN = function(v) 100 * (rank(v, ties.method = "average") - 1) / (length(v) - 1))
rat$ypos <- as.numeric(factor(rat$source))
meds <- aggregate(pct ~ source + policy, rat, median)
meds$ypos <- as.numeric(factor(meds$source, levels = levels(factor(rat$source))))
set.seed(7)
rat$yjit <- rat$ypos + ifelse(rat$policy, 0, runif(nrow(rat), -.12, .12))
p6 <- ggplot(rat, aes(pct, ypos)) +
  geom_segment(data = meds, aes(x = pct, xend = pct, y = ypos - .26, yend = ypos + .26, color = policy), linewidth = 1.1) +
  geom_point(data = rat[!rat$policy, ], aes(y = yjit), color = col_other, size = 2.8, alpha = .85) +
  geom_point(data = transform(rat[rat$policy, ],
               ypos = ypos + ave(pct, source, FUN = function(v) ifelse(duplicated(v) | duplicated(v, fromLast = TRUE), (rank(v, ties.method = "first") - mean(rank(v))) * .16, 0))),
             color = col_policy, shape = 17, size = 4.4) +
  geom_text(data = transform(rat[rat$policy, ],
              ypos = ypos + .3 + ave(pct, source, FUN = function(v) (rank(v, ties.method = "first") - 1) %% 2) * .14,
              pct = pct + ave(pct, source, FUN = function(v) ifelse(duplicated(v) | duplicated(v, fromLast = TRUE), (rank(v, ties.method = "first") - mean(rank(v))) * 6, 0))),
            aes(label = code), color = col_policy, fontface = "bold", size = 3.4) +
  geom_text(data = meds, aes(label = paste0(ifelse(policy, "policy median: ", "others' median: "), ordinal(pct)), color = policy),
            nudge_y = -.42, size = 3.1, fontface = "italic") +
  scale_color_manual(values = c(`TRUE` = col_policy, `FALSE` = "#777777"), guide = "none") +
  scale_x_continuous(limits = c(-3, 103)) +
  scale_y_continuous(breaks = sort(unique(rat$ypos)), labels = levels(factor(rat$source)), limits = c(.45, 2.55)) +
  labs(title = "Independent climate raters rank the policy-enabled cases high, but coverage is thin",
       subtitle = "External-rating percentile among covered countries. Green triangles: policy-enabled cases (CAT covers 3 of 9; CCPI covers 2). Corroborative, not definitive.",
       x = "Percentile of external climate rating within the covered sample (higher = better rating)", y = NULL) +
  theme_takeaway + theme(plot.title.position = "plot", axis.text.y = element_text(size = 10, lineheight = .95))
save_both(p6, "takeaway_fig06_external_corroboration", 12, 5.6)

## Supplement S1 — consumption vs production timing. ---------------------------
cv <- read.csv(file.path(root, "global_harmonization/consumption_max_overlap/consumption_vs_production_global.csv"))
cv <- cv[cv$both_eligible %in% TRUE, ]
cv <- cv[order(cv$date_difference), ]; cv$country <- factor(cv$country, levels = cv$country)
med_gap <- median(abs(cv$date_difference))
pS1 <- ggplot(cv, aes(y = country)) +
  geom_segment(aes(x = bp_production_CGDP, xend = bp_consumption, yend = country), color = "#BDBDBD", linewidth = 1.1) +
  geom_point(aes(x = bp_production_CGDP), color = "#3A66A5", size = 3.2) +
  geom_point(aes(x = bp_consumption), color = col_break, size = 3.2) +
  labs(title = "Trade accounting moves the apparent start of national transitions",
       subtitle = sprintf("Blue: production-based break. Red: consumption-based break. Only %d of %d agree within five years; median gap %.0f years.\nConsumption-based series begin in 1990, so very early production-based breaks cannot be matched by construction.",
                          sum(cv$within_5yr), nrow(cv), med_gap),
       x = "Estimated breakpoint year", y = NULL) + theme_takeaway
save_both(pS1, "takeaway_figS01_consumption_accounting", 10, 7, TRUE)

## Supplement S2 — E/GDP attribution. ------------------------------------------
sr <- read.csv(file.path(root, "global_harmonization/sector_recession_max_overlap/egdp_breakpoint_attribution.csv"))
st <- as.data.frame(sort(table(sr$attribution_class))); names(st) <- c("class", "n")
pS2 <- ggplot(st, aes(n, class)) +
  geom_segment(aes(x = 0, xend = n, yend = class), color = "#D0D0D0", linewidth = 1) +
  geom_point(size = 4, color = "#3A66A5") + geom_text(aes(label = n), nudge_x = 1, size = 3.8) +
  scale_x_continuous(expand = expansion(mult = c(0, .1))) +
  labs(title = "Demand-side (E/GDP) breaks often align with recession or sectoral change",
       subtitle = sprintf("Available-case attribution for %d eligible E/GDP breaks", nrow(sr)),
       x = "Countries", y = NULL) + theme_takeaway
save_both(pS2, "takeaway_figS02_egdp_attribution", 11, 5.5, TRUE)

cat("Takeaway figures written to", od, "\n")
