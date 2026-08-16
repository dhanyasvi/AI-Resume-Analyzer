import re

from app.schemas import CoverageItem, KeywordResult

COMMON_SKILLS = ["Python", "JavaScript", "TypeScript", "React", "Next.js", "Node.js", "FastAPI", "SQL", "PostgreSQL", "MongoDB", "AWS", "Docker", "Kubernetes", "Git", "GitHub Actions", "CI/CD", "Jest", "React Testing Library", "Figma", "Tableau", "Power BI", "Excel", "Machine Learning", "Data Analysis", "Agile", "Scrum", "REST API", "GraphQL", "HTML", "CSS", "Tailwind CSS", "Accessibility"]
SECTION_PATTERNS = {"summary": r"\b(summary|profile|objective|about me)\b", "experience": r"\b(experience|employment|work history|professional experience)\b", "education": r"\b(education|academic background|qualifications)\b", "skills": r"\b(skills|technical skills|core competencies)\b"}
ACTION_VERBS = r"\b(built|led|created|improved|increased|reduced|developed|delivered|designed|managed|launched|optimized)\b"


def _contains(text: str, phrase: str) -> bool:
    return bool(re.search(r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)", text.lower()))


def analyze_resume(resume_text: str, job_description: str) -> dict:
    lower_text = resume_text.lower()
    detected_skills = [skill for skill in COMMON_SKILLS if _contains(lower_text, skill)]
    job_keywords = [skill for skill in COMMON_SKILLS if _contains(job_description, skill)][:12]
    keyword_results = [KeywordResult(keyword=skill, found=skill in detected_skills) for skill in job_keywords]
    missing_skills = [item.keyword for item in keyword_results if not item.found]
    found_sections = [name for name, pattern in SECTION_PATTERNS.items() if re.search(pattern, lower_text)]
    quantified = len(re.findall(r"\b\d+(?:[.,]\d+)?\s?(?:%|\+|users|customers|projects|hours|days|months)\b", lower_text))
    action_verbs = len(re.findall(ACTION_VERBS, lower_text))
    word_count = len(re.findall(r"\b[\w'-]+\b", resume_text))
    contact_score = 10 if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text) else 0
    ats_score = min(100, 10 + contact_score + min(40, len(found_sections) * 10) + min(20, quantified * 5) + min(20, len(detected_skills) * 2))
    job_match_score = round(100 * (len(job_keywords) - len(missing_skills)) / len(job_keywords)) if job_keywords else min(100, 35 + len(detected_skills) * 4)
    strengths, improvements = [], []
    if "experience" in found_sections: strengths.append("Your resume includes an experience section, making your background easier to scan.")
    if quantified >= 2: strengths.append("You use measurable results, making achievements more credible.")
    if len(detected_skills) >= 5: strengths.append(f"We detected {len(detected_skills)} technical or professional skills.")
    if action_verbs >= 3: strengths.append("Your experience uses action-oriented language.")
    if not strengths: strengths.append("Your resume text was successfully extracted and is ready for detailed improvement.")
    if "summary" not in found_sections: improvements.append("Add a short professional summary tailored to the target role.")
    if quantified < 2: improvements.append("Add numbers where possible, such as revenue, time saved, users served, or percentage improvements.")
    if missing_skills: improvements.append("If accurate, include these job-description skills: " + ", ".join(missing_skills[:4]) + ".")
    if "skills" not in found_sections: improvements.append("Create a clear skills section so applicant-tracking systems can scan your expertise.")
    if not improvements: improvements.append("Tailor your summary and top achievements to the language of each job description.")
    keyword_score = job_match_score if job_keywords else min(100, len(detected_skills) * 12)
    coverage_items = [
        CoverageItem(label="Contact details", score=100 if contact_score else 30, status="Strong" if contact_score else "Needs work", detail="Email address detected." if contact_score else "Add a professional email address."),
        CoverageItem(label="Core resume sections", score=len(found_sections) * 25, status="Strong" if len(found_sections) >= 4 else "Needs work", detail=f"{len(found_sections)} of 4 key sections found: {', '.join(found_sections) or 'none'}."),
        CoverageItem(label="Skills coverage", score=min(100, len(detected_skills) * 10), status="Strong" if len(detected_skills) >= 7 else "Build up", detail=f"{len(detected_skills)} recognized skills found."),
        CoverageItem(label="Measurable impact", score=min(100, quantified * 25), status="Strong" if quantified >= 3 else "Needs work", detail=f"{quantified} quantified achievement signals found."),
        CoverageItem(label="Action language", score=min(100, action_verbs * 15), status="Strong" if action_verbs >= 5 else "Build up", detail=f"{action_verbs} strong action verbs found."),
        CoverageItem(label="Target keywords", score=keyword_score, status="Strong" if keyword_score >= 70 else "Needs work", detail="Matched to the supplied job description." if job_keywords else "Add a job description for tailored matching."),
    ]
    return {"overall_score": round(ats_score * .55 + job_match_score * .45), "ats_score": ats_score, "job_match_score": job_match_score, "detected_skills": detected_skills, "missing_skills": missing_skills, "keyword_results": keyword_results, "strengths": strengths[:3], "improvements": improvements[:4], "coverage_items": coverage_items, "resume_metrics": {"words": word_count, "sections": len(found_sections), "skills": len(detected_skills), "impact_signals": quantified, "action_verbs": action_verbs, "job_keywords": len(job_keywords)}}
