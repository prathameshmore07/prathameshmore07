#!/usr/bin/env python3
"""
Scrape real daily contribution counts from GitHub's public, unauthenticated
contributions endpoint and write data/contributions.json with derived stats.

Compatible with render_heatmap_svg.py
"""

import datetime
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

# ---------------- CONFIG ---------------- #

USERNAME = os.environ.get("GH_PROFILE_USER", "prathameshmore07")
URL = f"https://github.com/users/{USERNAME}/contributions"

OUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "contributions.json",
)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html",
}

# ---------------------------------------- #


def fetch_days():
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    cells = soup.select("td.ContributionCalendar-day")

    if not cells:
        print(
            "ERROR: GitHub contribution cells not found. GitHub markup may have changed.",
            file=sys.stderr,
        )
        sys.exit(1)

    days = []

    for td in cells:
        date = td.get("data-date")

        if not date:
            continue

        tooltip = None

        td_id = td.get("id")

        if td_id:
            tooltip = soup.find("tool-tip", attrs={"for": td_id})

        text = tooltip.get_text(strip=True) if tooltip else ""

        if re.search(r"no contributions", text, re.I):
            count = 0
        else:
            m = re.match(r"(\d+)", text)
            count = int(m.group(1)) if m else 0

        days.append(
            {
                "date": date,
                "count": count,
            }
        )

    days.sort(key=lambda x: x["date"])

    return days


def compute_current_streak(days):
    idx = len(days) - 1

    if idx >= 0 and days[idx]["count"] == 0:
        idx -= 1

    streak = 0

    end = idx

    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1

    if streak == 0:
        return {
            "length": 0,
            "start": None,
            "end": None,
        }

    return {
        "length": streak,
        "start": days[idx + 1]["date"],
        "end": days[end]["date"],
    }


def compute_longest_streak(days):
    longest = 0
    run = 0

    start = None
    end = None

    run_start = None

    for i, d in enumerate(days):

        if d["count"] > 0:

            if run == 0:
                run_start = i

            run += 1

            if run > longest:
                longest = run
                start = days[run_start]["date"]
                end = d["date"]

        else:
            run = 0

    return {
        "length": longest,
        "start": start,
        "end": end,
    }


def build_data(days):
    total = sum(d["count"] for d in days)

    active = sum(1 for d in days if d["count"] > 0)

    best = max(days, key=lambda x: x["count"])

    monthly = {}

    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "range": {
            "start": days[0]["date"],
            "end": days[-1]["date"],
        },
        "total_contributions": total,
        "active_days": active,
        "avg_per_active_day": round(total / active, 1) if active else 0,
        "current_streak": compute_current_streak(days),
        "longest_streak": compute_longest_streak(days),
        "best_day": {
            "date": best["date"],
            "count": best["count"],
        },
        "monthly": [
            {
                "month": m,
                "total": monthly[m],
            }
            for m in sorted(monthly)
        ],
        "days": days,
    }


def main():
    days = fetch_days()

    data = build_data(days)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(days)} contribution days.")
    print(f"Total contributions : {data['total_contributions']}")
    print(f"Current streak      : {data['current_streak']['length']}")
    print(f"Longest streak      : {data['longest_streak']['length']}")


if __name__ == "__main__":
    main()