def calculate_ats_score(text):
    
    text = text.lower()

    keywords = [
        "python", "java", "sql", "html", "css",
        "javascript", "flask", "django", "react",
        "bootstrap", "git", "github",
        "machine learning", "communication",
        "project", "internship"
    ]

    score = 0
    missing = []

    for keyword in keywords:

        if keyword in text:
            score += 6
        else:
            missing.append(keyword)

    score = min(score, 100)

    return score, missing