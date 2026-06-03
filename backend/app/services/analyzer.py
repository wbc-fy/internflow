from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.skills import get_all_skills


def analyze_application(data: AnalyzeRequest) -> AnalyzeResponse:
    jd_text = data.jd.lower()
    resume_text = data.resume.lower()

    matched_skills = []
    missing_skills = []

    all_skills = get_all_skills()

    for skill in all_skills:
        skill_lower = skill.lower()

        if skill_lower in jd_text:
            if skill_lower in resume_text:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    total_required = len(matched_skills) + len(missing_skills)

    if total_required == 0:
        match_score = 50
    else:
        match_score = int(len(matched_skills) / total_required * 100)

    if matched_skills:
        skill_text = "、".join(matched_skills)
    else:
        skill_text = "相关项目"

    return AnalyzeResponse(
        position_summary=f"该岗位描述中识别到 {total_required} 个主要技能要求。",
        match_score=match_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        resume_suggestions=[
            "补充 JD 中出现但简历中没有体现的技能关键词。",
            "把项目经历写得更具体，例如说明你负责了什么、用了什么技术、实现了什么结果。",
            "优先突出和岗位要求直接相关的项目。",
        ],
        email_draft=(
            "您好，我对贵公司的该实习岗位非常感兴趣。"
            f"我目前具备 {skill_text} 经验，"
            "希望有机会进一步交流。谢谢！"
        ),
    )