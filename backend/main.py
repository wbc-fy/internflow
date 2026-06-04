from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Response, UploadFile, File, Form

from app.config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    QWEN_API_KEY,
)
from app.database import init_db
from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    AnalyzeAndSaveRequest,
    AnalyzeAndSaveResponse,
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
    ApplicationStatsResponse,
    InterviewPrepRequest,
    InterviewPrepResponse,
    ResumeExtractResponse,
)
from app.services.analyzer import analyze_application
from app.services.application_service import (
    create_application,
    list_applications,
    update_application_status,
    delete_application_by_id,
    get_application_stats,
)
from app.services.interview_service import prepare_interview
from app.services.llm_client import get_llm_client
from app.services.file_extractor import extract_text_from_pptx_upload


app = FastAPI(title="InternFlow API")

init_db()


@app.get("/")
def root():
    return {"message": "InternFlow API is running"}


@app.get("/api/config")
def get_config():
    return {
        "llm_provider": LLM_PROVIDER,
        "has_openai_key": bool(OPENAI_API_KEY),
        "has_anthropic_key": bool(ANTHROPIC_API_KEY),
        "has_qwen_key": bool(QWEN_API_KEY),
    }


@app.get("/api/llm/test")
def test_llm():
    client = get_llm_client()

    result = client.generate(
        system_prompt="You are an internship application assistant.",
        user_prompt="Say hello to InternFlow.",
    )

    return {
        "provider": LLM_PROVIDER,
        "result": result,
    }


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(data: AnalyzeRequest):
    return analyze_application(data)


@app.post("/api/analyze/save", response_model=AnalyzeAndSaveResponse)
def analyze_and_save(data: AnalyzeAndSaveRequest):
    analysis = analyze_application(
        AnalyzeRequest(
            jd=data.jd,
            resume=data.resume,
        )
    )

    if analysis.missing_skills:
        missing_skill_text = "、".join(analysis.missing_skills)
    else:
        missing_skill_text = "暂无明显缺失技能"

    if data.notes:
        notes = data.notes
    else:
        notes = f"AI 分析：缺失技能：{missing_skill_text}"

    application = create_application(
        ApplicationCreate(
            company=data.company,
            position=data.position,
            match_score=analysis.match_score,
            status=data.status,
            notes=notes,
        )
    )

    return AnalyzeAndSaveResponse(
        analysis=analysis,
        application=application,
    )


@app.post("/api/analyze/input", response_model=AnalyzeResponse)
async def analyze_with_text_or_pptx(
    jd: str = Form(...),
    resume_text: str | None = Form(None),
    file: UploadFile | None = File(None),
):
    if file is not None:
        try:
            final_resume_text = await extract_text_from_pptx_upload(file)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif resume_text and resume_text.strip():
        final_resume_text = resume_text
    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide either resume_text or a .pptx file.",
        )

    return analyze_application(
        AnalyzeRequest(
            jd=jd,
            resume=final_resume_text,
        )
    )


@app.post("/api/resume/extract", response_model=ResumeExtractResponse)
async def extract_resume(file: UploadFile = File(...)):
    try:
        text = await extract_text_from_pptx_upload(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ResumeExtractResponse(
        filename=file.filename or "",
        file_type=Path(file.filename or "").suffix.lower(),
        text=text,
        text_length=len(text),
    )


@app.post("/api/applications", response_model=ApplicationResponse)
def add_application(data: ApplicationCreate):
    return create_application(data)


@app.get("/api/applications", response_model=List[ApplicationResponse])
def get_applications():
    return list_applications()


@app.get("/api/applications/stats", response_model=ApplicationStatsResponse)
def get_stats():
    return get_application_stats()


@app.patch("/api/applications/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, data: ApplicationStatusUpdate):
    updated_application = update_application_status(application_id, data)

    if updated_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return updated_application


@app.delete("/api/applications/{application_id}", status_code=204)
def delete_application(application_id: int):
    success = delete_application_by_id(application_id)

    if not success:
        raise HTTPException(status_code=404, detail="Application not found")

    return Response(status_code=204)


@app.post("/api/interview/prepare", response_model=InterviewPrepResponse)
def prepare_interview_api(data: InterviewPrepRequest):
    return prepare_interview(data)