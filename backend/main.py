from fastapi import FastAPI
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.analyzer import analyze_application

app = FastAPI(title="InternFlow API")


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