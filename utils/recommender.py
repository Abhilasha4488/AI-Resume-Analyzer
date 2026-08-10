def recommend_jobs(skills):
    
    jobs = []

    skills = [skill.lower() for skill in skills]

    if "python" in skills and "flask" in skills:
        jobs.append("Python Flask Developer")

    if "java" in skills:
        jobs.append("Java Developer")

    if "react" in skills:
        jobs.append("Frontend React Developer")

    if "machine learning" in skills:
        jobs.append("Machine Learning Engineer")

    if "sql" in skills:
        jobs.append("Database Developer")

    if len(jobs) == 0:
        jobs.append("Software Developer Intern")

    return jobs