# AI Resume Analyzer

A smart Flask-based application for analyzing resumes, scoring ATS compatibility, and suggesting improvements to increase the chances of landing an interview.

## Project Description for Portfolio

Built an AI-powered resume evaluation platform that helps users upload their resumes, detect missing skills, benchmark ATS performance, and receive actionable recommendations for improving job-readiness. The project combines resume parsing, scoring logic, data storage, and a polished dashboard to create a practical career-tech application with real-world usefulness.

## Why This Project Matters

Recruiters often rely on ATS systems to filter resumes before a human reviews them. This project addresses that gap by helping candidates understand how well their resume matches job expectations and what they need to improve.

## Key Features

- Resume upload for PDF and DOCX files
- ATS score analysis
- Skill extraction from uploaded resumes
- Job recommendations based on detected skills
- Resume improvement suggestions
- Admin dashboard for monitoring users and resumes
- Report download in PDF format
- Email report delivery support
- Dark mode interface
- Secure login and registration flow

## Tech Stack

- Python
- Flask
- SQLite
- ReportLab
- PyMuPDF
- python-docx
- HTML, CSS, JavaScript

## Project Structure

```text
AI-Resume-Analyzer/
├── app.py
├── config.py
├── check_db.py
├── requirements.txt
├── README.md
├── resume_analyzer.db
├── database/
│   └── init_db.py
├── docs/
│   └── screenshots/
│       └── README.md
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
│   ├── admin_dashboard.html
│   ├── admin_login.html
│   ├── admin_resumes.html
│   ├── admin_users.html
│   ├── analysis.html
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── leaderboard.html
│   ├── login.html
│   ├── profile.html
│   ├── recommendations.html
│   ├── register.html
│   ├── reports.html
│   ├── upload_resume.html
│   └── users.html
├── uploads/
│   └── resumes/
├── utils/
│   ├── analyzer.py
│   ├── ats_score.py
│   ├── improvement.py
│   ├── parser.py
│   ├── pdf_report.py
│   └── recommender.py
└── README.md
```

## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/Abhilasha4488/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Initialize the database

```bash
python database/init_db.py
```

5. Start the app

```bash
python app.py
```

Open the app in your browser at:

```text
http://192.168.0.200:5000
```

## Default Admin Credentials

- Username: `admin`
- Password: `admin123`

## Notes

- SQLite is used for local data storage.
- Email functionality is configured with Flask-Mail and Gmail SMTP.
- For production deployment, you should move sensitive values like secret keys and email credentials to environment variables.

## License

This project is intended for educational and portfolio use.

## Author

Abhilasha
