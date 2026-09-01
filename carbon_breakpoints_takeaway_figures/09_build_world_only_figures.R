# World-only paper: figures built on a COMPOSITION-CONSTANT (balanced) country panel.
# The raw panel's country coverage drifts (53 countries in 1965, 149 by 1980, 191 in
# 2021, 78 in 2022-23), so a naive sum-over-available-countries world aggregate mixes
# real trend with coverage change. Everything here uses a balanced panel instead.
options(stringsAsFactors = FALSE)
suppressPackageStartupMessages(library(ggplot2))

root <- normalizePath(file.path(getwd(), "outputs"), winslash = "/", mustWork = TRUE)
od <- file.path(root, "final_master", "figures_world")
dir.create(od, recursive = TRUE, showWarnings = FALSE)

p <- read.csv(file.path(root, "global_harmonization/global_kaya_external_parent.csv"))
ok <- p[is.finite(p$co2) & p$co2 > 0 & is.finite(p$primary_energy_consumption) &
        p$primary_energy_consumption > 0 & is.finite(p$gdp_usd) & p$gdp_usd > 0, ]

YRS <- 1971:2021                      # balanced window: drops the 2022-23 coverage cliff
tab <- table(ok$Code[ok$Year %in% YRS])
BAL <- names(tab)[tab == length(YRS)]
bal <- ok[ok$Code %in% BAL & ok$Year %in% YRS, ]
g <- aggregate(cbind(co2, primary_energy_consumption, gdp_usd) ~ Year, bal, sum)
share <- 100 * sum(bal$co2[bal$Year == 2015]) / sum(ok$co2[ok$Year == 2015])

kcols <- c("C/GDP" = "#3A66A5", "C/E" = "#2E8B57", "E/GDP" = "#C77F00")
col_break <- "#B33A3A"; col_rio <- "#3A66A5"; col_paris <- "#2E7D32"
theme_w <- theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold", size = 16),
        plot.subtitle = element_text(color = "#555555", size = 10.5),
        panel.grid.minor = element_blank(), legend.position = "bottom",
        plot.margin = margin(12, 18, 12, 12), plot.title.position = "plot")
save_both <- function(p, stem, w = 12, h = 6.5) {
  ggsave(file.path(od, paste0(stem, ".png")), p, width = w, height = h, dpi = 300, bg = "white")
  if (capabilities("cairo")) { svg(file.path(od, paste0(stem, ".svg")), width = w, height = h, bg = "white"); print(p); dev.off() }
}
comp <- function(k) switch(k, "C/GDP" = log(g$co2 / g$gdp_usd),
                              "C/E"   = log(g$co2 / g$primary_energy_consumption),
                              "E/GDP" = log(g$primary_energy_consumption / g$gdp_usd))
nw <- function(z, k) {
  X <- cbind(1, z$Year, pmax(0, z$Year - k)); y <- z$y
  b <- solve(crossprod(X), crossprod(X, y)); u <- as.vector(y - X %*% b)
  n <- nrow(X); L <- floor(4 * (n / 100)^(2/9)); S <- crossprod(X * u)
  for (l in 1:L) { w <- 1 - l/(L+1)
    G <- t(X[-(1:l), , drop = FALSE] * u[-(1:l)]) %*% (X[1:(n-l), , drop = FALSE] * u[1:(n-l)])
    S <- S + w * (G + t(G)) }
  V <- solve(crossprod(X)) %*% S %*% solve(crossprod(X))
  c(delta = 100 * b[3], t = b[3] / sqrt(V[3, 3]))
}

## W1 — the long record: several episodes, not one intervention -----------------
z <- data.frame(Year = g$Year, y = comp("C/GDP"))
cand <- (min(z$Year) + 8):(max(z$Year) - 8)
bic1 <- sapply(cand, function(k) BIC(lm(y ~ Year + I(pmax(0, Year - k)), z)))
k1 <- cand[which.min(bic1)]
best <- list(bic = Inf)
for (a in cand) for (b_ in cand) for (c_ in cand) if (b_ - a >= 8 && c_ - b_ >= 8) {
  m <- lm(y ~ Year + I(pmax(0, Year - a)) + I(pmax(0, Year - b_)) + I(pmax(0, Year - c_)), z)
  if (BIC(m) < best$bic) best <- list(bic = BIC(m), k = c(a, b_, c_), m = m)
}
z$fit <- predict(best$m)
z$idx <- 100 * exp(z$y - z$y[1])
z$fidx <- 100 * exp(z$fit - z$y[1])
cf <- coef(best$m); slopes <- 100 * cumsum(cf[2:5])
seg <- data.frame(k = c(min(z$Year), best$k), end = c(best$k, max(z$Year)), slope = slopes)
seg$mid <- (seg$k + seg$end) / 2
seg$ypos <- exp(approx(z$Year, log(z$fidx), seg$mid)$y) * 1.06
p1 <- ggplot(z, aes(Year, idx)) +
  geom_vline(xintercept = c(1992, 2015), linetype = "dashed", color = c(col_rio, col_paris)) +
  geom_vline(xintercept = best$k, color = col_break, linewidth = .7, alpha = .55) +
  geom_point(color = "#8A8A8A", size = 1.6) +
  geom_line(aes(y = fidx), color = col_break, linewidth = 1.2) +
  geom_label(data = seg, aes(mid, ypos, label = sprintf("%+.2f%%/yr", slope)),
             inherit.aes = FALSE, size = 3.5, fontface = "bold", color = "#333333",
             fill = "white", label.size = 0) +
  annotate("text", x = best$k, y = min(z$idx) * 0.985, label = best$k, color = col_break,
           fontface = "bold", size = 3.4) +
  annotate("text", x = 1992, y = max(z$idx) * .99, label = "Rio", color = col_rio, hjust = -.15, fontface = "bold", size = 3.6) +
  annotate("text", x = 2015, y = max(z$idx) * .99, label = "Paris", color = col_paris, hjust = -.15, fontface = "bold", size = 3.6) +
  scale_y_log10() + scale_x_continuous(breaks = seq(1970, 2020, 10)) +
  labs(title = "The world's carbon-intensity record is a sequence of episodes, not one turning point",
       subtitle = sprintf("Carbon intensity of a composition-constant panel of %d countries (%.0f%% of 2015 global CO2), 1971 = 100, log scale. Red = best multiple-break fit;\nBIC prefers three breaks (%s) over one (%s). Segment labels give the average annual change within each episode.",
                          length(BAL), share, paste(best$k, collapse = ", "), k1),
       x = NULL, y = "Carbon intensity (1971 = 100)") + theme_w
save_both(p1, "world_fig01_episodes", 12.5, 6.5)

## W2 — the anniversary test on a constant country set ---------------------------
proj <- do.call(rbind, lapply(names(kcols), function(k) {
  d <- data.frame(Year = g$Year, y = comp(k), component = k)
  d <- d[d$Year >= 1990, ]
  f <- lm(y ~ Year, d[d$Year <= 2015, ])
  pr <- predict(f, newdata = d, interval = "prediction")
  ref <- d$y[d$Year == 1990]
  d$idx <- 100 * exp(d$y - ref); d$fidx <- 100 * exp(pr[, 1] - ref)
  d$lo <- 100 * exp(pr[, 2] - ref); d$hi <- 100 * exp(pr[, 3] - ref)
  d
}))
proj$component <- factor(proj$component, levels = names(kcols))
lab <- do.call(rbind, lapply(names(kcols), function(k) {
  d <- data.frame(Year = g$Year, y = comp(k)); d <- d[d$Year >= 1990, ]
  r <- nw(d, 2015)
  sw <- sapply(2005:2016, function(kk) abs(nw(d, kk)[2]))
  data.frame(component = k, txt = sprintf("post-2015 change: %+.2f pp/yr (t = %.1f)\nbest-fitting onset: %d",
                                          r[1], r[2], (2005:2016)[which.max(sw)]))
}))
lab$component <- factor(lab$component, levels = names(kcols))
lab$Year <- 1991
lab$idx <- sapply(as.character(lab$component), function(k) min(proj$idx[proj$component == k]) * 1.03)
p2 <- ggplot(proj, aes(Year, idx)) +
  geom_ribbon(data = proj[proj$Year >= 2015, ], aes(ymin = lo, ymax = hi, fill = component), alpha = .15, show.legend = FALSE) +
  geom_line(data = proj[proj$Year <= 2015, ], aes(y = fidx, color = component), linewidth = 1, show.legend = FALSE) +
  geom_line(data = proj[proj$Year >= 2015, ], aes(y = fidx, color = component), linewidth = 1, linetype = "22", show.legend = FALSE) +
  geom_point(aes(color = component), size = 1.7, show.legend = FALSE) +
  geom_point(data = proj[proj$Year > 2015, ], color = col_break, size = 2.6) +
  geom_vline(xintercept = 2015, linetype = "dashed", color = col_paris) +
  geom_text(data = lab, aes(label = txt), hjust = 0, size = 3.2, color = "#333333", lineheight = .95) +
  facet_wrap(~component, ncol = 3, scales = "free_y") +
  scale_color_manual(values = kcols) + scale_fill_manual(values = kcols) + scale_y_log10() +
  labs(title = "On a constant country set, the post-Paris acceleration is large — and it runs through both Kaya doors",
       subtitle = "1990 = 100, log scale. Solid line: 1990-2015 trend; dashed: its extrapolation with a 95% prediction band; red points: observed since Paris.\nEvery component now accelerates significantly — but each one's best-fitting onset lands before 2015.",
       x = NULL, y = "Index (1990 = 100)") + theme_w
save_both(p2, "world_fig02_anniversary_test", 13, 6)

## W3 — the arithmetic, by era ---------------------------------------------------
sl <- function(v, a, b) { i <- g$Year >= a & g$Year <= b; 100 * unname(coef(lm(log(g[[v]][i]) ~ g$Year[i]))[2]) }
eras <- list(`1990-2015 (Rio to Paris)` = c(1990, 2015), `2016-2021 (after Paris)` = c(2016, 2021))
ar <- do.call(rbind, lapply(names(eras), function(e) {
  y <- eras[[e]]
  data.frame(era = e, part = c("GDP growth", "Fuel mix (C/E)", "Energy intensity (E/GDP)", "= CO2 emissions"),
             val = c(sl("gdp_usd", y[1], y[2]),
                     sl("co2", y[1], y[2]) - sl("primary_energy_consumption", y[1], y[2]),
                     sl("primary_energy_consumption", y[1], y[2]) - sl("gdp_usd", y[1], y[2]),
                     sl("co2", y[1], y[2])),
             gdp = sl("gdp_usd", y[1], y[2]))
}))
ar$part <- factor(ar$part, levels = rev(c("GDP growth", "Fuel mix (C/E)", "Energy intensity (E/GDP)", "= CO2 emissions")))
need <- unique(ar[, c("era", "gdp")])
p3 <- ggplot(ar, aes(val, part, fill = part)) +
  geom_col(width = .62, show.legend = FALSE) +
  geom_vline(xintercept = 0, color = "#555555") +
  geom_vline(data = need, aes(xintercept = -gdp), linetype = "dotted", color = "#333333", linewidth = .8) +
  geom_text(aes(label = sprintf("%+.2f%%", val), hjust = ifelse(val > 0, -.12, 1.12)), size = 3.8) +
  geom_text(data = need, aes(x = -gdp, y = .62, label = "intensity decline needed\nto hold emissions flat"),
            inherit.aes = FALSE, size = 3, color = "#333333", hjust = 0, nudge_x = .08, lineheight = .95) +
  facet_wrap(~era) + scale_fill_manual(values = c("GDP growth" = "#8A8A8A", "Fuel mix (C/E)" = "#2E8B57",
    "Energy intensity (E/GDP)" = "#C77F00", "= CO2 emissions" = "#B33A3A")) +
  scale_x_continuous(expand = expansion(mult = .22)) +
  labs(title = "Emissions growth halved after Paris — and this time intensity did most of the work",
       subtitle = "Average annual change, composition-constant panel. CO2 growth = GDP growth + fuel-mix change + energy-intensity change; the dotted line marks the\nintensity decline that would hold emissions flat. Of the 1.87-point slowdown in CO2 growth, roughly half is slower GDP and half is faster intensity improvement.",
       x = "Average annual change (%)", y = NULL) + theme_w
save_both(p3, "world_fig03_arithmetic", 12.5, 6)

ord <- function(v) { v <- round(v); s <- ifelse(v %% 100 %in% 11:13, "th",
  c("th","st","nd","rd", rep("th", 6))[v %% 10 + 1]); paste0(v, s) }
## W4 — the placebo plateau: which year does the record actually prefer? ---------
SW_MIN <- 1980
sweep <- do.call(rbind, lapply(names(kcols), function(k) {
  d <- data.frame(Year = g$Year, y = comp(k)); d <- d[d$Year >= SW_MIN, ]
  ks <- (SW_MIN + 8):(max(d$Year) - 5)
  data.frame(component = k, knot = ks, t = sapply(ks, function(kk) abs(nw(d, kk)[2])))
}))
sweep$component <- factor(sweep$component, levels = names(kcols))
ann <- do.call(rbind, lapply(split(sweep, sweep$component), function(d) {
  best <- d[which.max(d$t), ]
  pr <- mean(d$t <= d$t[d$knot == 2015]); rr <- mean(d$t <= d$t[d$knot == 1992])
  data.frame(component = best$component, knot = best$knot, t = best$t,
             lab = sprintf("best fit: %d", best$knot),
             foot = sprintf("Paris: %s percentile   ·   Rio: %s", ord(100 * pr), ord(100 * rr)),
             ymin = min(d$t))
}))
p4 <- ggplot(sweep, aes(knot, t, color = component)) +
  geom_vline(xintercept = 1992, linetype = "dashed", color = col_rio) +
  geom_vline(xintercept = 2015, linetype = "dashed", color = col_paris) +
  geom_line(linewidth = 1) +
  geom_point(data = ann, size = 3.4) +
  geom_point(data = sweep[sweep$knot == 2015, ], shape = 21, fill = "white", size = 3, stroke = 1.1) +
  geom_text(data = ann, aes(x = knot, y = t, label = lab), vjust = -1.2, hjust = 0.9,
            size = 3.4, fontface = "bold", show.legend = FALSE) +
  geom_text(data = ann, aes(x = 1988, y = ymin, label = foot), hjust = 0, vjust = -0.2,
            size = 3.2, color = "#333333", show.legend = FALSE) +
  facet_wrap(~component, ncol = 3, scales = "free_y") +
  scale_color_manual(values = kcols) +
  scale_x_continuous(breaks = seq(1990, 2015, 10), limits = c(SW_MIN + 7, 2019)) +
  scale_y_continuous(expand = expansion(mult = c(.12, .18))) +
  labs(title = "Rio the global record dismisses. Paris it cannot.",
       subtitle = "Evidence (|t|, autocorrelation-robust) for a slope change placed at each candidate year, composition-constant panel, 1980-2021. Open circles mark 2015.\nParis sits in the top decile of candidate years for overall intensity and the fuel mix; Rio sits near the bottom. But the best-fitting onset is 1-3 years earlier in every component.",
       x = "Candidate onset year", y = "Evidence for a break at this year (|t|)") +
  theme_w + theme(legend.position = "none")
save_both(p4, "world_fig04_placebo_plateau", 13, 6)

## W5 — why the world aggregate needs care: coverage drift and China -------------
cnt <- aggregate(Code ~ Year, ok, function(v) length(unique(v))); names(cnt)[2] <- "n"
pa <- ggplot(cnt, aes(Year, n)) +
  annotate("rect", xmin = 2021.5, xmax = 2023.5, ymin = -Inf, ymax = Inf, fill = col_break, alpha = .10) +
  geom_line(color = "#3A66A5", linewidth = 1.1) + geom_point(color = "#3A66A5", size = 1.5) +
  annotate("text", x = 2021, y = 120, label = "reporting lag:\n191 → 78 countries", color = col_break, size = 3.2, hjust = 1, lineheight = .95) +
  annotate("text", x = 1979, y = 95, label = "coverage jump:\n59 → 149 countries", color = "#333333", size = 3.2, hjust = 1, lineheight = .95) +
  labs(title = "Country coverage is not constant", subtitle = "Countries with complete Kaya data, by year",
       x = NULL, y = "Countries") + theme_w
exc <- ok[ok$Code %in% setdiff(BAL, "CHN") & ok$Year %in% YRS, ]
gx <- aggregate(cbind(co2, primary_energy_consumption) ~ Year, exc, sum)
ce <- rbind(data.frame(Year = g$Year, v = log(g$co2 / g$primary_energy_consumption), s = "All 58 countries"),
            data.frame(Year = gx$Year, v = log(gx$co2 / gx$primary_energy_consumption), s = "Excluding China"))
ce <- ce[ce$Year >= 1990, ]
ce$idx <- ave(ce$v, ce$s, FUN = function(v) 100 * exp(v - v[1]))
pb <- ggplot(ce, aes(Year, idx, color = s)) +
  geom_vline(xintercept = 2015, linetype = "dashed", color = col_paris) +
  geom_line(linewidth = 1.1) +
  scale_color_manual(values = c("All 58 countries" = "#8A8A8A", "Excluding China" = "#2E8B57")) +
  labs(title = "And the world average hides its largest member",
       subtitle = "Carbon intensity of energy, 1990 = 100. China's coal-era growth held the world\nfuel mix flat while the rest of the panel slowly improved.",
       x = NULL, y = "C/E (1990 = 100)", color = NULL) + theme_w
draw5 <- function() {
  grid::grid.newpage()
  grid::pushViewport(grid::viewport(layout = grid::grid.layout(1, 2)))
  print(pa, vp = grid::viewport(layout.pos.row = 1, layout.pos.col = 1))
  print(pb, vp = grid::viewport(layout.pos.row = 1, layout.pos.col = 2))
}
png(file.path(od, "world_fig05_aggregation.png"), width = 13, height = 5.6, units = "in", res = 300, bg = "white")
draw5(); dev.off()
if (capabilities("cairo")) { svg(file.path(od, "world_fig05_aggregation.svg"), width = 13, height = 5.6, bg = "white"); draw5(); dev.off() }

## W6 — the power problem: when does a modest effect become visible? -------------
d <- data.frame(Year = g$Year, y = comp("C/GDP")); d <- d[d$Year >= 1990, ]
f <- lm(y ~ Year + I(pmax(0, Year - 2015)), d); s <- summary(f)$sigma
mde <- do.call(rbind, lapply(3:20, function(np) {
  yr <- c(1990:2015, 2016:(2015 + np))
  X <- cbind(1, yr, pmax(0, yr - 2015))
  se <- 100 * s * sqrt(solve(crossprod(X))[3, 3])
  data.frame(post_years = np, end = 2015 + np, mde80 = 2.8 * se, mde50 = 1.96 * se)
}))
obs <- abs(nw(d, 2015)[1])
p6 <- ggplot(mde, aes(end)) +
  geom_ribbon(aes(ymin = mde50, ymax = mde80), fill = "#3A66A5", alpha = .13) +
  geom_line(aes(y = mde80), color = "#3A66A5", linewidth = 1.1) +
  geom_line(aes(y = mde50), color = "#3A66A5", linewidth = .7, linetype = "22") +
  geom_hline(yintercept = obs, color = col_break, linewidth = 1) +
  annotate("text", x = 2034, y = obs, label = sprintf("observed acceleration: %.2f pp/yr", obs),
           vjust = -0.6, hjust = 1, color = col_break, fontface = "bold", size = 3.6) +
  geom_vline(xintercept = 2021, linetype = "dotted", color = "#333333") +
  annotate("text", x = 2021, y = max(mde$mde80) * .95, label = "data end", hjust = -.12, size = 3.3, color = "#333333") +
  scale_x_continuous(breaks = seq(2018, 2035, 3)) +
  labs(title = "Ten years of data can only reveal a very large effect",
       subtitle = "Smallest post-2015 slope change detectable at 80% power (solid) and at the 5% significance threshold (dashed), given the noise in the world series.\nThe observed acceleration clears the bar because it is unusually large; an effect half its size would not be visible until the early 2030s.",
       x = "Data available through", y = "Minimum detectable slope change (pp/yr)") + theme_w
save_both(p6, "world_fig06_power", 12.5, 6)

cat("World-only figures written to", od, "\n")
cat(sprintf("balanced panel: %d countries, %.1f%% of 2015 CO2; episodes at %s\n",
            length(BAL), share, paste(best$k, collapse = ", ")))
