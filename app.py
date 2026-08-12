from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file
)

from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import sqlite3
import os
import config

from utils.parser import extract_resume_text
from utils.analyzer import extract_skills
from utils.ats_score import calculate_ats_score
from utils.recommender import recommend_jobs
from utils.improvement import generate_improvement_suggestions

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Create Flask App
app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

app.config["MAIL_SERVER"] = config.MAIL_SERVER
app.config["MAIL_PORT"] = config.MAIL_PORT
app.config["MAIL_USE_TLS"] = config.MAIL_USE_TLS
app.config["MAIL_USERNAME"] = config.MAIL_USERNAME
app.config["MAIL_PASSWORD"] = config.MAIL_PASSWORD
app.config["MAIL_DEFAULT_SENDER"] = config.MAIL_DEFAULT_SENDER

mail = Mail(app)


# =========================
# Database Connection
# =========================
def get_db_connection():
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# File Validation
# =========================
def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )


# =========================
# Home Route
# =========================
@app.route('/')
def home():
    return render_template('index.html')


# =========================
# Register Route
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()

        try:
            conn.execute(
                '''
                INSERT INTO users(fullname, email, password)
                VALUES (?, ?, ?)
                ''',
                (fullname, email, password)
            )

            conn.commit()

            flash('Registration successful! Please login.', 'success')

            return redirect(url_for('login'))

        except sqlite3.IntegrityError:

            flash('Email already exists!', 'danger')

        finally:
            conn.close()

    return render_template('register.html')


# =========================
# Login Route
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()

        user = conn.execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user['password'], password):

            session['user_id'] = user['id']
            session['fullname'] = user['fullname']

            flash('Login successful!', 'success')

            return redirect(url_for('dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html')


# =========================
# Forgot Password
# =========================

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email", "").strip()

        if not email:
            flash(
                "Please enter your email address.",
                "danger"
            )
            return render_template("forgot_password.html")

        conn = get_db_connection()

        user = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user:

            session["reset_user_id"] = user["id"]

            return redirect(url_for("reset_password"))

        flash(
            "No account found with this email address.",
            "danger"
        )

    return render_template("forgot_password.html")


# =========================
# Reset Password
# =========================

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    user_id = session.get("reset_user_id")

    if not user_id:

        flash(
            "Please request a password reset first.",
            "warning"
        )

        return redirect(url_for("forgot_password"))

    if request.method == "POST":

        password = request.form.get("password", "")
        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not password or not confirm_password:

            flash(
                "Please enter both password fields.",
                "danger"
            )

            return render_template("reset_password.html")

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template("reset_password.html")

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "danger"
            )

            return render_template("reset_password.html")

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()

        conn.execute(
            """
            UPDATE users
            SET password = ?
            WHERE id = ?
            """,
            (hashed_password, user_id)
        )

        conn.commit()
        conn.close()

        session.pop("reset_user_id", None)

        flash(
            "Password reset successfully. Please login.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("reset_password.html")

# =========================
# Dashboard Route
# =========================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    resumes = conn.execute(
        """
        SELECT * FROM resumes
        WHERE user_id=?
        ORDER BY upload_date DESC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        resumes=resumes
    )


# =========================
# Upload Resume
# =========================
@app.route("/upload", methods=["GET", "POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        if "resume" not in request.files:
            flash("No file selected", "danger")
            return redirect(request.url)

        file = request.files["resume"]

        if file.filename == "":
            flash("Choose a resume file", "danger")
            return redirect(request.url)

        if file and allowed_file(file.filename):

            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

            filename = f"{session['user_id']}_{secure_filename(file.filename)}"

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(filepath)

            conn = get_db_connection()

            conn.execute(
                """
                INSERT INTO resumes(user_id, filename, resume_score, ats_score)
                VALUES(?,?,?,?)
                """,
                (
                    session["user_id"],
                    filename,
                    0,
                    0
                )
            )

            conn.commit()
            conn.close()

            flash("Resume uploaded successfully!", "success")

            return redirect(url_for("dashboard"))

        flash("Only PDF and DOCX files are allowed.", "danger")

    return render_template("upload_resume.html")


# =========================
# Resume Analysis
# =========================
@app.route("/analysis/<int:resume_id>")
def analysis(resume_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    resume = conn.execute(
        """
        SELECT * FROM resumes
        WHERE id=? AND user_id=?
        """,
        (resume_id, session["user_id"])
    ).fetchone()

    if resume is None:
        conn.close()
        flash("Resume not found.", "danger")
        return redirect(url_for("dashboard"))

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume["filename"]
    )

    if not os.path.exists(filepath):
        conn.close()
        flash("Resume file not found.", "danger")
        return redirect(url_for("dashboard"))

    # =========================
    # Extract Resume Information
    # =========================

    text = extract_resume_text(filepath)

    skills = extract_skills(text)

    ats_score, missing_skills = calculate_ats_score(text)

    resume_score = min(len(skills) * 10, 100)

    jobs = recommend_jobs(skills)

    # =========================
    # AI Improvement Suggestions
    # =========================

    improvement_suggestions = generate_improvement_suggestions(
        ats_score,
        resume_score,
        skills,
        missing_skills,
        text
    )

    # =========================
    # Update Database
    # =========================

    conn.execute(
        """
        UPDATE resumes
        SET ats_score=?, resume_score=?
        WHERE id=?
        """,
        (ats_score, resume_score, resume_id)
    )

    conn.commit()

    # =========================
    # Resume History
    # =========================

    history = conn.execute(
        """
        SELECT ats_score, resume_score
        FROM resumes
        WHERE user_id=?
        ORDER BY upload_date
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    labels = []
    ats_history = []
    resume_history = []

    for i, row in enumerate(history, start=1):

        labels.append(f"Resume {i}")

        ats_history.append(row["ats_score"])

        resume_history.append(row["resume_score"])

    # =========================
    # Analysis Page
    # =========================

    return render_template(
        "analysis.html",

        resume=resume,

        skills=skills,

        ats_score=ats_score,

        resume_score=resume_score,

        missing_skills=missing_skills,

        jobs=jobs,

        resume_text=text,

        chart_labels=labels,

        ats_history=ats_history,

        resume_history=resume_history,

        improvement_suggestions=improvement_suggestions
    )
    
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if (
            username == config.ADMIN_USERNAME and
            password == config.ADMIN_PASSWORD
        ):

            session["admin"] = True

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Admin Login", "danger")

    return render_template("admin_login.html")  

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    total_users = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    total_resumes = conn.execute(
        "SELECT COUNT(*) FROM resumes"
    ).fetchone()[0]

    average_ats = conn.execute(
        "SELECT AVG(ats_score) FROM resumes"
    ).fetchone()[0]

    history = conn.execute("""
        SELECT upload_date, ats_score
        FROM resumes
        ORDER BY upload_date
    """).fetchall()

    chart_labels = [row["upload_date"] for row in history]
    chart_values = [row["ats_score"] for row in history]

    if average_ats is None:
        average_ats = 0

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_resumes=total_resumes,
        average_ats=round(average_ats, 2),
        chart_labels=chart_labels,
        chart_values=chart_values
    )
    
@app.route("/admin/users")
def admin_users():

    if "admin" not in session:
        return redirect(url_for("admin"))

    search = request.args.get("search", "")

    conn = get_db_connection()

    if search:

        users = conn.execute("""
            SELECT *
            FROM users
            WHERE fullname LIKE ?
            OR email LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%")).fetchall()

    else:

        users = conn.execute("""
            SELECT *
            FROM users
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return render_template(
        "admin_users.html",
        users=users,
        search=search
    )
@app.route("/admin/delete_user/<int:user_id>")
def delete_user(user_id):

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM resumes WHERE user_id=?",
        (user_id,)
    )

    conn.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    flash("User deleted successfully!", "success")

    return redirect(url_for("admin_users"))

@app.route("/admin/resumes")
def admin_resumes():

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    resumes = conn.execute("""
        SELECT
            resumes.*,
            users.fullname,
            users.email
        FROM resumes
        JOIN users
        ON resumes.user_id = users.id
        ORDER BY resumes.upload_date DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin_resumes.html",
        resumes=resumes
    )
@app.route("/admin/leaderboard")
def ats_leaderboard():

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    leaderboard = conn.execute("""
        SELECT
            users.fullname,
            users.email,
            resumes.ats_score,
            resumes.resume_score
        FROM resumes
        JOIN users
        ON resumes.user_id = users.id
        ORDER BY resumes.ats_score DESC
    """).fetchall()

    conn.close()

    return render_template(
        "leaderboard.html",
        leaderboard=leaderboard
    )
    
@app.route("/admin/download/<filename>")
def download_resume(filename):

    if "admin" not in session:
        return redirect(url_for("admin"))

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    return send_file(filepath, as_attachment=True)


@app.route("/download_report/<int:resume_id>")
def download_report(resume_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    resume = conn.execute(
        """
        SELECT * FROM resumes
        WHERE id=? AND user_id=?
        """,
        (resume_id, session["user_id"])
    ).fetchone()

    conn.close()

    if resume is None:
        flash("Resume not found.", "danger")
        return redirect(url_for("dashboard"))

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume["filename"]
    )

    if not os.path.exists(filepath):
        flash("Resume file not found.", "danger")
        return redirect(url_for("dashboard"))

    text = extract_resume_text(filepath)
    skills = extract_skills(text)
    ats_score, missing_skills = calculate_ats_score(text)
    resume_score = min(len(skills) * 10, 100)
    jobs = recommend_jobs(skills)

    pdf_file = os.path.join(
        app.config["UPLOAD_FOLDER"],
        f"Resume_Report_{resume_id}.pdf"
    )

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_file)
    story = []

    story.append(Paragraph("<b>AI Resume Analyzer Report</b>", styles["Title"]))
    story.append(Paragraph(f"ATS Score: {ats_score}%", styles["BodyText"]))
    story.append(Paragraph(f"Resume Score: {resume_score}%", styles["BodyText"]))
    story.append(Paragraph("Skills: " + ", ".join(skills), styles["BodyText"]))
    story.append(Paragraph("Recommended Jobs: " + ", ".join(jobs), styles["BodyText"]))
    story.append(Paragraph("Missing Skills: " + ", ".join(missing_skills), styles["BodyText"]))

    doc.build(story)

    return send_file(pdf_file, as_attachment=True)

@app.route("/email_report/<int:resume_id>")
def email_report(resume_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    resume = conn.execute(
        "SELECT * FROM resumes WHERE id=? AND user_id=?",
        (resume_id, session["user_id"])
    ).fetchone()

    conn.close()

    if resume is None:
        flash("Resume not found.", "danger")
        return redirect(url_for("dashboard"))

    pdf_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        f"Resume_Report_{resume_id}.pdf"
    )

    # Generate report if it doesn't exist
    if not os.path.exists(pdf_path):
        return redirect(
            url_for("download_report", resume_id=resume_id)
        )

    # Check email configuration
    sender = app.config.get("MAIL_DEFAULT_SENDER")

    if not sender:
        flash(
            "Email service is not configured. Please configure MAIL_USERNAME and MAIL_DEFAULT_SENDER.",
            "danger"
        )
        return redirect(url_for("analysis", resume_id=resume_id))

    msg = Message(
        subject="Your Resume Analysis Report",
        sender=sender,
        recipients=[user["email"]]
    )

    msg.body = (
        f"Hello {user['fullname']},\n\n"
        "Please find your Resume Analysis Report attached.\n\n"
        "Regards,\n"
        "AI Resume Analyzer"
    )

    with open(pdf_path, "rb") as f:
        msg.attach(
            f"Resume_Report_{resume_id}.pdf",
            "application/pdf",
            f.read()
        )

    mail.send(msg)

    flash("Email sent successfully!", "success")

    return redirect(
        url_for("analysis", resume_id=resume_id)
    )
# =========================
# Logout
# =========================

# =========================
# Certificates / Achievements
# =========================

@app.route("/certificates")
def certificates():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    certificates = conn.execute(
        """
        SELECT *
        FROM certificates
        WHERE user_id=?
        ORDER BY issue_date DESC, id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "certificates.html",
        certificates=certificates
    )


@app.route("/certificates/add", methods=["GET", "POST"])
def add_certificate():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        organization = request.form.get("organization", "").strip()
        issue_date = request.form.get("issue_date", "").strip()
        certificate_url = request.form.get("certificate_url", "").strip()
        description = request.form.get("description", "").strip()

        if not title:
            flash("Certificate title is required.", "danger")
            return redirect(url_for("add_certificate"))

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO certificates
            (
                user_id,
                title,
                organization,
                issue_date,
                certificate_url,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                title,
                organization,
                issue_date,
                certificate_url,
                description
            )
        )

        conn.commit()
        conn.close()

        flash("Certificate added successfully! 🏆", "success")

        return redirect(url_for("certificates"))

    return render_template("add_certificate.html")


@app.route("/certificates/delete/<int:certificate_id>")
def delete_certificate(certificate_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    certificate = conn.execute(
        """
        SELECT *
        FROM certificates
        WHERE id=? AND user_id=?
        """,
        (certificate_id, session["user_id"])
    ).fetchone()

    if certificate is None:
        conn.close()

        flash("Certificate not found.", "danger")

        return redirect(url_for("certificates"))

    conn.execute(
        """
        DELETE FROM certificates
        WHERE id=? AND user_id=?
        """,
        (certificate_id, session["user_id"])
    )

    conn.commit()
    conn.close()

    flash("Certificate deleted successfully.", "success")

    return redirect(url_for("certificates"))

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "success")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
