from typing import List
from fastapi import FastAPI
from app.config import LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY
from app.database import init_db
from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ApplicationCreate,
    ApplicationResponse,
)
from app.services.analyzer import analyze_application
from app.services.application_service import create_application, list_applications
app = FastAPI(title="InternFlow API")
init_db()

@app.get("/")
def root():
    return {"message": "InternFlow API is running"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(data: AnalyzeRequest):
    return analyze_application(data)
from app.config import LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY


@app.get("/api/config")
def get_config():
    return {
        "llm_provider": LLM_PROVIDER,
        "has_openai_key": bool(OPENAI_API_KEY),
        "has_anthropic_key": bool(ANTHROPIC_API_KEY)
    }

@app.post("/api/applications", response_model=ApplicationResponse)
def add_application(data: ApplicationCreate):
    return create_application(data)


@app.get("/api/applications", response_model=List[ApplicationResponse])
def get_applications():
    return list_applications()