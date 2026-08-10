# AI Resume Analyzer

AI Resume Analyzer is a Flask-based web application that helps users upload their resumes, analyze ATS compatibility, extract key skills, receive job recommendations, and view improvement suggestions.

## Features

- User registration and login
- Resume upload support for PDF and DOCX files
- ATS score analysis
- Skill extraction and matching
- Job recommendations based on detected skills
- Improvement suggestions for resume optimization
- Admin dashboard for user and resume management
- Downloadable PDF report
- Email report functionality
- Dark mode UI

## Tech Stack

- Python
- Flask
- SQLite
- ReportLab
- PyMuPDF / python-docx
- HTML, CSS, JavaScript

## Project Structure

```text
AI-Resume-Analyzer/
├── app.py
├── config.py
├── check_db.py
├── requirements.txt
├── resume_analyzer.db
├── database/
│   └── init_db.py
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

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

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

5. Run the application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Default Admin Login

- Username: `admin`
- Password: `admin123`

## Notes

- The project uses SQLite for local storage.
- Email sending is configured through Flask-Mail and Gmail SMTP.
- For production use, store secret keys and mail credentials in environment variables.

## License

This project is for educational and personal use.

## Author

Abhilasha
