from pydantic import BaseModel
from typing import List,Optional
from typing import Dict


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



class ApplicationCreate(BaseModel):
    company: str
    position: str
    match_score: int
    status: str = "准备中"
    notes: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    company: str
    position: str
    match_score: int
    status: str
    notes: Optional[str]
    created_at: str

class ApplicationStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
class AnalyzeAndSaveRequest(BaseModel):
    company: str
    position: str
    jd: str
    resume: str
    status: str = "准备中"
    notes: Optional[str] = None


class AnalyzeAndSaveResponse(BaseModel):
    analysis: AnalyzeResponse
    application: ApplicationResponse



class ApplicationStatsResponse(BaseModel):
    total: int
    average_match_score: float
    status_counts: Dict[str, int]