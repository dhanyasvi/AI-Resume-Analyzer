from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import AnalysisResult
from app.services.ai_analysis import enrich_analysis
from app.services.pdf_extractor import extract_pdf_text
from app.services.scoring import analyze_resume

app = FastAPI(title="AI Resume Analyzer API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze(resume: UploadFile = File(...), job_description: str = Form(default="")) -> AnalysisResult:
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")
    file_bytes = await resume.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Please upload a PDF smaller than 10 MB.")
    try:
        resume_text = extract_pdf_text(file_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    base = analyze_resume(resume_text, job_description)
    ai_feedback = enrich_analysis(resume_text, job_description, base)
    breakdown = {
        "content": base["ats_score"],
        "keywords": base["job_match_score"],
        "skills": min(100, len(base["detected_skills"]) * 10),
        "impact": 75 if "measurable results" in " ".join(base["strengths"]).lower() else 45,
    }
    return AnalysisResult(
        filename=resume.filename or "resume.pdf",
        extracted_characters=len(resume_text),
        extracted_text_preview=resume_text[:500],
        score_breakdown=breakdown,
        **base,
        **ai_feedback,
    )
