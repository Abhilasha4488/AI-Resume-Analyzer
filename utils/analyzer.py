import re

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "bootstrap",
    "flask",
    "django",
    "react",
    "node.js",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "linux",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "tensorflow",
    "keras",
    "opencv",
    "pandas",
    "numpy",
    "power bi",
    "tableau",
    "excel"
]

def extract_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill.title())

    return sorted(list(set(found)))