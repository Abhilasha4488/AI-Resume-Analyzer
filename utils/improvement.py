def generate_improvement_suggestions(
    ats_score,
    resume_score,
    skills,
    missing_skills,
    resume_text
):

    suggestions = []

    # ATS score suggestions
    if ats_score < 50:
        suggestions.append(
            "Your ATS score is low. Add more job-specific keywords "
            "and improve the structure of your resume."
        )

    elif ats_score < 70:
        suggestions.append(
            "Your ATS score is moderate. Add relevant technical "
            "keywords from the job description to improve your score."
        )

    else:
        suggestions.append(
            "Your ATS score is good. Keep your resume targeted "
            "towards the specific job description."
        )

    # Resume score
    if resume_score < 50:
        suggestions.append(
            "Your resume contains limited skills. Add more relevant "
            "technical and professional skills."
        )

    elif resume_score < 80:
        suggestions.append(
            "Your resume has a good skill set. Consider adding "
            "more advanced or job-specific skills."
        )

    else:
        suggestions.append(
            "Your resume demonstrates a strong range of skills."
        )

    # Missing skills
    if missing_skills:

        skill_text = ", ".join(missing_skills[:8])

        suggestions.append(
            f"Consider adding these missing skills if you have experience "
            f"with them: {skill_text}."
        )

    # Resume length
    word_count = len(resume_text.split())

    if word_count < 250:
        suggestions.append(
            "Your resume appears short. Add relevant projects, "
            "experience, achievements and technical skills."
        )

    elif word_count > 1200:
        suggestions.append(
            "Your resume is quite long. Remove unnecessary information "
            "and keep the most relevant experience."
        )

    else:
        suggestions.append(
            "Your resume length is reasonable. Focus on keeping "
            "the content concise and relevant."
        )

    # Skills section
    if len(skills) < 5:
        suggestions.append(
            "Add a dedicated Technical Skills section containing "
            "relevant programming languages, frameworks, databases "
            "and development tools."
        )

    # Experience / achievements
    experience_keywords = [
        "experience",
        "project",
        "achievement",
        "responsibility",
        "developed",
        "implemented",
        "created"
    ]

    found_experience = any(
        keyword in resume_text.lower()
        for keyword in experience_keywords
    )

    if not found_experience:
        suggestions.append(
            "Add project or experience details. Explain what you built, "
            "what technologies you used and what results you achieved."
        )

    # Final suggestion
    suggestions.append(
        "Use measurable achievements wherever possible, such as "
        "percentages, numbers, performance improvements or user counts."
    )

    return suggestions