from pydantic import BaseModel
from typing import List


class AnalyzeRequest(BaseModel):
    jd: str
    resume: str


class AnalyzeResponse(BaseModel):
    position_summary: str
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    resume_suggestions: List[str]
    email_draft: str