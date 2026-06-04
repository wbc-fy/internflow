from app.config import LLM_PROVIDER, QWEN_API_KEY, QWEN_MODEL


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
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError(
            "Qwen client is prepared but not implemented yet."
        )


def get_llm_client() -> LLMClient:
    provider = LLM_PROVIDER.lower()

    if provider == "qwen":
        return QwenClient(
            api_key=QWEN_API_KEY,
            model=QWEN_MODEL,
        )

    return NoLLMClient()