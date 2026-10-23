# 🚀 JobHunter AutoApply Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Playwright Supported](https://img.shields.io/badge/Engine-Playwright%20CDP-green.svg)](https://playwright.dev/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

> **Autonomous Job Discovery, Intelligent ATS Form Pre-Filler & Application Tracker**  
> Designed for college students, freshers, and 2026/2027 batch grads from **any branch (CSE, ECE, Civil, Mechanical, etc.)** to apply for **verified, live tech roles** with zero repetitive manual typing.

---

## 📌 Table of Contents
- [⚡ 3-Minute Quick Start](#-3-minute-quick-start)
- [🛠️ How It Works](#️-how-it-works)
- [🎯 Complete Customization Guide](#-complete-customization-guide)
  - [1. Branch, College & CGPA (With Auto-Cutoff Guardrails)](#1-branch-college--cgpa-with-auto-cutoff-guardrails)
  - [2. Target Roles & Tech Stacks](#2-target-roles--tech-stacks)
  - [3. Multi-Resume Routing (SDE vs AI/ML vs Data)](#3-multi-resume-routing-sde-vs-aiml-vs-data)
  - [4. Location Preferences (India First vs Remote)](#4-location-preferences-india-first-vs-remote)
  - [5. Custom Essays & Technical Achievements](#5-custom-essays--technical-achievements)
  - [6. Demographics & EEO Dropdowns](#6-demographics--eeo-dropdowns)
- [📊 Auto-Generated Excel Tracker](#-auto-generated-excel-tracker)
- [💡 Troubleshooting & FAQ](#-troubleshooting--faq)
- [📄 License](#-license)

---

## ⚡ 3-Minute Quick Start

### Step 1: Clone or Download
```bash
git clone https://github.com/ShaikKoduruAsif114/JobHunter-AutoApply-Kit.git
cd JobHunter-AutoApply-Kit
```
*(Or click **Code → Download ZIP** on GitHub and extract the folder).*

### Step 2: 1-Click Dependency Installation
* **On Windows:** Double-click **`install.bat`**
* **On macOS / Linux:**
  ```bash
  pip install -r requirements.txt
  playwright install chromium
  ```

### Step 3: Add Your Resume
Place your resume PDF into the **`resumes/`** folder:
```
JobHunter-AutoApply-Kit/
  └── resumes/
        └── My_Resume.pdf
```

### Step 4: Configure & Run!
* **On Windows:** Double-click **`start.bat`**
* **On macOS / Linux:**
  ```bash
  python setup_wizard.py
  python run_batch.py
  ```

The first time you run it, the interactive **Setup Wizard** will ask for:
1. Your Name, Email, Phone, and City
2. College Name, Degree, Branch (CSE, Civil, ECE, Mech, etc.), CGPA, and Grad Year
3. Target Roles (SDE, AI/ML, Data Science, Full-Stack, etc.)
4. Location Preference (India First vs Remote vs Worldwide)

*(Your settings are saved to `config/profile.json` — you only do this once!)*

### Step 5: Review & 1-Click Submit in Chrome
1. The engine launches Google Chrome in remote debugging mode.
2. It opens **5 to 8 applications simultaneously**, pre-filling all input fields, React-Select dropdowns, and attaching your resume.
3. You review each tab and click **Submit Application**.
4. In your terminal, hit **`[Enter]`** to launch the next batch!
5. Submissions are automatically detected and saved into **`Job_Applications_Tracker.xlsx`**.

---

## 🛠️ How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Active Job Discovery (Greenhouse, Lever, Ashby APIs)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Candidate Filtering Engine                               │
│    • Branch & Keyword Alignment                             │
│    • Experience Guardrail: Strictly 0-1 YOE / Internships   │
│    • CGPA Guardrail: Skips roles with cutoffs above yours   │
│    • Anti-Noise: Excludes non-tech roles (QC, ops, HR, etc.)│
│    • Location Sorting: India first, then Global Remote      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Automated Browser Workspace                              │
│    • Launches Chrome with CDP Remote Debugging (Port 9222)  │
│    • Handles embedded iframes & React-Select dropdowns      │
│    • Attaches correct target resume PDF (Track-Specific)    │
│    • Populates Demographics / EEO / Custom Technical Essays │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Human Approval & Automated Tracking                      │
│    • 1-Click Review & Submit in Chrome                      │
│    • Auto-detects submission confirmation URLs in history   │
│    • Auto-logs entries into Job_Applications_Tracker.xlsx   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Complete Customization Guide

Every single aspect of the application pipeline is customizable in **`config/profile.json`** (or via `python setup_wizard.py`).

### 1. Branch, College & CGPA (With Auto-Cutoff Guardrails)
You do **not** need to be a Computer Science student. You can specify any branch:
```json
"education": {
  "university": "National Institute of Technology, Trichy",
  "degree": "Bachelor of Technology (B.Tech)",
  "major": "Civil Engineering",
  "cgpa": "7.80",
  "cgpa_scale": "10.0",
  "start_month_year": "08/2023",
  "graduation_month_year": "05/2027",
  "graduation_year": "2027",
  "academic_standing": "Senior / Final Year"
}
```
* **Auto-Cutoff Protection:** In `preferences.user_cgpa`, put your exact CGPA (e.g. `7.80`). If a company's job description demands an `8.5+` or `9.0+` cutoff, the engine automatically skips that role so you don't waste time on auto-rejections.

---

### 2. Target Roles & Tech Stacks
In `preferences.target_roles`, list whatever role titles you want the engine to search for:

* **For Frontend Developers:**
  ```json
  "target_roles": ["Frontend Engineer", "React Developer", "UI Engineer", "Software Engineer"]
  ```
* **For Backend / Systems Engineers:**
  ```json
  "target_roles": ["Backend Engineer", "Go Developer", "Java Developer", "SDE", "Systems"]
  ```
* **For AI / ML / Data Science:**
  ```json
  "target_roles": ["AI Engineer", "Machine Learning", "Data Scientist", "Data Analyst", "NLP"]
  ```
* **For Embedded / Hardware:**
  ```json
  "target_roles": ["Embedded Systems", "Firmware", "VLSI", "Hardware Engineer", "Robotics"]
  ```

* **Roles to Exclude:** Any unwanted non-technical or senior roles are blocked in `preferences.excluded_keywords`:
  ```json
  "excluded_keywords": [
    "senior", "sr.", "lead", "principal", "staff", "director", "manager",
    "quality check", "inventory", "trainer", "operations", "recruitment", "sales", "marketing"
  ]
  ```

---

### 3. Multi-Resume Routing (SDE vs AI/ML vs Data)
If you have different resumes tailored for different tracks, place them in the `resumes/` folder and map them in `resumes`:
```json
"resumes": {
  "SDE": "resumes/Resume_SDE.pdf",
  "AI_ML": "resumes/Resume_AIML.pdf",
  "DATA": "resumes/Resume_Data.pdf",
  "DEFAULT": "resumes/General_Resume.pdf"
}
```
* When an **AI/ML** opening is opened, the engine automatically uploads `Resume_AIML.pdf`.
* When an **SDE / Software** opening is opened, it automatically uploads `Resume_SDE.pdf`.

---

### 4. Location Preferences (India First vs Remote)
Set `preferences.target_location_tiers`:
* **Strictly India:** `["India"]` (searches Bengaluru, Hyderabad, Pune, Mumbai, Gurgaon, Noida, Chennai, etc.)
* **India + Global Remote:** `["India", "Global Remote"]`
* **Worldwide:** `["India", "Global Remote", "International"]`

---

### 5. Custom Essays & Technical Achievements
Many application portals (Greenhouse, Lever) ask essay-type questions. You can customize your answers in `essays`:
```json
"essays": {
  "why_join_us": "I want to work with high-performing engineering teams solving large-scale challenges. Your engineering culture, rigorous technical standards, and impact align directly with my drive to build scalable software and apply modern engineering practices.",
  "technical_project": "Engineered an AI game engine in JavaScript using Minimax with alpha-beta pruning and BigInt bitmasks, achieving a 106.6x speedup. Also trained a custom 12.2M-parameter Transformer with RoPE from scratch in PyTorch.",
  "availability": "Available for a 6-month full-time internship starting January 2027 or immediate full-time employment."
}
```

---

### 6. Demographics & EEO Dropdowns
Forms frequently include voluntary demographic and work authorization questions. The engine auto-selects them:
```json
"eeo": {
  "gender": "Male",
  "ethnicity": "South Asian",
  "hispanic": "No",
  "veteran": "Not a veteran",
  "disability": "No",
  "work_auth_in_country": "Yes",
  "require_sponsorship": "No"
}
```
*(Options can also be set to `"Decline to specify"` if preferred).*

---

## 📊 Auto-Generated Excel Tracker

Every confirmed submission is automatically appended to **`Job_Applications_Tracker.xlsx`**:

| Company | Role Title | Location | Track | ATS Platform | Apply Link | Status | Submitted At | Notes |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| **HackerRank** | SDE Intern | Bengaluru | SDE | Greenhouse | [Link](https://job-boards.greenhouse.io) | **Submitted** | Oct 18, 2026 | Confirmed |
| **Enterpret** | Backend Intern | Bengaluru | SDE | Greenhouse | [Link](https://job-boards.greenhouse.io) | **Submitted** | Oct 18, 2026 | Confirmed |
| **Karya** | Research Intern | Bengaluru | AI/ML | Greenhouse | [Link](https://job-boards.greenhouse.io) | **Submitted** | Oct 18, 2026 | Confirmed |
| **Twilio** | MLE Intern | Remote - India | AI/ML | Greenhouse | [Link](https://job-boards.greenhouse.io) | **Submitted** | Oct 18, 2026 | Confirmed |

---

## 💡 Troubleshooting & FAQ

* **Q: Chrome gives connection refused or won't launch?**  
  Close any existing Chrome windows before running `start.bat`. Chrome needs to start with `--remote-debugging-port=9222`.
* **Q: Can I add more companies to scan?**  
  Yes! In `core/job_discovery.py`, add any company's career board slug to the `POPULAR_COMPANIES` list.
* **Q: How does it know I submitted the form?**  
  `core/tracker.py` monitors Chrome history for confirmation tokens (`/confirmation`, `/thanks`, `status=success`) and automatically matches them to the job ID.

---

## 📄 License
Released under the [MIT License](LICENSE). Free for college students, freshers, and job seekers everywhere!

