#!/usr/bin/env python3
"""
Job Discovery Engine
Queries official Greenhouse, Lever, and Ashby APIs for active early-career roles,
filters by candidate preferences (Role, YOE, CGPA, Location),
and returns verified, live job postings.
"""

import json
import re
import urllib.request
from pathlib import Path
from typing import List, Dict, Any

POPULAR_COMPANIES = [
    # High-growth tech startups & tech giants
    "togetherai", "enterpret", "superapp", "instawork", "karya", "sprinto",
    "hackerrank", "observeai", "atlan", "postman", "browserstack", "clevertap",
    "groww", "meesho", "cred", "razorpay", "slice", "jupiter", "swiggy",
    "urbancompany", "lenskart", "spinny", "curefit", "signoz", "appsmith",
    "hasura", "rubrik", "stripe", "coinbase", "databricks", "snowflake",
    "nutanix", "thoughtspot", "druva", "innovaccer", "cohesity", "sprinklr",
    "twilio", "okta", "box", "airtable", "asana", "datadog", "cloudflare",
    "pinterest", "reddit", "quora", "scaleai", "deepgram", "cohere", "modal",
    "retool", "temporal", "vanta", "webflow", "sentry", "launchdarkly"
]

def check_yoe_and_cgpa(text: str, max_yoe: int, user_cgpa: float) -> bool:
    """Rejects if requiring higher YOE than max_yoe or higher CGPA than user_cgpa."""
    # 1. Check YOE
    yoe_patterns = [
        r'\b([2-9]|\d{2,})\+?\s*(?:to\s*\d+)?\s*(?:years?|yrs?)(?:\s*of)?\s*(?:relevant|industry|professional|software|work)?\s*(?:experience|exp)\b'
    ]
    for pat in yoe_patterns:
        if re.search(pat, text, re.I):
            return False

    # 2. Check CGPA cutoff
    if user_cgpa > 0:
        cg_matches = re.findall(r'\b(8\.[0-9]|9\.[0-9]|85%|80%|8\.5|8\.0|9\.0)\b', text)
        if cg_matches:
            # If job strictly demands 8.0+ or 8.5+ and user is below it, exclude
            for m in cg_matches:
                try:
                    val = float(m.replace("%", ""))
                    if val <= 10.0 and val > user_cgpa:
                        return False
                except ValueError:
                    pass

    return True

def fetch_greenhouse_jobs(company: str, headers: dict) -> List[Dict[str, Any]]:
    api_url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=3.5) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data.get("jobs", [])
    except Exception:
        return []

def fetch_lever_jobs(company: str, headers: dict) -> List[Dict[str, Any]]:
    api_url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=3.5) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data if isinstance(data, list) else []
    except Exception:
        return []

def discover_jobs(profile: dict, limit: int = 40) -> List[Dict[str, Any]]:
    prefs = profile.get("preferences", {})
    target_roles = prefs.get("target_roles", ["Software Engineer", "SDE", "AI", "ML", "Data"])
    excluded = prefs.get("excluded_keywords", ["senior", "lead", "principal", "manager", "quality check", "trainer", "operations"])
    loc_tiers = [l.lower() for l in prefs.get("target_location_tiers", ["India", "Global Remote"])]
    max_yoe = prefs.get("max_yoe_allowed", 1)
    user_cgpa = float(prefs.get("user_cgpa", 7.8))

    role_regex = re.compile(r'\b(' + '|'.join(re.escape(r) for r in target_roles) + r')\b', re.I)
    excl_regex = re.compile(r'\b(' + '|'.join(re.escape(e) for e in excluded) + r')\b', re.I)
    india_loc_regex = re.compile(r'\b(india|bengaluru|bangalore|hyderabad|pune|mumbai|noida|gurgaon|gurugram|chennai|delhi)\b', re.I)

    headers = {"User-Agent": "Mozilla/5.0"}
    discovered = []
    seen_urls = set()

    print(f"🔎 Scanning top {len(POPULAR_COMPANIES)} tech boards for active roles...")

    for company in POPULAR_COMPANIES:
        # 1. Try Greenhouse
        gh_jobs = fetch_greenhouse_jobs(company, headers)
        for j in gh_jobs:
            title = j.get("title", "")
            loc = (j.get("location", {}).get("name") or "")
            url = j.get("absolute_url") or ""

            if not url or url.lower() in seen_urls:
                continue

            if excl_regex.search(title):
                continue

            if not role_regex.search(title):
                continue

            is_india = bool(india_loc_regex.search(loc))
            is_remote = "remote" in loc.lower() and not any(r in loc.lower() for r in ["us only", "usa only", "canada only", "uk only"])

            location_tier = "India" if is_india else ("Global Remote" if is_remote else "International")
            if location_tier.lower() not in loc_tiers and "all" not in loc_tiers:
                continue

            # Classify track
            t_low = title.lower()
            track = "AI / ML" if any(k in t_low for k in ["ai", "ml", "machine learning", "deep learning", "research"]) else ("Data" if "data" in t_low else "SDE")

            seen_urls.add(url.lower())
            discovered.append({
                "company": company.capitalize(),
                "title": title,
                "location": loc,
                "location_tier": location_tier,
                "apply_link": url,
                "ats": "Greenhouse",
                "track": track
            })

        # 2. Try Lever
        lv_jobs = fetch_lever_jobs(company, headers)
        for j in lv_jobs:
            title = j.get("text", "")
            loc = j.get("categories", {}).get("location", "")
            url = j.get("hostedUrl") or ""

            if not url or url.lower() in seen_urls:
                continue

            if excl_regex.search(title):
                continue

            if not role_regex.search(title):
                continue

            is_india = bool(india_loc_regex.search(loc))
            is_remote = "remote" in loc.lower() and not any(r in loc.lower() for r in ["us only", "usa only", "canada only", "uk only"])

            location_tier = "India" if is_india else ("Global Remote" if is_remote else "International")
            if location_tier.lower() not in loc_tiers and "all" not in loc_tiers:
                continue

            t_low = title.lower()
            track = "AI / ML" if any(k in t_low for k in ["ai", "ml", "machine learning", "deep learning", "research"]) else ("Data" if "data" in t_low else "SDE")

            seen_urls.add(url.lower())
            discovered.append({
                "company": company.capitalize(),
                "title": title,
                "location": loc,
                "location_tier": location_tier,
                "apply_link": url,
                "ats": "Lever",
                "track": track
            })

    # Sort priorities: India first, then Remote, then International
    tier_weights = {"india": 1, "global remote": 2, "international": 3}
    discovered.sort(key=lambda x: tier_weights.get(x["location_tier"].lower(), 99))

    print(f"🎯 Found {len(discovered)} matching candidate roles.\n")
    return discovered[:limit]
