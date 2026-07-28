"""
Weekly news digest — fetches World, India, and Business headlines from
GNews and emails them to yourself. Designed to run on a schedule via
GitHub Actions (see .github/workflows/news-digest.yml).

Required environment variables (set as GitHub Actions secrets):
  GNEWS_API_KEY   - your GNews API key
  GMAIL_USER      - the Gmail address sending the email
  GMAIL_APP_PASS  - a Gmail App Password (not your normal password —
                    generate one at https://myaccount.google.com/apppasswords)
  RECIPIENT_EMAIL - the email address that should receive the digest
                    (can be the same as GMAIL_USER, i.e. email yourself)
"""

import os
import smtplib
import requests
from email.mime.text import MIMEText

GNEWS_API_KEY = os.environ["GNEWS_API_KEY"]
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASS = os.environ["GMAIL_APP_PASS"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]

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
    return [a["title"] for a in articles]


def build_digest_body():
    sections = []
    for label, category, country in QUERIES:
        titles = get_headlines(category, country)
        if titles:
            lines = "\n".join(f"- {t}" for t in titles)
        else:
            lines = "(no articles returned)"
        sections.append(f"{label}\n{'-' * len(label)}\n{lines}")
    return "\n\n".join(sections)


def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "Your Sunday News Digest"
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASS)
        server.send_message(msg)


def write_digest_file(body, path="digest.txt"):
    with open(path, "w") as f:
        f.write(body)


def main():
    body = build_digest_body()
    write_digest_file(body)
    send_email(body)
    print("Digest written and emailed successfully.")
    print(body)


if __name__ == "__main__":
    main()
