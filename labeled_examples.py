"""
Your labeled examples for the relevance filter, organized per category.
Add more headlines here over time as you find things you did/didn't like —
the more examples, the smarter the filter gets. No need to touch any
other file when you do this.
"""

WORLD_LIKED = [
    "Powerful earthquake strikes Japan, tsunami warning issued",
    "Wildfires spread across southern France, thousands evacuated",
    "Trump announces new policy on trade tariffs",
    "Israel launches strikes amid escalating regional tensions",
    "Ukraine reports major battlefield developments as war continues",
]

WORLD_DISLIKED = [
    "Africa Moves Toward Cleaner Transport as GEF Approves $13.46 Million Green Mobility Initiative",
    "Kenya Accelerates Mission 300 Energy Plan to Expand Electricity Access by 2030",
    "Sudan: SAF Claims Gains On Omdurman-El Obeid Road As Fighting Continues in North Kordofan",
    "Prison worker stands trial accused of raping inmate at Adelaide prison",
    "Submit Applications for Distinguished Women Scientists Fund (Netherlands)",
    "West Africa: Ecowas Reaffirms 2027 Launch of Eco Single Currency",
    "Africa International Design Awards 2026",
    "Institute asserts statutory mandate, seeks stronger governance culture",
    "Applications open for Festive Fund Grants (Australia)",
    "How Comoros Is Turning Climate Commitments Into Real Progress",
]

BUSINESS_LIKED = [
    "Oil prices fall to one-week low as Iran war fears ease",
    "Coca-Cola hikes full-year forecast after World Cup marketing boost",
    "Visa plans to trim 7% of its workforce",
    "South Korean market at three-month low as AI selloff intensifies",
]

BUSINESS_DISLIKED = [
    "Erwin Tulfo files measures to slash power bills via VAT, system loss cuts",
    "GCash gathers top global tech leaders shaping the future of AI and cybersecurity at the 5th iGnite Innovation Summit",
    "SK hynix Plans To Diminish CXMT's Golden Period With The Only Way It Knows; Technological Superiority, As It Wins Over Chinese Customers With LPDDR6 RAM",
]

# Maps a category label (lowercased) to its (liked, disliked) example lists
CATEGORIES = {
    "world": (WORLD_LIKED, WORLD_DISLIKED),
    "business": (BUSINESS_LIKED, BUSINESS_DISLIKED),
}
