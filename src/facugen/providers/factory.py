from facugen.core import ModelSpec
from facugen.providers.base import LLMProvider
from facugen.providers.openai import OpenAIClient
from facugen.providers.gemini import GeminiClient


def create_provider(model_spec: ModelSpec) -> LLMProvider:
    if model_spec.provider == "openai":
        return OpenAIClient(model_spec.model)

    if model_spec.provider == "gemini":
        return GeminiClient(model_spec.model)

    raise RuntimeError(f"Unsupported provider: {model_spec.provider}")
