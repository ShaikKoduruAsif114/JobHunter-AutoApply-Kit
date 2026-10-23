#!/usr/bin/env python3
"""
Deep Form Filler Engine
Auto-fills ATS forms (Greenhouse, Lever, Ashby, and custom portals).
Handles iframes, React-Select dropdowns, standard selects, radios, checkboxes, and file uploads.
"""

import time
import os
from pathlib import Path
from typing import Dict, Any, List

def get_target_scope(page):
    """Finds the form scope, handling embedded iframes if present."""
    for frame in page.frames:
        if frame == page.main_frame:
            continue
        try:
            if frame.locator("#first_name, input[name*='name'], input[name*='first_name'], form[action*='greenhouse']").count() > 0:
                return frame
        except Exception:
            pass
    return page

def resolve_resume_path(profile: dict, track: str) -> str:
    """Finds the appropriate resume PDF path from profile configuration."""
    resumes = profile.get("resumes", {})
    t_low = (track or "").lower()
    
    if "ai" in t_low or "ml" in t_low or "data" in t_low:
        r_path = resumes.get("AI_ML") or resumes.get("DEFAULT")
    else:
        r_path = resumes.get("SDE") or resumes.get("DEFAULT")

    if not r_path:
        # Fallback to any PDF found in resumes directory
        resumes_dir = Path("resumes")
        if resumes_dir.exists():
            pdfs = list(resumes_dir.glob("*.pdf"))
            if pdfs:
                return str(pdfs[0].resolve())
        return ""
    
    p = Path(r_path)
    if not p.is_absolute():
        p = Path.cwd() / p
    return str(p.resolve()) if p.exists() else ""

def fill_application_form(page, profile: dict, track: str = "SDE", is_india: bool = True) -> List[str]:
    """Fills all fields on the page or iframe and attaches the target resume."""
    scope = get_target_scope(page)
    pers = profile.get("personal", {})
    edu = profile.get("education", {})
    links = profile.get("links", {})
    essays = profile.get("essays", {})
    eeo = profile.get("eeo", {})

    resume_path = resolve_resume_path(profile, track)
    filled_items = []

    # 1. Resume File Upload
    if resume_path and os.path.exists(resume_path):
        for fi in scope.locator("input[type='file']").all():
            try:
                fi.set_input_files(resume_path)
                filled_items.append(f"Resume ({Path(resume_path).name})")
                break
            except Exception:
                pass

    # 2. Text Inputs & Textareas
    for inp in scope.locator("input:visible, textarea:visible").all():
        try:
            itype = (inp.get_attribute("type") or "text").lower()
            if itype in ["hidden", "submit", "button", "checkbox", "radio", "file"]:
                continue
            if inp.input_value():
                continue

            name = (inp.get_attribute("name") or inp.get_attribute("id") or "").lower()
            ph = (inp.get_attribute("placeholder") or "").lower()
            lbl = inp.locator("xpath=../..").inner_text().lower() if inp.locator("xpath=../..").count() > 0 else ""
            desc = f"{name} {ph} {lbl}"

            # Names
            if "preferred" in desc and ("first" in desc or "name" in desc):
                inp.fill(pers.get("preferred_name") or pers.get("first_name", ""))
                filled_items.append("Preferred Name")
            elif ("first" in desc or "fname" in desc or "given" in desc) and "last" not in desc:
                inp.fill(pers.get("first_name", ""))
                filled_items.append("First Name")
            elif ("last" in desc or "lname" in desc or "surname" in desc or "family" in desc) and "first" not in desc:
                inp.fill(pers.get("last_name", ""))
                filled_items.append("Last Name")
            elif "full" in desc and "name" in desc and "user" not in desc:
                inp.fill(pers.get("full_name", ""))
                filled_items.append("Full Name")
            elif "name" in desc and not any(k in desc for k in ["first", "last", "school", "company", "file", "org", "user"]):
                inp.fill(pers.get("full_name", ""))
                filled_items.append("Full Name")

            # Contact
            elif "email" in desc:
                inp.fill(pers.get("email", ""))
                filled_items.append("Email")
            elif "phone" in desc or "mobile" in desc or "tel" in desc:
                inp.fill(pers.get("phone", ""))
                filled_items.append("Phone")

            # Links
            elif "linkedin" in desc:
                inp.fill(links.get("linkedin", ""))
                filled_items.append("LinkedIn")
            elif "github" in desc or "git" in desc:
                inp.fill(links.get("github", ""))
                filled_items.append("GitHub")
            elif any(k in desc for k in ["portfolio", "website", "blog", "personal url"]):
                inp.fill(links.get("portfolio") or links.get("github", ""))
                filled_items.append("Portfolio/Website")

            # Location
            elif any(k in desc for k in ["city", "candidate-location", "location"]):
                inp.fill(pers.get("location_city", "Bengaluru, Karnataka, India"))
                filled_items.append("Location/City")
            elif "country" in desc:
                inp.fill(pers.get("country", "India"))
                filled_items.append("Country")

            # Education Details
            elif any(k in desc for k in ["school", "university", "college", "institution"]):
                inp.fill(edu.get("university", ""))
                filled_items.append("University")
            elif any(k in desc for k in ["degree", "qualification"]):
                inp.fill(edu.get("degree", "Bachelor of Technology"))
                filled_items.append("Degree")
            elif any(k in desc for k in ["major", "discipline", "field of study", "department"]):
                inp.fill(edu.get("major", ""))
                filled_items.append("Major")
            elif "gpa" in desc or "cgpa" in desc:
                inp.fill(str(edu.get("cgpa", "")))
                filled_items.append("CGPA")
            elif "start" in desc and ("date" in desc or "year" in desc) and "earliest" not in desc:
                val = edu.get("start_month_year", "08/2023")
                inp.fill(val if "/" in ph else val.split("/")[-1])
                filled_items.append("Start Date")
            elif ("end" in desc or "grad" in desc) and ("date" in desc or "year" in desc) and "earliest" not in desc:
                val = edu.get("graduation_month_year", "05/2027")
                inp.fill(val if "/" in ph else val.split("/")[-1])
                filled_items.append("Graduation Date")

            # Essays & Questions
            elif any(k in desc for k in ["why", "excited", "interest", "inspire"]):
                inp.fill(essays.get("why_join_us", "I want to work with engineering teams tackling high-scale software challenges."))
                filled_items.append("Essay: Why Us")
            elif any(k in desc for k in ["project", "proud", "challenge", "built"]):
                inp.fill(essays.get("technical_project", "Engineered and shipped high-performance software systems with strong algorithmic design."))
                filled_items.append("Essay: Technical Project")
            elif "availab" in desc or "earliest start" in desc:
                inp.fill(essays.get("availability", "Available immediately / as per internship timelines."))
                filled_items.append("Availability")
        except Exception:
            pass

    # 3. React-Select Dropdowns
    for sc in scope.locator(".select, div[class*='select__container'], div[class*='select-shell']").all():
        try:
            txt = sc.inner_text().lower()
            ctrl = sc.locator(".select__control").first
            if ctrl.count() == 0 or not ctrl.is_visible():
                continue
            choice = None
            if "school" in txt or "university" in txt:
                choice = edu.get("university", "Indian Institute of Technology")
            elif "degree" in txt:
                choice = "Bachelor"
            elif "discipline" in txt or "major" in txt:
                choice = edu.get("major", "Engineering")
            elif "gender" in txt and "pronoun" not in txt:
                choice = eeo.get("gender", "Male")
            elif "ethnicity" in txt or "race" in txt:
                choice = eeo.get("ethnicity", "South Asian")
            elif "hispanic" in txt:
                choice = eeo.get("hispanic", "No")
            elif "veteran" in txt:
                choice = "Not a"
            elif "disability" in txt:
                choice = "No"
            elif "authorized" in txt:
                choice = eeo.get("work_auth_in_country", "Yes")
            elif "sponsorship" in txt or "visa" in txt:
                choice = "No" if is_india else "Yes"

            if choice:
                ctrl.click()
                time.sleep(0.15)
                opt = scope.locator(f"[class*='option']:has-text('{choice}')").first
                if opt.count() > 0:
                    opt.click()
                    filled_items.append(f"Dropdown: {choice}")
                else:
                    scope.page.keyboard.press("Escape")
        except Exception:
            pass

    # 4. Standard Select Dropdowns
    for sel in scope.locator("select:visible").all():
        try:
            stxt = (sel.get_attribute("name") or sel.get_attribute("id") or "").lower()
            for opt in sel.locator("option").all():
                otxt = (opt.inner_text() or "").lower()
                val = opt.get_attribute("value")
                if "gender" in stxt and eeo.get("gender", "male").lower() in otxt:
                    sel.select_option(value=val)
                    filled_items.append(f"Select: {eeo.get('gender')}")
                    break
                elif "disability" in stxt and ("no" in otxt or "not" in otxt):
                    sel.select_option(value=val)
                    filled_items.append("Select: No Disability")
                    break
        except Exception:
            pass

    # 5. Radio Buttons
    for r in scope.locator("input[type='radio']:visible").all():
        try:
            ptext = r.locator("xpath=../..").inner_text().lower() if r.locator("xpath=../..").count() > 0 else ""
            rval = (r.get_attribute("value") or "").lower()

            if ("authorized to work" in ptext or "legal right" in ptext) and "sponsorship" not in ptext:
                if "yes" in rval or "yes" in ptext:
                    r.check(force=True)
                    filled_items.append("Radio: Work Auth (Yes)")
            elif "sponsorship" in ptext or "visa" in ptext:
                target = "no" if is_india else "yes"
                if target in rval or target in ptext:
                    r.check(force=True)
                    filled_items.append(f"Radio: Sponsorship ({target.title()})")
            elif "18 years" in ptext or "18 or older" in ptext:
                if "yes" in rval or "yes" in ptext:
                    r.check(force=True)
                    filled_items.append("Radio: 18+ (Yes)")
        except Exception:
            pass

    # 6. Consent & Terms Checkboxes
    for cb in scope.locator("input[type='checkbox']:visible").all():
        try:
            ptext = cb.locator("xpath=..").inner_text().lower() if cb.locator("xpath=..").count() > 0 else ""
            if any(k in ptext for k in ["consent", "privacy", "terms", "agree", "accurate", "certify"]):
                if not cb.is_checked():
                    cb.check(force=True)
                    filled_items.append("Checkbox: Consent")
        except Exception:
            pass

    return filled_items
