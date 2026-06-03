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