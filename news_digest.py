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

GNEWS_API_KEY = os.environ["GNEWS_API_KEY"]

BASE_URL = "https://gnews.io/api/v4/top-headlines"

QUERIES = [
    ("World", "world", None),
    ("India", "nation", "in"),
    ("Business", "business", None),
]


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
    for label, category, country in QUERIES:
        entries = get_headlines(category, country)
        if entries:
            lines = "\n\n".join(
                f"- {title}\n  {description}" if description else f"- {title}"
                for title, description in entries
            )
        else:
            lines = "(no articles returned)"
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
