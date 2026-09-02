# Master world-level analysis.
#
# Steps, in the order agreed:
#   (3) Data vintage  - current OWID CO2/energy + World Bank world GDP.
#   (2) Provenance    - a TRUE world aggregate replaces constructed country panels
#                       as the primary series; panels become robustness.
#   (1) Specification grid - every result re-run across series source, start year,
#                       endpoint, completeness threshold and interpolation.
#   (4) Unknown-break-date test - supWald with moving-block bootstrap critical
#                       values, plus BIC selection of the number of breaks.
#
# Outputs: outputs/final_master/world_master/{spec_grid.csv, supwald.csv, findings.txt}
options(stringsAsFactors = FALSE)
suppressPackageStartupMessages(library(ggplot2))

root <- normalizePath(file.path(getwd(), "outputs"), winslash = "/", mustWork = TRUE)
od <- file.path(root, "final_master", "world_master")
dir.create(od, recursive = TRUE, showWarnings = FALSE)
set.seed(20260902)

## ---------------------------------------------------------------- data --------
owid <- read.csv("data/owid_co2_current.csv")
wbg  <- read.csv("data/worldbank_world_gdp_const2015usd.csv")

W <- owid[owid$country == "World", c("year", "co2", "primary_energy_consumption")]
names(W) <- c("Year", "co2", "energy")
W <- W[is.finite(W$co2) & is.finite(W$energy) & W$co2 > 0 & W$energy > 0, ]
W <- merge(W, setNames(wbg, c("Year", "gdp")), by = "Year")
W <- W[order(W$Year), ]
WORLD <- W[W$Year >= 1965, ]

cty <- owid[nchar(owid$iso_code) == 3 & owid$country != "World",
            c("iso_code", "year", "co2", "primary_energy_consumption", "gdp")]
names(cty) <- c("Code", "Year", "co2", "energy", "gdp")
cty$ok <- is.finite(cty$co2) & cty$co2 > 0 & is.finite(cty$energy) & cty$energy > 0 &
          is.finite(cty$gdp) & cty$gdp > 0

build_panel <- function(y0, y1, minfrac, interpolate = TRUE) {
  yrs <- y0:y1
  d <- cty[cty$Year %in% yrs & cty$ok, ]
  have <- tapply(d$Year, d$Code, function(v) length(unique(v)))
  ends <- tapply(d$Year, d$Code, max)
  keep <- names(have)[have >= minfrac * length(yrs) & ends >= y1]
  if (!length(keep)) return(NULL)
  if (!interpolate) {
    keep <- names(have)[have == length(yrs) & ends >= y1]
    if (!length(keep)) return(NULL)
    m <- d[d$Code %in% keep, ]
  } else {
    full <- expand.grid(Code = keep, Year = yrs, stringsAsFactors = FALSE)
    m <- merge(full, d[, c("Code", "Year", "co2", "energy", "gdp")], all.x = TRUE)
    m <- m[order(m$Code, m$Year), ]
    for (v in c("co2", "energy", "gdp"))
      m[[v]] <- ave(m[[v]], m$Code, FUN = function(x)
        if (all(is.na(x))) x else exp(approx(seq_along(x), log(x), seq_along(x), rule = 2)$y))
  }
  g <- aggregate(cbind(co2, energy, gdp) ~ Year, m, sum)
  attr(g, "n") <- length(keep)
  g
}

kseries <- function(G, k) switch(k,
  "C/GDP" = log(G$co2 / G$gdp),
  "C/E"   = log(G$co2 / G$energy),
  "E/GDP" = log(G$energy / G$gdp))

## ------------------------------------------------------- inference helpers ----
hac_hinge <- function(z, k) {
  # slope-change coefficient at a FIXED knot k, Newey-West standard error
  X <- cbind(1, z$Year, pmax(0, z$Year - k)); y <- z$y
  b <- solve(crossprod(X), crossprod(X, y)); u <- as.vector(y - X %*% b)
  n <- nrow(X); L <- floor(4 * (n / 100)^(2/9)); S <- crossprod(X * u)
  for (l in 1:L) { w <- 1 - l/(L+1)
    G <- t(X[-(1:l), , drop = FALSE] * u[-(1:l)]) %*% (X[1:(n-l), , drop = FALSE] * u[1:(n-l)])
    S <- S + w * (G + t(G)) }
  V <- solve(crossprod(X)) %*% S %*% solve(crossprod(X))
  c(delta = 100 * b[3], t = b[3] / sqrt(V[3, 3]))
}
cand_years <- function(z, trim = .15) {
  n <- nrow(z); lo <- z$Year[max(2, floor(trim * n))]; hi <- z$Year[min(n - 1, ceiling((1 - trim) * n))]
  lo:hi
}
supwald <- function(z, trim = .15) {
  ks <- cand_years(z, trim)
  w <- sapply(ks, function(k) hac_hinge(z, k)[2]^2)
  list(stat = max(w), k = ks[which.max(w)], ks = ks, w = w)
}
mb_bootstrap_supwald <- function(z, B = 499, block = 5, trim = .15) {
  # null: single linear trend. Moving-block resample of residuals preserves serial dependence.
  f0 <- lm(y ~ Year, z); u <- resid(f0); fit <- fitted(f0); n <- nrow(z)
  nb <- ceiling(n / block)
  stats <- replicate(B, {
    starts <- sample(seq_len(n - block + 1), nb, replace = TRUE)
    ub <- unlist(lapply(starts, function(s) u[s:(s + block - 1)]))[1:n]
    supwald(data.frame(Year = z$Year, y = fit + ub), trim)$stat
  })
  stats
}
bic_nbreaks <- function(z, maxb = 3, minseg = 8) {
  best <- list(); ks <- cand_years(z, .12)
  best[[1]] <- list(nb = 0, bic = BIC(lm(y ~ Year, z)), k = integer(0))
  fitb <- function(brk) {
    X <- data.frame(y = z$y, Year = z$Year)
    for (i in seq_along(brk)) X[[paste0("s", i)]] <- pmax(0, z$Year - brk[i])
    lm(y ~ ., data = X)
  }
  for (nb in 1:maxb) {
    combos <- if (nb == 1) as.list(ks) else
      apply(utils::combn(ks, nb), 2, function(v) if (all(diff(v) >= minseg)) v else NULL)
    combos <- Filter(Negate(is.null), combos)
    if (!length(combos)) next
    b <- sapply(combos, function(v) BIC(fitb(v)))
    i <- which.min(b)
    best[[nb + 1]] <- list(nb = nb, bic = b[i], k = combos[[i]])
  }
  best <- Filter(Negate(is.null), best)
  bics <- sapply(best, `[[`, "bic")
  best[[which.min(bics)]]$all <- setNames(round(bics, 1), sapply(best, `[[`, "nb"))
  best[[which.min(bics)]]
}
ordn <- function(v) { v <- round(v); paste0(v, ifelse(v %% 100 %in% 11:13, "th",
  c("th","st","nd","rd", rep("th", 6))[v %% 10 + 1])) }

## ------------------------------------------------ (1) specification grid ------
specs <- list()
add <- function(...) specs[[length(specs) + 1]] <<- list(...)
for (y0 in c(1965, 1970, 1980, 1990)) for (y1 in c(2021, 2022, 2023))
  add(src = "World aggregate", y0 = y0, y1 = y1, minfrac = NA, interp = NA)
for (y0 in c(1980, 1990)) for (y1 in c(2020, 2021))
  for (mf in c(.80, .90, .95, 1.00)) for (ip in c(TRUE, FALSE))
    add(src = "Country panel", y0 = y0, y1 = y1, minfrac = mf, interp = ip)

rows <- list()
for (sp in specs) {
  if (sp$src == "World aggregate") {
    G <- WORLD[WORLD$Year >= sp$y0 & WORLD$Year <= sp$y1, ]; nlab <- NA
  } else {
    G <- build_panel(sp$y0, sp$y1, sp$minfrac, sp$interp)
    if (is.null(G) || nrow(G) < 25) next
    nlab <- attr(G, "n")
  }
  if (nrow(G) < 25) next
  for (k in c("C/GDP", "C/E", "E/GDP")) {
    y <- kseries(G, k)
    if (!all(is.finite(y))) next
    z <- data.frame(Year = G$Year, y = y)
    r <- hac_hinge(z, 2015)
    sw <- supwald(z)
    ks <- sw$ks; wv <- sw$w
    prc <- function(yr) if (yr %in% ks) 100 * mean(wv <= wv[ks == yr]) else NA_real_
    rows[[length(rows) + 1]] <- data.frame(
      source = sp$src, start = sp$y0, end = sp$y1,
      minfrac = sp$minfrac, interpolated = sp$interp, n_countries = nlab,
      component = k, n_obs = nrow(z),
      delta_pp = round(r[1], 3), t = round(r[2], 2),
      significant = abs(r[2]) >= 1.96,
      best_year = sw$k, paris_pctile = round(prc(2015), 1), rio_pctile = round(prc(1992), 1))
  }
}
grid <- do.call(rbind, rows)
write.csv(grid, file.path(od, "spec_grid.csv"), row.names = FALSE)

## ------------------------------------- (4) unknown-break-date test, primary ----
PRIMARY <- WORLD[WORLD$Year >= 1965 & WORLD$Year <= 2023, ]
sup_rows <- list()
for (k in c("C/GDP", "C/E", "E/GDP")) {
  z <- data.frame(Year = PRIMARY$Year, y = kseries(PRIMARY, k))
  z <- z[is.finite(z$y), ]
  sw <- supwald(z)
  bs <- mb_bootstrap_supwald(z, B = 499, block = 5)
  bb <- bic_nbreaks(z)
  sup_rows[[k]] <- data.frame(
    component = k, n_obs = nrow(z),
    supWald = round(sw$stat, 2), break_year = sw$k,
    crit95_bootstrap = round(quantile(bs, .95), 2),
    p_bootstrap = round(mean(bs >= sw$stat), 4),
    bic_n_breaks = bb$nb, bic_break_years = paste(bb$k, collapse = ", "))
  cat(sprintf("%-6s supWald=%.1f at %d | boot 95%% crit %.1f | p=%.3f | BIC breaks: %s\n",
      k, sw$stat, sw$k, quantile(bs, .95), mean(bs >= sw$stat), paste(bb$k, collapse = ", ")))
}
supdf <- do.call(rbind, sup_rows)
write.csv(supdf, file.path(od, "supwald.csv"), row.names = FALSE)

## ------------------------------------------------------------- invariance -----
inv <- do.call(rbind, lapply(split(grid, grid$component), function(d) data.frame(
  component = d$component[1], n_specs = nrow(d),
  pct_significant = round(100 * mean(d$significant), 0),
  delta_median = round(median(d$delta_pp), 2),
  delta_min = round(min(d$delta_pp), 2), delta_max = round(max(d$delta_pp), 2),
  best_year_median = median(d$best_year),
  best_year_range = paste(range(d$best_year), collapse = "-"),
  pct_best_before_2015 = round(100 * mean(d$best_year < 2015), 0),
  paris_pctile_median = round(median(d$paris_pctile, na.rm = TRUE), 0),
  rio_pctile_median = round(median(d$rio_pctile, na.rm = TRUE), 0))))
write.csv(inv, file.path(od, "invariance_summary.csv"), row.names = FALSE)

## ---------------------------------------------------------- provenance --------
prov <- do.call(rbind, lapply(c("C/GDP", "C/E", "E/GDP"), function(k) {
  a <- WORLD[WORLD$Year >= 1965, ]; za <- data.frame(Year = a$Year, y = kseries(a, k))
  za <- za[is.finite(za$y), ]
  b <- build_panel(1980, 2021, .90, TRUE); zb <- data.frame(Year = b$Year, y = kseries(b, k))
  data.frame(component = k,
             world_break = supwald(za)$k, world_n = nrow(za),
             panel1980_break = supwald(zb)$k, panel_n = nrow(zb))
}))
write.csv(prov, file.path(od, "provenance_comparison.csv"), row.names = FALSE)

## ------------------------------------------------------------- findings -------
sink(file.path(od, "findings.txt"))
cat("WORLD-LEVEL MASTER ANALYSIS\n===========================\n\n")
cat("PRIMARY SERIES: true world aggregate\n")
cat(sprintf("  CO2 and energy: OWID 'World' row, %d-%d (contiguous)\n", min(WORLD$Year), max(WORLD$Year)))
cat("  GDP: World Bank world total, constant 2015 USD\n")
cat(sprintf("  No panel construction, no interpolation, no composition drift. %d post-Paris years.\n\n",
            sum(WORLD$Year > 2015)))
cat("(4) UNKNOWN-BREAK-DATE TEST (supWald, moving-block bootstrap critical values)\n")
print(supdf, row.names = FALSE)
cat("\n(1) SPECIFICATION GRID:", nrow(grid), "estimates across", length(unique(paste(grid$source, grid$start, grid$end, grid$minfrac, grid$interpolated))), "specifications\n")
print(inv, row.names = FALSE)
cat("\n(2) PROVENANCE: break year, true world aggregate vs constructed panel\n")
print(prov, row.names = FALSE)
cat("\nPost-2015 hinge estimates on the primary series:\n")
for (k in c("C/GDP", "C/E", "E/GDP")) {
  z <- data.frame(Year = PRIMARY$Year, y = kseries(PRIMARY, k)); z <- z[is.finite(z$y), ]
  r <- hac_hinge(z, 2015); sw <- supwald(z); ks <- sw$ks; wv <- sw$w
  cat(sprintf("  %-6s %+0.2f pp/yr (t = %.2f) | best year %d | Paris %s pctile | Rio %s\n",
    k, r[1], r[2], sw$k,
    ordn(100 * mean(wv <= wv[ks == 2015])),
    if (1992 %in% ks) ordn(100 * mean(wv <= wv[ks == 1992])) else "n/a"))
}
sink()
cat(readLines(file.path(od, "findings.txt")), sep = "\n")
