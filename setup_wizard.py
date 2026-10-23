#!/usr/bin/env python3
"""
Interactive Profile Setup Wizard for JobHunter AutoApply Kit
Quickly sets up candidate profile, academic background, resume routing, and job preferences.
"""

import os
import sys
import json
import shutil
from pathlib import Path

CONFIG_DIR = Path("config")
PROFILE_FILE = CONFIG_DIR / "profile.json"
TEMPLATE_FILE = CONFIG_DIR / "profile_template.json"
RESUMES_DIR = Path("resumes")

def prompt(text, default=""):
    suffix = f" [{default}]: " if default else ": "
    val = input(text + suffix).strip()
    return val if val else default

def main():
    print("=" * 65)
    print("🎓 JOBHUNTER AUTOAPPLY - CANDIDATE SETUP WIZARD")
    print("=" * 65)
    print("Configure your profile once. The pipeline uses this to discover")
    print("matching jobs, auto-fill forms, attach resumes, and track submissions.\n")

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    RESUMES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Personal Details
    print("--- 1. Personal & Contact Details ---")
    full_name = prompt("Full Name (as on official ID)", "Alex Kumar")
    name_parts = full_name.split()
    first_name = name_parts[0] if name_parts else ""
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
    pref_name = prompt("Preferred First Name", first_name)
    email = prompt("Email Address", "alex.kumar@gmail.com")
    phone = prompt("Phone Number (with country code)", "+91 9876543210")
    city = prompt("Current City / State / Country", "Bengaluru, Karnataka, India")

    # 2. Education Details
    print("\n--- 2. Academic Background & Branch ---")
    college = prompt("College / University Name", "Indian Institute of Technology")
    degree = prompt("Degree", "Bachelor of Technology (B.Tech)")
    major = prompt("Branch / Field of Study (e.g. Computer Science, Civil, Mechanical)", "Computer Science")
    cgpa = prompt("Current CGPA (out of 10.0)", "8.0")
    grad_year = prompt("Graduation Year", "2027")
    start_date = prompt("College Start Date (MM/YYYY)", "08/2023")
    grad_date = prompt("Expected Graduation Date (MM/YYYY)", f"05/{grad_year}")

    # 3. Links
    print("\n--- 3. Professional Links ---")
    linkedin = prompt("LinkedIn Profile URL", f"https://www.linkedin.com/in/{first_name.lower()}-{last_name.lower()}")
    github = prompt("GitHub Profile URL", f"https://github.com/{first_name.lower()}{last_name.lower()}")
    portfolio = prompt("Portfolio / Personal Website URL (or GitHub)", github)

    # 4. Job Preferences
    print("\n--- 4. Target Roles & Track ---")
    print("Select primary interest:")
    print("  [1] SDE / Software Engineering / Full-Stack / Backend / Frontend")
    print("  [2] AI / Machine Learning / Data Science / NLP / LLMs")
    print("  [3] Quant / Trading / High-Performance Systems")
    print("  [4] All Technical Roles (SDE + AI/ML + Data)")
    choice = prompt("Choose an option [1-4]", "4")

    if choice == "1":
        target_roles = ["Software Engineer", "SDE", "Backend", "Frontend", "Full Stack", "Systems Engineer"]
    elif choice == "2":
        target_roles = ["AI Engineer", "Machine Learning", "Data Scientist", "Data Analyst", "Deep Learning", "NLP"]
    elif choice == "3":
        target_roles = ["Quantitative", "Quant Research", "Low Latency", "Trading Systems", "C++ Developer"]
    else:
        target_roles = ["Software Engineer", "SDE", "Backend", "Frontend", "AI Engineer", "Machine Learning", "Data Scientist"]

    loc_choice = prompt("Target Locations: [1] Strictly India  [2] India + Global Remote  [3] Worldwide", "2")
    if loc_choice == "1":
        target_locs = ["India"]
    elif loc_choice == "2":
        target_locs = ["India", "Global Remote"]
    else:
        target_locs = ["India", "Global Remote", "International"]

    # 5. Resume Routing
    print("\n--- 5. Resume Configuration ---")
    print("Place your PDF resume into the 'resumes/' folder in this directory.")
    resume_filename = prompt("Enter your resume PDF filename (e.g. My_Resume.pdf)", "Resume.pdf")
    resume_path = f"resumes/{resume_filename}"

    # 6. Build and Save Profile
    profile_data = {
        "personal": {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "preferred_name": pref_name,
            "email": email,
            "phone": phone,
            "location_city": city,
            "country": "India"
        },
        "links": {
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio
        },
        "education": {
            "university": college,
            "degree": degree,
            "major": major,
            "cgpa": cgpa,
            "cgpa_scale": "10.0",
            "start_month_year": start_date,
            "graduation_month_year": grad_date,
            "graduation_year": grad_year,
            "academic_standing": "Senior / Final Year"
        },
        "preferences": {
            "target_roles": target_roles,
            "excluded_keywords": [
                "senior", "sr.", "lead", "principal", "staff", "director", "manager",
                "quality check", "inventory", "trainer", "operations", "recruitment", "sales", "marketing"
            ],
            "target_location_tiers": target_locs,
            "max_yoe_allowed": 1,
            "user_cgpa": float(cgpa) if cgpa.replace(".", "", 1).isdigit() else 7.5
        },
        "resumes": {
            "SDE": resume_path,
            "AI_ML": resume_path,
            "DEFAULT": resume_path
        },
        "essays": {
            "why_join_us": "I want to work with high-performing engineering teams solving large-scale challenges. Your engineering culture, rigorous technical standards, and impact in the ecosystem align directly with my drive to build scalable software and apply modern engineering practices.",
            "technical_project": "Developed a high-performance system from scratch demonstrating algorithmic optimization, clean API design, and modular architecture. Focused on efficiency, edge-case resilience, and production-grade quality standards.",
            "availability": "Available for 6-month full-time internship or immediate employment as per hiring timelines."
        },
        "eeo": {
            "gender": "Male",
            "ethnicity": "South Asian",
            "hispanic": "No",
            "veteran": "Not a veteran",
            "disability": "No",
            "work_auth_in_country": "Yes",
            "require_sponsorship": "No" if "india" in city.lower() else "Yes"
        }
    }

    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2)

    print("\n" + "=" * 65)
    print("🎉 SETUP COMPLETE!")
    print(f"Profile saved to: {PROFILE_FILE.resolve()}")
    print(f"Resume target set to: {RESUMES_DIR.resolve()} / {resume_filename}")
    print("=" * 65)
    print("👉 Now run 'python run_batch.py' or double-click 'start.bat' to begin applying!")

if __name__ == "__main__":
    main()
