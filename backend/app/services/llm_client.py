from openai import OpenAI

from app.config import (
    LLM_PROVIDER,
    QWEN_API_KEY,
    QWEN_MODEL,
    QWEN_BASE_URL,
)


class LLMClient:
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class NoLLMClient(LLMClient):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        return (
            "LLM provider is not configured. "
            "Current mode uses rule-based analysis only."
        )


class QwenClient(LLMClient):
    def __init__(self, api_key: str, model: str, base_url: str):
        if not api_key:
            raise ValueError("QWEN_API_KEY is missing.")

        self.model = model
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content


def get_llm_client() -> LLMClient:
    provider = LLM_PROVIDER.lower()

    if provider == "qwen":
        return QwenClient(
            api_key=QWEN_API_KEY,
            model=QWEN_MODEL,
            base_url=QWEN_BASE_URL,
        )

    return NoLLMClient()