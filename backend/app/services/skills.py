SKILL_CATEGORIES = {
    "programming_languages": [
        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "C++",
    ],
    "backend_frameworks": [
        "FastAPI",
        "Flask",
        "Django",
        "Spring Boot",
    ],
    "databases": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "SQLite",
        "MongoDB",
        "Redis",
    ],
    "devops_tools": [
        "Git",
        "Docker",
        "Linux",
        "Nginx",
    ],
    "frontend": [
        "React",
        "Vue",
        "HTML",
        "CSS",
    ],
    "ai_agent": [
        "LangChain",
        "LangGraph",
        "RAG",
        "LLM",
        "Prompt Engineering",
    ],
}


def get_all_skills() -> list[str]:
    all_skills = []

    for skills in SKILL_CATEGORIES.values():
        all_skills.extend(skills)

    return all_skills


def get_skill_category(skill_name: str) -> str:
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            if skill.lower() == skill_name.lower():
                return category

    return "unknown"