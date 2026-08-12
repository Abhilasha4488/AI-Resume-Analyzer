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

## Deployment / Live Demo

You can publish a live demo of this Flask app using any cloud host that supports Python web apps (Render, Heroku, Railway, etc.). Below are two quick options.

1) Render (recommended - simple):

- Create a free account on https://render.com and connect your GitHub repository.
- For a `Web Service` choose `Python` and set the `Start Command` to:

	`gunicorn app:app`

- Add environment variables (from `config.py`) under the service's `Environment` settings.
- Deploy — Render will build using `requirements.txt` and run the `gunicorn` command.

Render automation (recommended)

- This repo includes `render.yaml` at the project root. When you connect the repository, Render will detect `render.yaml` and create/update the service automatically.
- Ensure these environment variables are set in Render's service settings (keys shown; values should come from your production/account settings):

	- `SECRET_KEY`
	- `DATABASE` (optional; default is a local SQLite file included in the repo)
	- `UPLOAD_FOLDER` (optional)
	- `ADMIN_USERNAME`, `ADMIN_PASSWORD`
	- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`

Example Render steps:

1. In Render, create a new `Web Service` and choose "Connect a repository".
2. Select `Abhilasha4488/AI-Resume-Analyzer` and the `main` branch.
3. Make sure the `Build Command` is `pip install -r requirements.txt` and `Start Command` is `gunicorn app:app` (these are set in `render.yaml`).
4. Under "Environment", add the secrets listed above.
5. Deploy — Render will build and serve your app.

2) Heroku (via GitHub Actions):

- Create a Heroku app and note its name.
- In your GitHub repo, add the following repository secrets: `HEROKU_API_KEY`, `HEROKU_APP_NAME`, `HEROKU_EMAIL`.
- This repository already includes a GitHub Actions workflow at `.github/workflows/deploy-heroku.yml` that will deploy on push to `main`.
- The project contains a `Procfile` with `web: gunicorn app:app` and `gunicorn` is added to `requirements.txt`.

Local run (for testing before deploy):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python database/init_db.py
python app.py
```

If you want, I can also add a Dockerfile or set up a GitHub Actions workflow for Render — tell me which provider you prefer and I will add the automation. 
