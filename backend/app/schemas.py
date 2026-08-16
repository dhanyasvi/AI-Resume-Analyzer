from pydantic import BaseModel, Field


class KeywordResult(BaseModel):
    keyword: str
    found: bool


class CoverageItem(BaseModel):
    label: str
    score: int = Field(ge=0, le=100)
    detail: str
    status: str


class AnalysisResult(BaseModel):
    filename: str
    extracted_characters: int
    overall_score: int = Field(ge=0, le=100)
    ats_score: int = Field(ge=0, le=100)
    job_match_score: int = Field(ge=0, le=100)
    detected_skills: list[str]
    missing_skills: list[str]
    keyword_results: list[KeywordResult]
    strengths: list[str]
    improvements: list[str]
    executive_assessment: str
    priority_actions: list[str]
    rewritten_bullet: str
    score_breakdown: dict[str, int]
    coverage_items: list[CoverageItem]
    resume_metrics: dict[str, int]
    ai_enabled: bool
    extracted_text_preview: str
