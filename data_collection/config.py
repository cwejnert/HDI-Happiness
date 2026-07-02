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
