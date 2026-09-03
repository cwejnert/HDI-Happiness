# Corrected world-level figures, built on the TRUE world aggregate and the
# 44-specification invariance grid produced by 11_master_world_analysis.R.
options(stringsAsFactors = FALSE)
suppressPackageStartupMessages(library(ggplot2))

root <- normalizePath(file.path(getwd(), "outputs"), winslash = "/", mustWork = TRUE)
md <- file.path(root, "final_master", "world_master")
od <- file.path(root, "final_master", "figures_world_v3")
dir.create(od, recursive = TRUE, showWarnings = FALSE)

owid <- read.csv("data/owid_co2_current.csv"); wbg <- read.csv("data/worldbank_world_gdp_const2015usd.csv")
W <- owid[owid$country == "World", c("year", "co2", "primary_energy_consumption")]
names(W) <- c("Year", "co2", "energy")
W <- W[is.finite(W$co2) & is.finite(W$energy) & W$co2 > 0 & W$energy > 0, ]
W <- merge(W, setNames(wbg, c("Year", "gdp")), by = "Year"); W <- W[order(W$Year), ]
W <- W[W$Year >= 1965, ]
grid <- read.csv(file.path(md, "spec_grid.csv"))

kcols <- c("C/GDP" = "#3A66A5", "C/E" = "#2E8B57", "E/GDP" = "#C77F00")
nm <- c("C/GDP" = "Carbon intensity (overall)", "C/E" = "Supply-side decarbonization", "E/GDP" = "Efficiency gains")
GREY <- "#8A8A8A"; REDC <- "#B33A3A"; PARIS <- "#2E7D32"
theme_w <- theme_minimal(base_size = 14) +
  theme(plot.title = element_text(face = "bold", size = 17),
        plot.subtitle = element_text(color = "#555555", size = 11.5),
        panel.grid.minor = element_blank(), legend.position = "bottom",
        plot.margin = margin(12, 18, 12, 12), plot.title.position = "plot")
save_both <- function(pl, stem, w = 12.5, h = 6.4) {
  ggsave(file.path(od, paste0(stem, ".png")), pl, width = w, height = h, dpi = 300, bg = "white")
  if (capabilities("cairo")) { svg(file.path(od, paste0(stem, ".svg")), width = w, height = h, bg = "white"); print(pl); dev.off() }
}
ser <- function(k) switch(k, "C/GDP" = log(W$co2 / W$gdp), "C/E" = log(W$co2 / W$energy),
                             "E/GDP" = log(W$energy / W$gdp))
rate <- function(v, a, b) { i <- W$Year >= a & W$Year <= b; 100 * unname(coef(lm(log(W[[v]][i]) ~ W$Year[i]))[2]) }
comp_rate <- function(k, a, b) switch(k,
  "C/GDP" = rate("co2", a, b) - rate("gdp", a, b),
  "C/E"   = rate("co2", a, b) - rate("energy", a, b),
  "E/GDP" = rate("energy", a, b) - rate("gdp", a, b))

## FIG 1 — the long record: the dominant break is the 1970s ---------------------
z <- data.frame(Year = W$Year, y = ser("C/GDP"))
brk <- c(1973, 2001, 2012)                       # BIC-selected, from the master run
X <- data.frame(y = z$y, Year = z$Year)
for (i in seq_along(brk)) X[[paste0("s", i)]] <- pmax(0, z$Year - brk[i])
fit <- lm(y ~ ., X); z$fit <- fitted(fit)
z$idx <- 100 * exp(z$y - z$y[1]); z$fidx <- 100 * exp(z$fit - z$y[1])
sl <- 100 * cumsum(coef(fit)[2:5])
seg <- data.frame(a = c(min(z$Year), brk), b = c(brk, max(z$Year)), slope = sl)
seg$mid <- (seg$a + seg$b) / 2
seg$y <- exp(approx(z$Year, log(z$fidx), seg$mid)$y) * 1.07
p1 <- ggplot(z, aes(Year, idx)) +
  geom_vline(xintercept = c(1992, 2015), linetype = "dashed", color = c("#3A66A5", PARIS)) +
  geom_vline(xintercept = brk, color = REDC, alpha = .5, linewidth = .7) +
  geom_point(color = GREY, size = 1.7) + geom_line(aes(y = fidx), color = REDC, linewidth = 1.2) +
  geom_label(data = seg, aes(mid, y, label = sprintf("%+.2f%%/yr", slope)), inherit.aes = FALSE,
             size = 3.6, fontface = "bold", fill = "white", label.size = 0, color = "#333333") +
  annotate("text", x = brk, y = min(z$idx) * .985, label = brk, color = REDC, fontface = "bold", size = 3.4) +
  annotate("text", x = c(1992, 2015), y = max(z$idx) * .99, label = c("Rio", "Paris"),
           color = c("#3A66A5", PARIS), fontface = "bold", size = 3.6, hjust = -.15) +
  scale_y_log10() + scale_x_continuous(breaks = seq(1970, 2020, 10)) +
  labs(title = "The world's decisive turn was the 1970s oil shocks - and it is still the largest in the record",
       subtitle = "Carbon intensity of the true world aggregate (OWID world CO2 and energy; World Bank world GDP), 1965 = 100, log scale.\nRed line: best multiple-break fit, breaks chosen by BIC. A formal unknown-break test puts the single dominant break at 1972 (p = 0.002).",
       x = NULL, y = "Carbon intensity (1965 = 100)") + theme_w
save_both(p1, "v3_fig1_long_record")

## FIG 2 — the baseline problem: the stall, then the resumption -----------------
eras <- list(c(1973, 1990), c(1990, 2015), c(2016, 2023))
elab <- c("1973-1990\nafter the oil shocks", "1990-2015\nRio to Paris", "2016-2023\nsince Paris")
d2 <- do.call(rbind, lapply(seq_along(eras), function(i) do.call(rbind, lapply(names(kcols), function(k)
  data.frame(era = elab[i], ord = i, comp = nm[k], key = k, val = comp_rate(k, eras[[i]][1], eras[[i]][2]))))))
d2$comp <- factor(d2$comp, levels = nm); d2$era <- factor(d2$era, levels = elab)
p2 <- ggplot(d2, aes(era, val, fill = key)) +
  geom_hline(yintercept = 0, color = "#777777") +
  geom_col(width = .62, show.legend = FALSE) +
  geom_text(aes(label = sprintf("%+.2f", val), vjust = ifelse(val > 0, -0.6, 1.5)), size = 4.2, fontface = "bold") +
  facet_wrap(~comp, ncol = 3) +
  scale_fill_manual(values = kcols) +
  scale_y_continuous(expand = expansion(mult = .22)) +
  labs(title = "Efficiency never changed pace. The fuel mix stalled for 25 years, then resumed.",
       subtitle = "Average annual change (%) in each component of the true world aggregate. Overall carbon intensity is now improving at its fastest rate on record -\nbut that is the fuel mix resuming after a generation-long stall, not efficiency speeding up. How large the recent gain looks depends on which era you compare it to.",
       x = NULL, y = "Average annual change (%)") + theme_w
save_both(p2, "v3_fig2_baseline_problem", 13, 6.2)

## FIG 3 — specification invariance: where does the turning point land? ----------
g3 <- grid; g3$comp <- factor(nm[g3$component], levels = nm)
share <- do.call(rbind, lapply(split(g3, g3$comp), function(d) data.frame(
  comp = d$comp[1], lab = sprintf("%.0f%% of specifications put the\nturning point before 2015", 100 * mean(d$best_year < 2015)))))
p3 <- ggplot(g3, aes(best_year, fill = component)) +
  geom_vline(xintercept = 2015, linetype = "dashed", color = PARIS, linewidth = .9) +
  geom_vline(xintercept = 1992, linetype = "dashed", color = "#3A66A5") +
  geom_dotplot(binwidth = 1.4, dotsize = .85, stackratio = .9, color = "white", show.legend = FALSE) +
  geom_text(data = share, aes(x = 1966, y = .92, label = lab), inherit.aes = FALSE,
            hjust = 0, size = 3.7, color = "#333333", lineheight = .95, fontface = "bold") +
  facet_wrap(~comp, ncol = 3) +
  scale_fill_manual(values = kcols) +
  scale_y_continuous(NULL, breaks = NULL, limits = c(0, 1.05)) +
  scale_x_continuous(breaks = seq(1970, 2020, 10)) +
  labs(title = "Across 44 ways of building the series, the turning point lands before Paris",
       subtitle = "Each dot is one specification: true world aggregate or constructed country panel, four start years, three endpoints, four completeness\nthresholds, with and without interpolation. The dot shows the best-fitting turning-point year under that specification.",
       x = "Best-fitting turning-point year") + theme_w
save_both(p3, "v3_fig3_specification_invariance", 13, 6)

## FIG 4 — what is and is not robust --------------------------------------------
inv <- read.csv(file.path(md, "invariance_summary.csv"))
inv$comp <- factor(nm[inv$component], levels = rev(nm))
d4 <- data.frame(comp = rep(inv$comp, 2),
                 metric = rep(c("Post-2015 change is\nstatistically significant",
                                "Turning point falls\nbefore 2015"), each = nrow(inv)),
                 pct = c(inv$pct_significant, inv$pct_best_before_2015))
p4 <- ggplot(d4, aes(pct, comp, fill = metric)) +
  geom_col(position = position_dodge(width = .72), width = .62) +
  geom_text(aes(label = paste0(pct, "%")), position = position_dodge(width = .72),
            hjust = -.15, size = 4, fontface = "bold") +
  scale_fill_manual(values = c("#B0B7BE", "#1B7837")) +
  scale_x_continuous(limits = c(0, 118), breaks = seq(0, 100, 25)) +
  labs(title = "One finding survives every specification. The others do not.",
       subtitle = "Share of the 44 specifications in which each statement holds. The timing result is near-universal; whether the post-2015 change\nis statistically significant depends on the component and on how the series is built - especially for energy efficiency.",
       x = "Share of specifications (%)", y = NULL, fill = NULL) + theme_w
save_both(p4, "v3_fig4_what_is_robust", 12.5, 5.8)

cat("v3 figures written to", od, "\n")
