"""
Weekly news digest — fetches World, India, and Business headlines from
GNews and writes them to digest.txt. Designed to run on a schedule via
GitHub Actions (see .github/workflows/news-digest.yml), which commits
digest.txt back to the repo so it's readable at a permanent raw URL.

Required environment variable (set as a GitHub Actions secret):
  GNEWS_API_KEY   - your GNews API key
"""

import os
import time
import requests
from relevance_filter import classify

GNEWS_API_KEY = os.environ["GNEWS_API_KEY"]

BASE_URL = "https://gnews.io/api/v4/top-headlines"

QUERIES = [
    ("World", "world", None, "keywords_then_ml"),
    ("India", "nation", "in", "none"),
    ("Business", "business", None, "keywords_then_ml"),
]

AFRICA_KEYWORDS = [
    "africa", "african", "algeria", "angola", "benin", "botswana",
    "burkina faso", "burundi", "cameroon", "cape verde", "central african republic",
    "chad", "comoros", "congo", "djibouti", "egypt", "equatorial guinea",
    "eritrea", "eswatini", "ethiopia", "gabon", "gambia", "ghana", "guinea",
    "ivory coast", "kenya", "lesotho", "liberia", "libya", "madagascar",
    "malawi", "mali", "mauritania", "mauritius", "morocco", "mozambique",
    "namibia", "niger", "nigeria", "rwanda", "senegal", "seychelles",
    "sierra leone", "somalia", "south africa", "south sudan", "sudan",
    "tanzania", "togo", "tunisia", "uganda", "zambia", "zimbabwe",
]


def contains_keyword(text, keywords):
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)


def get_headlines(category, country=None):
    params = {"category": category, "lang": "en", "apikey": GNEWS_API_KEY}
    if country:
        params["country"] = country

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    return [
        (a["title"], a.get("description", "").strip())
        for a in articles
    ]


def build_digest_body():
    sections = []
    for label, category, country, filter_mode in QUERIES:
        entries = get_headlines(category, country)

        if filter_mode == "ml_filter":
            category_key = label.lower()
            kept = [
                (title, description)
                for title, description in entries
                if classify(f"{title}. {description}", category_key) == "liked"
            ]
        elif filter_mode == "exclude_keywords":
            kept = [
                (title, description)
                for title, description in entries
                if not contains_keyword(f"{title} {description}", AFRICA_KEYWORDS)
            ]
        elif filter_mode == "keywords_then_ml":
            category_key = label.lower()
            after_keywords = [
                (title, description)
                for title, description in entries
                if not contains_keyword(f"{title} {description}", AFRICA_KEYWORDS)
            ]
            kept = [
                (title, description)
                for title, description in after_keywords
                if classify(f"{title}. {description}", category_key) == "liked"
            ]
        else:  # "none" — no filtering
            kept = entries

        if kept:
            lines = "\n\n".join(
                f"- {title}\n  {description}" if description else f"- {title}"
                for title, description in kept
            )
        else:
            lines = "(no articles passed the relevance filter)"
        sections.append(f"{label}\n{'-' * len(label)}\n{lines}")
        time.sleep(2)  # small pause to avoid rapid-fire rate limiting
    return "\n\n".join(sections)


def write_digest_file(body, path="digest.txt"):
    with open(path, "w") as f:
        f.write(body)


def main():
    body = build_digest_body()
    write_digest_file(body)
    print("Digest written successfully.")
    print(body)


if __name__ == "__main__":
    main()
