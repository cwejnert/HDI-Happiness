"""
Shared configuration for the HDI / SHDI / ESS wellbeing-expansion data pipeline.

Mirrors the variable groups and indicator definitions laid out in the concept
note ("Human Development and Subjective Well-Being in Europe Using ESS, HDI,
and SHDI") and reuses the HDI indicator codes from HappinessHDI.R so the two
projects stay consistent.
"""

YEAR_MIN = 2002   # ESS round 1
YEAR_MAX = 2024   # ESS round 11 / latest HDI vintage

# -----------------------------------------------------------------------
# ESS variables, grouped exactly as in the concept note. Use this list when
# building the extract in the ESS Data Builder (https://ess.sikt.no) so
# nothing gets missed. `essround` and `cntry` are always included by ESS.
# -----------------------------------------------------------------------
ESS_VARIABLES = {
    "identifiers": [
        "idno", "cntry", "essround", "region",  # 'region' = NUTS-coded regional identifier
    ],
    "outcomes": [
        "stflife",  # life satisfaction (evaluative)
        "happy",    # happiness (affective)
    ],
    "demographics": [
        "agea", "gndr", "domicil",
    ],
    "education_class": [
        "eisced", "eduyrs", "hinctnta", "hincfel",
        "uempla", "uempli", "pdwrk", "emplrel", "isco08",
    ],
    "family_household": [
        "rshpsts", "hhmmb",
    ],
    "social_trust": [
        "ppltrst", "pplfair", "pplhlp",
    ],
    "institutional_trust": [
        "trstprl", "trstlgl", "trstplc", "trstplt", "trstprt", "trstep", "trstun",
    ],
    "health": [
        "health", "hlthhmp",
    ],
    "social_integration": [
        "sclmeet", "inprdsc", "sclact",
    ],
    "safety": [
        "aesfdrk", "crmvct",
    ],
    "politics_efficacy": [
        "stfeco", "stfgov", "stfdem", "stfedu", "stfhlth", "psppsgva", "actrolga",
    ],
    "values": [
        "ipcrtiv", "imprich", "ipeqopt", "ipshabt", "impsafe",
        "impfree", "iphlppl", "ipstrgv", "imptrad", "impfun",
    ],
}

ESS_ALL_VARIABLES = [v for group in ESS_VARIABLES.values() for v in group]

# Highest legitimate substantive value per ESS variable, used to distinguish
# a real scale score from a repeated-digit missing sentinel (77/88/99 etc.)
# that happens to share the same digits -- e.g. stflife=8 is a real score on
# its 0-10 scale, but stflife=88 is "Don't know". A repeated-{6,7,8,9}-digit
# value only gets recoded to missing in io_utils.read_ess_extract if it
# exceeds this bound. Variables not listed here (e.g. isco08, whose 4-digit
# occupation codes can collide with the missing-sentinel pattern) are left
# untouched rather than risk corrupting real values with a guessed bound.
ESS_MAX_VALID = {
    "stflife": 10, "happy": 10,
    "agea": 100,
    "domicil": 5,
    "eisced": 7, "eduyrs": 50, "hinctnta": 10, "hincfel": 4,
    "uempla": 1, "uempli": 1, "pdwrk": 1, "emplrel": 3,
    "rshpsts": 6, "hhmmb": 20,
    "ppltrst": 10, "pplfair": 10, "pplhlp": 10,
    "trstprl": 10, "trstlgl": 10, "trstplc": 10, "trstplt": 10,
    "trstprt": 10, "trstep": 10, "trstun": 10,
    "health": 5, "hlthhmp": 3,
    "sclmeet": 7, "inprdsc": 6, "sclact": 5,
    "aesfdrk": 4, "crmvct": 2,
    "stfeco": 10, "stfgov": 10, "stfdem": 10, "stfedu": 10, "stfhlth": 10,
    "psppsgva": 5, "actrolga": 5,
    "ipcrtiv": 6, "imprich": 6, "ipeqopt": 6, "ipshabt": 6, "impsafe": 6,
    "impfree": 6, "iphlppl": 6, "ipstrgv": 6, "imptrad": 6, "impfun": 6,
    "gndr": 2,
}

# Variable-specific sentinel values that fall inside ESS_MAX_VALID's range and
# so survive the repeated-{6,7,8,9}-digit missing-code sweep, but still aren't
# real points on the variable's numeric scale. Confirmed against real ESS
# data (2026-07): eisced=55 is ESS's own "Other" category (level not
# classifiable on the standard 1-7 ISCED ladder) -- a legitimate response,
# but not an ordinal position, so it has to drop out of any numeric analysis
# the same way a missing value would.
ESS_EXTRA_MISSING_CODES = {
    "eisced": [55],
}

# ESS round -> fieldwork year used to match against HDI/SHDI year.
# Rounds span two calendar years in the field; the HDR/SHDI year is matched
# to the first fieldwork year of the round (adjust if a later round is added).
ESS_ROUND_YEAR = {
    1: 2002, 2: 2004, 3: 2006, 4: 2008, 5: 2010, 6: 2012, 7: 2014,
    8: 2016, 9: 2018, 10: 2020, 11: 2023,
}

# -----------------------------------------------------------------------
# ESS country name -> ISO3, matching the country set used across ESS rounds
# 1-11. Needed to query GDL (which keys on ISO3) and to reuse the national
# HDI crosswalk logic from HappinessHDI.R.
# -----------------------------------------------------------------------
ESS_ISO2_TO_ISO3 = {
    "AL": "ALB", "AT": "AUT", "BE": "BEL", "BG": "BGR", "HR": "HRV",
    "CY": "CYP", "CZ": "CZE", "DK": "DNK", "EE": "EST", "FI": "FIN",
    "FR": "FRA", "DE": "DEU", "GR": "GRC", "HU": "HUN", "IS": "ISL",
    "IE": "IRL", "IL": "ISR", "IT": "ITA", "XK": "XKX", "LV": "LVA",
    "LT": "LTU", "LU": "LUX", "ME": "MNE", "NL": "NLD", "MK": "MKD",
    "NO": "NOR", "PL": "POL", "PT": "PRT", "RO": "ROU", "RU": "RUS",
    "RS": "SRB", "SK": "SVK", "SI": "SVN", "ES": "ESP", "SE": "SWE",
    "CH": "CHE", "TR": "TUR", "UA": "UKR", "GB": "GBR",
}

ESS_COUNTRY_ISO3 = {
    "Albania": "ALB", "Austria": "AUT", "Belgium": "BEL", "Bulgaria": "BGR",
    "Croatia": "HRV", "Cyprus": "CYP", "Czechia": "CZE", "Czech Republic": "CZE",
    "Denmark": "DNK", "Estonia": "EST", "Finland": "FIN", "France": "FRA",
    "Germany": "DEU", "Greece": "GRC", "Hungary": "HUN", "Iceland": "ISL",
    "Ireland": "IRL", "Israel": "ISR", "Italy": "ITA", "Kosovo": "XKX",
    "Latvia": "LVA", "Lithuania": "LTU", "Luxembourg": "LUX",
    "Montenegro": "MNE", "Netherlands": "NLD", "North Macedonia": "MKD",
    "Norway": "NOR", "Poland": "POL", "Portugal": "PRT", "Romania": "ROU",
    "Russian Federation": "RUS", "Russia": "RUS", "Serbia": "SRB",
    "Slovakia": "SVK", "Slovenia": "SVN", "Spain": "ESP", "Sweden": "SWE",
    "Switzerland": "CHE", "Turkey": "TUR", "Turkiye": "TUR",
    "Ukraine": "UKR", "United Kingdom": "GBR",
}

# -----------------------------------------------------------------------
# HDI / SHDI indicator codes. National HDI codes (le, eys, mys, gnipc, hdi)
# come straight from HappinessHDI.R. SHDI uses different short codes for the
# same underlying dimensions, confirmed against globaldatalab.org/shdi's
# metadata page.
# -----------------------------------------------------------------------
HDI_COMPOSITE = "hdi"
HDI_SUBCOMPS = ["le", "eys", "mys", "gnipc"]

# Short labels for figures, matching HappinessHDI.R's ind_short.
ind_short = {
    "hdi": "HDI", "le": "Life Exp.", "eys": "Exp. Schooling",
    "mys": "Mean Schooling", "gnipc": "GNI p.c.",
}

SHDI_COMPOSITE = "shdi"
SHDI_DIMENSION_INDICES = ["healthindex", "edindex", "incindex"]
SHDI_RAW_COMPONENTS = ["lifexp", "esch", "msch", "gnic"]
SHDI_INDICATORS = [SHDI_COMPOSITE] + SHDI_DIMENSION_INDICES + SHDI_RAW_COMPONENTS

# National-HDI-code -> SHDI-code, for labeling comparable panels side by side.
HDI_TO_SHDI = {
    "hdi": "shdi",
    "le": "lifexp",
    "eys": "esch",
    "mys": "msch",
    "gnipc": "gnic",
}

# Confirmed against a real GDL export (2026-07): the 'Level' column is text,
# not the numeric level=1/4 used in GDL's old query-string API.
SHDI_LEVEL_NATIONAL = "National"
SHDI_LEVEL_SUBNATIONAL = "Subnat"
