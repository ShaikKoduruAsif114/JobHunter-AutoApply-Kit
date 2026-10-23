#!/usr/bin/env python3
"""
Main Batch Application Runner
Orchestrates:
1. Job discovery based on candidate preferences and branch/CGPA.
2. Launching Chrome in remote debugging mode.
3. Pre-filling application forms & attaching resumes.
4. Auto-detecting submissions and syncing to Excel.
5. Interactive batch loop.
"""

import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

from core.browser_manager import ensure_chrome_running, DEFAULT_PORT
from core.job_discovery import discover_jobs
from core.form_filler import fill_application_form
from core.tracker import sync_submissions

CONFIG_FILE = Path("config/profile.json")
STATE_FILE = Path("config/pipeline_state.json")
EXCEL_PATH = Path("Job_Applications_Tracker.xlsx")
USER_DATA_DIR = Path.home() / ".autoapply_chrome_profile"

def load_profile() -> dict:
    if not CONFIG_FILE.exists():
        template = Path("config/profile_template.json")
        if template.exists():
            with open(template, "r", encoding="utf-8") as f:
                return json.load(f)
        print("⚠️ No profile found. Please run 'python setup_wizard.py' first.")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"jobs": {}}
    return {"jobs": {}}

def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def run_application_batch(batch_size: int = 8):
    profile = load_profile()
    state = load_state()

    # 1. Sync any existing submissions first
    newly_synced = sync_submissions(USER_DATA_DIR, STATE_FILE, EXCEL_PATH)
    if newly_synced > 0:
        print(f"📥 Synced {newly_synced} confirmed submissions to {EXCEL_PATH.name}!\n")

    # 2. Discover live jobs matching profile
    candidate_jobs = discover_jobs(profile, limit=50)
    
    # Filter out already submitted jobs
    submitted_links = set(j.get("apply_link", "").strip().lower() for j in state.get("jobs", {}).values() if j.get("status") == "submitted")
    pending_jobs = [j for j in candidate_jobs if j["apply_link"].strip().lower() not in submitted_links]

    if not pending_jobs:
        print("🎉 You have applied to all currently discovered live roles matching your criteria!")
        print(f"Check {EXCEL_PATH.name} for your submission history.")
        return 0

    target_batch = pending_jobs[:batch_size]
    print("=" * 65)
    print(f"🚀 PRE-FILLING BATCH OF {len(target_batch)} APPLICATIONS IN CHROME")
    print("=" * 65)

    ensure_chrome_running(port=DEFAULT_PORT, user_data_dir=USER_DATA_DIR)

    opened_list = []

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{DEFAULT_PORT}")
        context = browser.contexts[0]

        # Reuse first blank tab if present
        first_page = context.pages[0] if context.pages and context.pages[0].url.startswith("chrome://") else None

        for idx, job in enumerate(target_batch, 1):
            comp = job["company"]
            title = job["title"]
            loc = job["location"]
            url = job["apply_link"]
            track = job.get("track", "SDE")
            is_india = job.get("location_tier", "").lower() == "india"

            print(f"[{idx}/{len(target_batch)}] Opening: {comp} — {title}")
            print(f"      📍 Location: {loc} | Track: {track}")

            if idx == 1 and first_page:
                page = first_page
            else:
                page = context.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                time.sleep(2)

                filled_items = fill_application_form(page, profile, track=track, is_india=is_india)

                inps = page.locator("input:visible, textarea:visible").count()
                fcount = sum(1 for j in range(inps) if page.locator("input:visible, textarea:visible").nth(j).input_value())

                opened_list.append({
                    "company": comp,
                    "title": title,
                    "location": loc,
                    "filled": fcount,
                    "total": inps,
                    "url": url,
                    "track": track
                })
                print(f"      ✅ Pre-filled {fcount}/{inps} fields ({len(set(filled_items))} tags attached)")

            except Exception as e:
                print(f"      ⚠️ Note on page: {e}")
                opened_list.append({
                    "company": comp,
                    "title": title,
                    "location": loc,
                    "filled": 0,
                    "total": 0,
                    "url": url,
                    "track": track
                })

        # Save to pipeline state
        for item in opened_list:
            jid = f"{item['company'][:3].upper()}-{abs(hash(item['url'])) % 100000}"
            state.setdefault("jobs", {})[jid] = {
                "id": jid,
                "company": item["company"],
                "title": item["title"],
                "location": item["location"],
                "apply_link": item["url"],
                "track": item["track"],
                "status": "prefilled_in_browser",
                "opened_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }

        save_state(state)

    print("\n" + "=" * 65)
    print(f"🎉 BATCH READY: {len(opened_list)} applications open in Chrome!")
    print("=" * 65)
    for i, r in enumerate(opened_list, 1):
        print(f"  {i}. {r['company']} — {r['title']} ({r['location']})")
        print(f"     Fields filled: {r['filled']}/{r['total']} | Link: {r['url']}")
    print("=" * 65)
    print("👉 Switch to Chrome, review each pre-filled form, and click 'Submit Application'.")
    print("=" * 65 + "\n")
    return len(opened_list)

def main():
    while True:
        count = run_application_batch(batch_size=8)
        if count == 0:
            break
        print("Waiting for you to review and submit in Chrome...")
        ans = input("Press [Enter] or type '.' for next batch, or 'q' to quit: ").strip().lower()
        if ans in ['q', 'quit', 'exit']:
            print("👋 Finished session. All submissions saved to Job_Applications_Tracker.xlsx!")
            break

if __name__ == "__main__":
    main()
