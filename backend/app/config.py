import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "none")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-max")
QWEN_BASE_URL = os.getenv(
    "QWEN_BASE_URL",
    "https://dashscope.aliyuncs.com/compatible-mode/v1"
)