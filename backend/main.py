from typing import List
from fastapi import FastAPI, HTTPException
from app.config import LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY
from app.database import init_db
from app.models.schemas import (
    ApplicationStatusUpdate,
    AnalyzeRequest,
    AnalyzeResponse,
    ApplicationCreate,
    ApplicationResponse,
)
from app.services.analyzer import analyze_application
from app.services.application_service import (
    create_application,
    list_applications,
    update_application_status,
)
from app.services.llm_client import get_llm_client
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
@app.patch("/api/applications/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, data: ApplicationStatusUpdate):
    updated_application = update_application_status(application_id, data)

    if updated_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return updated_application
@app.get("/api/llm/test")
def test_llm():
    client = get_llm_client()

    result = client.generate(
        system_prompt="You are an internship application assistant.",
        user_prompt="Say hello to InternFlow."
    )

    return {
        "provider": LLM_PROVIDER,
        "result": result
    }