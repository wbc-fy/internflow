import json

from app.config import LLM_PROVIDER
from app.models.schemas import (
    AnalyzeRequest,
    InterviewPrepRequest,
    InterviewPrepResponse,
)
from app.services.analyzer import clean_json_text, rule_based_analyze
from app.services.llm_client import get_llm_client


def fallback_interview_prep(data: InterviewPrepRequest) -> InterviewPrepResponse:
    analysis = rule_based_analyze(
        AnalyzeRequest(
            jd=data.jd,
            resume=data.resume,
        )
    )

    return InterviewPrepResponse(
        self_introduction=(
            f"您好，我对 {data.company} 的 {data.position} 岗位非常感兴趣。"
            "我有 Python 后端开发和 AI 应用项目经验，希望能结合项目经历参与实际业务开发。"
        ),
        key_focus=[
            "熟悉自己的项目背景、技术选型和实现过程。",
            "重点准备 JD 中出现但简历中体现较少的技能。",
            "准备解释自己在项目中具体负责了什么，以及项目结果。"
        ],
        questions=[
            {
                "category": "project",
                "question": "请介绍一下你的 InternFlow 项目。",
                "answer_hint": "说明项目背景、核心功能、技术栈、你负责的部分和项目亮点。"
            },
            {
                "category": "technical",
                "question": f"你如何理解这些缺失技能：{', '.join(analysis.missing_skills) if analysis.missing_skills else '暂无明显缺失技能'}？",
                "answer_hint": "可以说明你目前的学习进度，以及准备用什么方式补齐。"
            },
            {
                "category": "behavioral",
                "question": "你为什么想申请这个实习岗位？",
                "answer_hint": "结合岗位方向、个人项目经历和职业规划回答。"
            }
        ]
    )


def prepare_interview(data: InterviewPrepRequest) -> InterviewPrepResponse:
    if LLM_PROVIDER.lower() == "none":
        return fallback_interview_prep(data)

    client = get_llm_client()

    system_prompt = """
You are InternFlow, an AI interview preparation assistant.
Generate interview preparation content based on the job description and resume.
Return only valid JSON.
Do not include markdown.
Do not include explanations outside JSON.
"""

    user_prompt = f"""
Company:
{data.company}

Position:
{data.position}

Job Description:
{data.jd}

Resume:
{data.resume}

Return JSON with exactly this structure:
{{
  "self_introduction": "Chinese self introduction, 80-120 words",
  "key_focus": ["focus point 1", "focus point 2", "focus point 3"],
  "questions": [
    {{
      "category": "technical",
      "question": "question text",
      "answer_hint": "how to answer this question"
    }},
    {{
      "category": "project",
      "question": "question text",
      "answer_hint": "how to answer this question"
    }},
    {{
      "category": "behavioral",
      "question": "question text",
      "answer_hint": "how to answer this question"
    }}
  ]
}}
"""

    try:
        result_text = client.generate(system_prompt, user_prompt)
        json_text = clean_json_text(result_text)
        result_data = json.loads(json_text)
        return InterviewPrepResponse(**result_data)
    except Exception as e:
        print(f"Interview prep failed, fallback to rule-based prep: {e}")
        return fallback_interview_prep(data)