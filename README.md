# 🚀 JobHunter AutoApply Kit (One-Click Shareable Setup)

> **Autonomous Job Discovery, Intelligent ATS Form Pre-Filler & Application Tracker**  
> Designed for college students, freshers, and 2027 batch grads to apply for **verified, live SDE, AI/ML, and Data roles** with zero repetitive manual typing.

---

## ⚡ 3-Minute Quick Start

### Step 1: Install Dependencies
Double-click **`install.bat`** (or open terminal in this folder and run):
```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Add Your Resume
Place your resume PDF into the **`resumes/`** folder:
```
JobHunter-AutoApply-Kit/
  └── resumes/
        └── My_Resume.pdf
```

### Step 3: Configure Your Profile
Double-click **`start.bat`** (or run `python setup_wizard.py`).  
An interactive wizard will ask for:
* Your Name, Email, Phone, and City
* College, Degree, Major/Branch (Civil, CSE, ECE, Mech, etc.), CGPA, and Graduation Batch
* Target Roles (SDE, AI/ML, Data Science, Quant, etc.)
* Location Preference (India First vs Remote vs Worldwide)

*(This saves your settings into `config/profile.json` — you only have to do this once!)*

### Step 4: Run & Apply!
Double-click **`start.bat`** (or run `python run_batch.py`):
1. The engine scans top tech job boards (Greenhouse, Lever, Ashby) for **100% verified active openings**.
2. It launches Google Chrome and opens **5 to 8 applications simultaneously**.
3. It automatically **fills all fields** (Name, Contact, Education, EEO, Technical Essays) and **attaches your resume PDF**.
4. You simply switch to Chrome, give a quick review, and click **Submit Application** on each tab.
5. In the terminal, hit **[Enter]** or send **`.`** to launch the next batch!
6. Every submitted application is automatically detected from the confirmation page and saved into **`Job_Applications_Tracker.xlsx`**.

---

## 🧠 How the Intelligent Engine Works

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Active Job Discovery (Greenhouse, Lever, Ashby, Telegram)│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Candidate Filtering                                      │
│    • Branch & Keyword Alignment                             │
│    • Experience Guardrail: Strictly 0-1 YOE / Internships   │
│    • CGPA Guardrail: Excludes any role above your CGPA      │
│    • Excludes non-tech roles (no quality check, ops, etc.)  │
│    • Location Sorting: India first, then Remote             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Automated Browser Workspace                              │
│    • Launches Chrome with CDP Remote Debugging              │
│    • Handles embedded iframes & React-Select dropdowns      │
│    • Attaches correct target resume PDF                     │
│    • Populates Demographics / EEO / Essays                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Human Approval & Tracking                                │
│    • 1-Click Review & Submit in Chrome                      │
│    • Detects submission confirmation URLs                   │
│    • Auto-logs entries into Job_Applications_Tracker.xlsx   │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Customizing Your Profile (`config/profile.json`)

You can edit `config/profile.json` anytime in any text editor or rerun `python setup_wizard.py`:

```json
{
  "personal": {
    "full_name": "Your Name",
    "email": "your_email@gmail.com",
    "phone": "+91 9876543210",
    "location_city": "Bengaluru, Karnataka, India"
  },
  "education": {
    "university": "Your College Name",
    "degree": "Bachelor of Technology (B.Tech)",
    "major": "Computer Science / Civil / Mechanical",
    "cgpa": "7.8",
    "graduation_year": "2027"
  },
  "preferences": {
    "target_roles": ["Software Engineer", "SDE", "Backend", "AI Engineer", "Machine Learning", "Data Analyst"],
    "target_location_tiers": ["India", "Global Remote"],
    "max_yoe_allowed": 1,
    "user_cgpa": 7.8
  },
  "resumes": {
    "SDE": "resumes/Resume_SDE.pdf",
    "AI_ML": "resumes/Resume_AIML.pdf",
    "DEFAULT": "resumes/Resume.pdf"
  }
}
```

---

## 📋 Auto-Generated Excel Tracker
Every confirmed submission is automatically appended to **`Job_Applications_Tracker.xlsx`**:
* **Company Name**
* **Role Title**
* **Location**
* **Track (SDE / AI / Data)**
* **Platform (Greenhouse / Lever / Direct)**
* **Apply URL**
* **Submission Timestamp**

---

## 💡 Troubleshooting & FAQ

* **Q: Chrome didn't open or showed connection error?**  
  Make sure all previous Chrome windows are closed before launching, or ensure Chrome is installed in the standard `Program Files` directory.
* **Q: Can I add custom companies to scan?**  
  Yes! In `core/job_discovery.py`, add any company's career board slug to the `POPULAR_COMPANIES` list.
* **Q: How does it prevent submitting expired jobs?**  
  The discovery engine queries live ATS board APIs and filters out requisitions returning "Page not found" or "Closed".
