# Paris-reframe figures: the null as a diagnostic, not an indictment.
# Requires only outputs/global_harmonization/global_kaya_external_parent.csv.
options(stringsAsFactors = FALSE)
suppressPackageStartupMessages(library(ggplot2))

root <- normalizePath(file.path(getwd(), "outputs"), winslash = "/", mustWork = TRUE)
od <- file.path(root, "final_master", "figures_takeaway")
dir.create(od, recursive = TRUE, showWarnings = FALSE)

panel <- read.csv(file.path(root, "global_harmonization/global_kaya_external_parent.csv"))
g <- aggregate(cbind(co2, primary_energy_consumption, gdp_usd) ~ Year, panel, sum, na.rm = TRUE)
g <- g[g$co2 > 0 & g$primary_energy_consumption > 0 & g$gdp_usd > 0, ]

kcols <- c("C/GDP" = "#3A66A5", "C/E" = "#2E8B57", "E/GDP" = "#C77F00")
col_obs <- "#B33A3A"; col_paris <- "#2E7D32"
theme_takeaway <- theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold", size = 17),
        plot.subtitle = element_text(color = "#555555", size = 11),
        panel.grid.minor = element_blank(), legend.position = "bottom",
        plot.margin = margin(12, 18, 12, 12), plot.title.position = "plot")
save_both <- function(p, stem, w = 12, h = 7) {
  ggsave(file.path(od, paste0(stem, ".png")), p, width = w, height = h, dpi = 300, bg = "white")
  if (capabilities("cairo")) { svg(file.path(od, paste0(stem, ".svg")), width = w, height = h, bg = "white"); print(p); dev.off() }
}

series <- data.frame(Year = rep(g$Year, 3),
                     component = rep(c("C/GDP", "C/E", "E/GDP"), each = nrow(g)),
                     y = c(log(g$co2 / g$gdp_usd), log(g$co2 / g$primary_energy_consumption),
                           log(g$primary_energy_consumption / g$gdp_usd)))
series <- series[series$Year >= 1990 & is.finite(series$y), ]
series$component <- factor(series$component, levels = c("C/GDP", "C/E", "E/GDP"))

## Figure 2A: is post-Paris intensity falling faster than the pre-Paris trend predicts?
proj <- do.call(rbind, lapply(levels(series$component), function(k) {
  z <- series[series$component == k, ]
  base <- z[z$Year <= 2015, ]
  fit <- lm(y ~ Year, base)
  z$fitline <- predict(fit, newdata = z)
  pi <- predict(fit, newdata = z, interval = "prediction")
  z$lo <- pi[, 2]; z$hi <- pi[, 3]
  ref <- base$y[base$Year == 1990]
  z$idx <- 100 * exp(z$y - ref); z$fidx <- 100 * exp(z$fitline - ref)
  z$loidx <- 100 * exp(z$lo - ref); z$hiidx <- 100 * exp(z$hi - ref)
  z$dev <- 100 * (z$y - z$fitline)
  z
}))
dev_note <- aggregate(dev ~ component, proj[proj$Year > 2015, ], mean)
dev_note$lab <- sprintf("post-2015 average: %+.1f%% vs trend", dev_note$dev)
dev_note$Year <- 1991; dev_note$idx <- 100 * exp(apply(
  sapply(dev_note$component, function(k) range(log(proj$idx[proj$component == k] / 100))), 2, min)) * 1.02
# place the note near the bottom of each panel
dev_note$idx <- sapply(dev_note$component, function(k) min(proj$idx[proj$component == k]) * 1.02)
p2a <- ggplot(proj, aes(Year, idx)) +
  geom_ribbon(data = proj[proj$Year >= 2015, ], aes(ymin = loidx, ymax = hiidx, fill = component), alpha = .15, show.legend = FALSE) +
  geom_line(data = proj[proj$Year <= 2015, ], aes(y = fidx, color = component), linewidth = 1, show.legend = FALSE) +
  geom_line(data = proj[proj$Year >= 2015, ], aes(y = fidx, color = component), linewidth = 1, linetype = "22", show.legend = FALSE) +
  geom_point(aes(color = component), size = 1.6, show.legend = FALSE) +
  geom_point(data = proj[proj$Year > 2015, ], color = col_obs, size = 2.4) +
  geom_vline(xintercept = 2015, linetype = "dashed", color = col_paris) +
  geom_text(data = dev_note, aes(label = lab), hjust = 0, size = 3.4, color = "#333333") +
  annotate("text", x = 2015.4, y = Inf, label = "Paris", color = col_paris, fontface = "bold",
           hjust = 0, vjust = 1.4, size = 3.6) +
  facet_wrap(~component, ncol = 3, scales = "free_y") +
  scale_color_manual(values = kcols) + scale_fill_manual(values = kcols) +
  scale_y_log10() +
  labs(title = "Ten years on, global intensity is falling almost exactly as the pre-Paris trend predicted",
       subtitle = "Each panel: 1990 = 100 (log scale). Solid line: 1990-2015 trend; dashed: its extrapolation with a 95% prediction band; red points: observed after Paris.\nA Paris effect on realized outcomes must eventually appear as an acceleration below this band - it has not yet.",
       x = NULL, y = "Index (1990 = 100)") +
  theme_takeaway
save_both(p2a, "takeaway_fig02a_paris_and_the_long_trend", 13, 6)

## Figure 2B: the stabilization arithmetic.
sl <- function(v, yrs) { z <- g[g$Year >= yrs[1] & g$Year <= yrs[2], ]; unname(coef(lm(log(z[[v]]) ~ z$Year))[2]) * 100 }
eras <- list(`1990-2015 (Rio to Paris)` = c(1990, 2015), `2016-2023 (after Paris)` = c(2016, 2023))
ar <- do.call(rbind, lapply(names(eras), function(e) {
  y <- eras[[e]]
  gdp <- sl("gdp_usd", y); co2 <- sl("co2", y)
  ce <- sl("co2", y) - sl("primary_energy_consumption", y)
  eg <- sl("primary_energy_consumption", y) - sl("gdp_usd", y)
  data.frame(era = e,
             part = c("GDP growth", "Fuel mix (C/E)", "Energy intensity (E/GDP)", "= CO2 emissions"),
             val = c(gdp, ce, eg, co2), gdp = gdp)
}))
ar$part <- factor(ar$part, levels = rev(c("GDP growth", "Fuel mix (C/E)", "Energy intensity (E/GDP)", "= CO2 emissions")))
pcols <- c("GDP growth" = "#8A8A8A", "Fuel mix (C/E)" = "#2E8B57",
           "Energy intensity (E/GDP)" = "#C77F00", "= CO2 emissions" = "#B33A3A")
need <- unique(ar[, c("era", "gdp")])
p2b <- ggplot(ar, aes(val, part, fill = part)) +
  geom_col(width = .62, show.legend = FALSE) +
  geom_vline(xintercept = 0, color = "#555555") +
  geom_vline(data = need, aes(xintercept = -gdp), linetype = "dotted", color = "#333333", linewidth = .8) +
  geom_text(aes(label = sprintf("%+.1f%%", val), hjust = ifelse(val > 0, -.15, 1.15)), size = 3.8) +
  geom_text(data = need, aes(x = -gdp, y = .62, label = "intensity decline needed\nto hold emissions flat"),
            inherit.aes = FALSE, size = 3, color = "#333333", hjust = 0, nudge_x = .08, lineheight = .95) +
  facet_wrap(~era) +
  scale_fill_manual(values = pcols) +
  scale_x_continuous(expand = expansion(mult = .22)) +
  labs(title = "The arithmetic of bending the curve: intensity must fall as fast as GDP grows",
       subtitle = "Average annual log growth rates of the global Kaya terms. CO2 growth = GDP growth + fuel-mix change + energy-intensity change,\nso the emissions curve cannot bend until the two intensity slopes accelerate - which is where any policy signal must appear first.",
       x = "Average annual change (%)", y = NULL) +
  theme_takeaway
save_both(p2b, "takeaway_fig02b_stabilization_arithmetic", 13, 6)

## Detectability note: how big a post-2015 acceleration could the data even show yet?
det <- lapply(levels(series$component), function(k) {
  z <- series[series$component == k, ]
  fit <- lm(y ~ Year + I(pmax(0, Year - 2015)), z)
  se <- summary(fit)$coefficients[3, 2] * 100
  sprintf("%s: minimum detectable post-2015 slope change (95%%, ~50%% power) about %.2f pp/yr; for 80%% power about %.2f pp/yr", k, 1.96 * se, 2.8 * se)
})
writeLines(c("Post-Paris detectability with data through 2023 (hinge-at-2015 model on 1990-2023):",
             unlist(det),
             "Compare: the entire post-1973 global C/GDP trend is about -0.8%/yr."),
           file.path(od, "paris_detectability_note.txt"))
cat(readLines(file.path(od, "paris_detectability_note.txt")), sep = "\n")
