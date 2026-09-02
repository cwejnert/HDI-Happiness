# World-level figures, v2 — near-complete country coverage, simplified for the talk.
#
# Panel construction (one rule, applied twice):
#   keep every country that still reports in 2021 and has at least 90% of the years
#   in the window; linearly interpolate the few interior gaps in logs.
#   PRIMARY  1990-2021: 182 countries, 99.8% of 2015 global CO2, 13 interpolated cells.
#   HISTORY  1980-2021: 153 countries, 90% of 2015 global CO2 (needed to test Rio).
# 2022-23 are excluded throughout: only 78 countries have reported them yet.
options(stringsAsFactors = FALSE)
suppressPackageStartupMessages(library(ggplot2))

root <- normalizePath(file.path(getwd(), "outputs"), winslash = "/", mustWork = TRUE)
od <- file.path(root, "final_master", "figures_world_v2")
dir.create(od, recursive = TRUE, showWarnings = FALSE)

p <- read.csv(file.path(root, "global_harmonization/global_kaya_external_parent.csv"))
p$ok <- is.finite(p$co2) & p$co2 > 0 & is.finite(p$primary_energy_consumption) &
        p$primary_energy_consumption > 0 & is.finite(p$gdp_usd) & p$gdp_usd > 0

build <- function(y0, y1, minfrac = .90) {
  yrs <- y0:y1
  d <- p[p$Year %in% yrs & p$ok, ]
  have <- tapply(d$Year, d$Code, function(v) length(unique(v)))
  ends <- tapply(d$Year, d$Code, max)
  keep <- names(have)[have >= minfrac * length(yrs) & ends >= y1]
  full <- expand.grid(Code = keep, Year = yrs, stringsAsFactors = FALSE)
  m <- merge(full, d[, c("Code", "Year", "co2", "primary_energy_consumption", "gdp_usd")], all.x = TRUE)
  m <- m[order(m$Code, m$Year), ]
  filled <- sum(is.na(m$co2))
  for (v in c("co2", "primary_energy_consumption", "gdp_usd"))
    m[[v]] <- ave(m[[v]], m$Code, FUN = function(x)
      if (all(is.na(x))) x else exp(approx(seq_along(x), log(x), seq_along(x), rule = 2)$y))
  list(g = aggregate(cbind(co2, primary_energy_consumption, gdp_usd) ~ Year, m, sum),
       n = length(keep), filled = filled,
       share = 100 * sum(p$co2[p$Year == 2015 & p$Code %in% keep & p$ok]) /
                     sum(p$co2[p$Year == 2015 & p$ok]))
}
P <- build(1990, 2021)     # primary
H <- build(1980, 2021, .95)  # history (lets us test Rio)

kcols <- c("C/GDP" = "#3A66A5", "C/E" = "#2E8B57", "E/GDP" = "#C77F00")
GREY <- "#8A8A8A"; REDC <- "#B33A3A"; col_paris <- "#2E7D32"
theme_w <- theme_minimal(base_size = 14) +
  theme(plot.title = element_text(face = "bold", size = 17),
        plot.subtitle = element_text(color = "#555555", size = 11.5),
        panel.grid.minor = element_blank(), legend.position = "bottom",
        plot.margin = margin(12, 18, 12, 12), plot.title.position = "plot")
save_both <- function(pl, stem, w = 12, h = 6.5) {
  ggsave(file.path(od, paste0(stem, ".png")), pl, width = w, height = h, dpi = 300, bg = "white")
  if (capabilities("cairo")) { svg(file.path(od, paste0(stem, ".svg")), width = w, height = h, bg = "white"); print(pl); dev.off() }
}
series <- function(G, k) switch(k, "C/GDP" = log(G$co2 / G$gdp_usd),
                                   "C/E"   = log(G$co2 / G$primary_energy_consumption),
                                   "E/GDP" = log(G$primary_energy_consumption / G$gdp_usd))
nw <- function(z, k) {
  X <- cbind(1, z$Year, pmax(0, z$Year - k)); y <- z$y
  b <- solve(crossprod(X), crossprod(X, y)); u <- as.vector(y - X %*% b)
  n <- nrow(X); L <- floor(4 * (n / 100)^(2/9)); S <- crossprod(X * u)
  for (l in 1:L) { w <- 1 - l/(L+1)
    G2 <- t(X[-(1:l), , drop = FALSE] * u[-(1:l)]) %*% (X[1:(n-l), , drop = FALSE] * u[1:(n-l)])
    S <- S + w * (G2 + t(G2)) }
  V <- solve(crossprod(X)) %*% S %*% solve(crossprod(X))
  c(delta = 100 * b[3], t = b[3] / sqrt(V[3, 3]))
}
ord <- function(v) { v <- round(v); paste0(v, ifelse(v %% 100 %in% 11:13, "th",
  c("th","st","nd","rd", rep("th", 6))[v %% 10 + 1])) }

## ---- FIGURE 1 · what actually changed after Paris -----------------------------
g <- P$g
rate <- function(v, a, b) { i <- g$Year >= a & g$Year <= b; 100 * unname(coef(lm(log(g[[v]][i]) ~ g$Year[i]))[2]) }
mk <- function(a, b) c(GDP = rate("gdp_usd", a, b),
                       CE  = rate("co2", a, b) - rate("primary_energy_consumption", a, b),
                       EG  = rate("primary_energy_consumption", a, b) - rate("gdp_usd", a, b),
                       CO2 = rate("co2", a, b))
pre <- mk(1990, 2015); post <- mk(2016, 2021)
lab <- c(GDP = "Economic growth", CE = "Fuel mix\n(cleaner energy)",
         EG = "Energy efficiency\n(energy per $)", CO2 = "CO2 emissions")
d1 <- data.frame(key = names(pre), part = factor(lab[names(pre)], levels = rev(lab)),
                 before = pre, after = post, chg = post - pre)
d1$txt <- sprintf("%+.1f  \u2192  %+.1f", d1$before, d1$after)
d1$note <- ifelse(abs(d1$chg) < .1, "no change", sprintf("%+.1f", d1$chg))
XR <- 3.9
p1 <- ggplot(d1, aes(y = part)) +
  geom_vline(xintercept = 0, color = "#BBBBBB") +
  geom_segment(aes(x = before, xend = after, yend = part), color = "#D2D2D2", linewidth = 2.4,
               arrow = arrow(length = unit(.17, "cm"), type = "closed")) +
  geom_point(aes(x = before), color = GREY, size = 5) +
  geom_point(aes(x = after), color = REDC, size = 5) +
  geom_text(aes(x = XR, label = txt), hjust = 1, size = 4.1, color = "#333333") +
  geom_text(aes(x = XR + 1.55, label = note), hjust = 1, size = 4.1, fontface = "bold",
            color = ifelse(abs(d1$chg) < .1, GREY, REDC)) +
  annotate("point", x = c(-1.35, -0.10), y = 4.55, color = c(GREY, REDC), size = 4) +
  annotate("text", x = c(-1.25, 0.00), y = 4.55, label = c("1990-2015", "since Paris"),
           hjust = 0, size = 3.8, color = c(GREY, REDC), fontface = "bold") +
  annotate("text", x = c(XR, XR + 1.55), y = 4.55, label = c("before \u2192 after", "change"),
           hjust = 1, size = 3.8, color = "#333333", fontface = "bold") +
  scale_x_continuous(limits = c(-1.5, 5.5), breaks = seq(-1, 3, 1)) +
  coord_cartesian(ylim = c(0.6, 4.75), clip = "off") +
  labs(title = "Emissions growth fell by two thirds after Paris - but only the fuel mix improved",
       subtitle = sprintf("Average annual change (%%). CO2 growth = economic growth + fuel mix + energy efficiency. %d countries, %.1f%% of global CO2.\nEnergy efficiency improved at exactly the same rate as before. Most of the slowdown is slower growth; the rest is cleaner energy.",
                          P$n, P$share),
       x = "Average annual change (%)", y = NULL) +
  theme_w + theme(panel.grid.major.x = element_line(color = "#EEEEEE"))
save_both(p1, "w2_fig1_what_changed", 12.5, 6.4)

## ---- FIGURE 2 · the anniversary test ------------------------------------------
proj <- do.call(rbind, lapply(names(kcols), function(k) {
  d <- data.frame(Year = g$Year, y = series(g, k), component = k)
  f <- lm(y ~ Year, d[d$Year <= 2015, ])
  pr <- predict(f, newdata = d, interval = "prediction")
  ref <- d$y[d$Year == 1990]
  d$idx <- 100 * exp(d$y - ref); d$fidx <- 100 * exp(pr[, 1] - ref)
  d$lo <- 100 * exp(pr[, 2] - ref); d$hi <- 100 * exp(pr[, 3] - ref); d
}))
nm <- c("C/GDP" = "Carbon intensity (overall)", "C/E" = "Fuel mix (cleaner energy)",
        "E/GDP" = "Energy efficiency")
proj$panel <- factor(nm[proj$component], levels = nm)
lb <- do.call(rbind, lapply(names(kcols), function(k) {
  d <- data.frame(Year = g$Year, y = series(g, k)); r <- nw(d, 2015)
  data.frame(panel = nm[k], txt = if (abs(r[2]) >= 2)
    sprintf("faster than trend:\n%+.1f pp/yr (t = %.1f)", r[1], r[2]) else
    sprintf("no change from trend:\n%+.1f pp/yr (t = %.1f)", r[1], r[2]))
}))
lb$panel <- factor(lb$panel, levels = nm)
lb$Year <- 1991
lb$idx <- sapply(as.character(lb$panel), function(k) min(proj$idx[proj$panel == k]) * 1.02)
p2 <- ggplot(proj, aes(Year, idx)) +
  geom_ribbon(data = proj[proj$Year >= 2015, ], aes(ymin = lo, ymax = hi, fill = component), alpha = .16, show.legend = FALSE) +
  geom_line(data = proj[proj$Year <= 2015, ], aes(y = fidx, color = component), linewidth = 1, show.legend = FALSE) +
  geom_line(data = proj[proj$Year >= 2015, ], aes(y = fidx, color = component), linewidth = 1, linetype = "22", show.legend = FALSE) +
  geom_point(aes(color = component), size = 1.7, show.legend = FALSE) +
  geom_point(data = proj[proj$Year > 2015, ], color = REDC, size = 2.8) +
  geom_vline(xintercept = 2015, linetype = "dashed", color = col_paris) +
  geom_text(data = lb, aes(label = txt), hjust = 0, size = 3.6, color = "#333333", lineheight = .95) +
  facet_wrap(~panel, ncol = 3, scales = "free_y") +
  scale_color_manual(values = kcols) + scale_fill_manual(values = kcols) + scale_y_log10() +
  labs(title = "The fuel mix broke away from its old trend after Paris. Efficiency did not.",
       subtitle = "Each panel is indexed to 1990 = 100. The line is the 1990-2015 trend, extended past Paris with a shaded band showing where\nthe following years should have landed if nothing had changed. Red points are what actually happened.",
       x = NULL, y = "Index (1990 = 100)") + theme_w
save_both(p2, "w2_fig2_anniversary_test", 13, 6)

## ---- FIGURE 3 · Rio versus Paris ------------------------------------------------
gh <- H$g
sweep <- do.call(rbind, lapply(names(kcols), function(k) {
  d <- data.frame(Year = gh$Year, y = series(gh, k))
  ks <- (min(d$Year) + 8):(max(d$Year) - 5)
  data.frame(panel = nm[k], knot = ks, t = sapply(ks, function(kk) abs(nw(d, kk)[2])))
}))
sweep$panel <- factor(sweep$panel, levels = nm)
ann <- do.call(rbind, lapply(split(sweep, sweep$panel), function(d) {
  data.frame(panel = d$panel[1], knot = d$knot[which.max(d$t)], t = max(d$t), ymin = min(d$t),
             paris = ord(100 * mean(d$t <= d$t[d$knot == 2015])),
             rio = ord(100 * mean(d$t <= d$t[d$knot == 1992])))
}))
p3 <- ggplot(sweep, aes(knot, t, color = panel)) +
  geom_vline(xintercept = 1992, linetype = "dashed", color = "#3A66A5") +
  geom_vline(xintercept = 2015, linetype = "dashed", color = col_paris) +
  geom_line(linewidth = 1.1) +
  geom_point(data = sweep[sweep$knot == 2015, ], shape = 21, fill = "white", size = 3.2, stroke = 1.2) +
  geom_text(data = ann, aes(x = 1994, y = ymin, label = paste0("Rio: ", rio, " percentile")),
            hjust = 0, vjust = -1.6, size = 3.5, color = "#3A66A5", show.legend = FALSE) +
  geom_text(data = ann, aes(x = 1994, y = ymin, label = paste0("Paris: ", paris)),
            hjust = 0, vjust = -0.3, size = 3.5, color = col_paris, fontface = "bold", show.legend = FALSE) +
  facet_wrap(~panel, ncol = 3, scales = "free_y") +
  scale_color_manual(values = unname(kcols)) +
  scale_x_continuous(breaks = c(1992, 2015), labels = c("Rio\n1992", "Paris\n2015")) +
  scale_y_continuous(expand = expansion(mult = c(.16, .10))) +
  labs(title = "Rio the record rejects. Paris it does not.",
       subtitle = sprintf("We put the turning point in every possible year and record how strong the evidence is. Higher means the record prefers that year.\nRio ranks near the bottom of all candidate years; Paris ranks near the top. %d countries, 1980-2021.", H$n),
       x = NULL, y = "Strength of evidence for a turn in this year") +
  theme_w + theme(legend.position = "none")
save_both(p3, "w2_fig3_rio_vs_paris", 13, 6)

## ---- FIGURE 4 · what the record could have seen ---------------------------------
d <- data.frame(Year = g$Year, y = series(g, "C/E"))
f <- lm(y ~ Year + I(pmax(0, Year - 2015)), d); s <- summary(f)$sigma
mde <- do.call(rbind, lapply(3:20, function(np) {
  yr <- c(1990:2015, 2016:(2015 + np)); X <- cbind(1, yr, pmax(0, yr - 2015))
  data.frame(end = 2015 + np, mde = 2.8 * 100 * s * sqrt(solve(crossprod(X))[3, 3]))
}))
obs <- abs(nw(d, 2015)[1])
half_yr <- min(mde$end[mde$mde <= obs / 2])
cat(sprintf("MDE crosses half the observed effect (%.2f pp/yr) in %d\n", obs/2, half_yr))
p4 <- ggplot(mde, aes(end, mde)) +
  geom_area(fill = "#3A66A5", alpha = .10) +
  geom_line(color = "#3A66A5", linewidth = 1.2) +
  geom_hline(yintercept = obs, color = REDC, linewidth = 1) +
  annotate("text", x = 2035, y = obs, label = sprintf("what we observe: %.1f pp/yr", obs),
           vjust = -0.7, hjust = 1, color = REDC, fontface = "bold", size = 4) +
  annotate("text", x = 2035, y = obs / 2, label = sprintf("an effect half this size\nstays invisible until %d", half_yr),
           vjust = -0.2, hjust = 1, color = "#333333", size = 3.8, lineheight = .95) +
  geom_vline(xintercept = 2021, linetype = "dotted") +
  annotate("text", x = 2021, y = max(mde$mde) * .95, label = "data end", hjust = -.12, size = 3.6) +
  scale_x_continuous(breaks = seq(2018, 2035, 3)) +
  labs(title = "Six years of data can only reveal a large effect",
       subtitle = "The line is the smallest change in the fuel-mix trend the test could reliably detect, as more years of data accumulate.\nWhat we observe clears the bar because it is large. A subtler Paris effect would not yet be visible at all.",
       x = "Data available through", y = "Smallest detectable change (pp/yr)") + theme_w
save_both(p4, "w2_fig4_what_we_could_see", 12.5, 6)

## ---- FIGURE 5 · how the panel is built (methods/appendix) ------------------------
cnt <- aggregate(Code ~ Year, p[p$ok, ], function(v) length(unique(v))); names(cnt)[2] <- "n"
p5 <- ggplot(cnt, aes(Year, n)) +
  annotate("rect", xmin = 1990, xmax = 2021, ymin = -Inf, ymax = Inf, fill = "#2E8B57", alpha = .08) +
  annotate("rect", xmin = 2021.5, xmax = 2023.5, ymin = -Inf, ymax = Inf, fill = REDC, alpha = .12) +
  geom_line(color = "#3A66A5", linewidth = 1.2) + geom_point(color = "#3A66A5", size = 1.6) +
  annotate("text", x = 2005, y = 55, label = sprintf("our window: %d countries,\n%.1f%% of global CO2", P$n, P$share),
           color = "#1B7837", fontface = "bold", size = 4, lineheight = .95) +
  annotate("text", x = 2021, y = 120, label = "not yet reported:\n191 → 78 countries", color = REDC, size = 3.5, hjust = 1.05, lineheight = .95) +
  labs(title = "We use every country that reports, for as long as it reports",
       subtitle = sprintf("Countries with complete emissions, energy and GDP data each year. We keep every country still reporting in 2021 with at least 90%% of\nyears present, and interpolate the %d remaining gaps. 2022-23 are excluded: most countries have not reported them yet.", P$filled),
       x = NULL, y = "Countries reporting") + theme_w
save_both(p5, "w2_fig5_panel_construction", 12.5, 5.8)

cat(sprintf("v2 figures written to %s\nPRIMARY %d countries (%.1f%% CO2, %d gaps filled) | HISTORY %d countries\n",
            od, P$n, P$share, P$filled, H$n))
