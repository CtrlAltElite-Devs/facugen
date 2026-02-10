from facugen.models import ModelSpec
from facugen.providers.openai_client import OpenAIClient
from facugen.providers.gemini_client import GeminiClient


def create_provider(model_spec: ModelSpec):
    if model_spec.provider == "openai":
        return OpenAIClient(model_spec.model)

    if model_spec.provider == "gemini":
        return GeminiClient(model_spec.model)

    raise RuntimeError(f"Unsupported provider: {model_spec.provider}")
